import logging
import re
from typing import Dict, List, Optional, Set, Pattern, Iterator, Callable
from pathlib import Path
from datetime import datetime
import threading
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

from mission_scanner.cache import MissionCacheManager
from .models import ScanResult
from .scanner import MissionScanner

@dataclass
class MIssionScannerAPIConfig:
    """Configuration settings for AssetAPI"""
    cache_max_age: int = 3600
    cache_max_size: int = 1_000_000
    max_workers: Optional[int] = None
    error_handler: Optional[Callable[[Exception], None]] = None
    progress_callback: Optional[Callable[[str, float], None]] = None

class MissionScannerAPI:
    """API for scanning mission files."""
    
    API_VERSION = "1.0"
    VALID_EXTENSIONS = {'.sqf', '.hpp', '.ext', '.xml'}
    
    def __init__(self, cache_dir: Path, config: Optional[MIssionScannerAPIConfig] = None):
        self.config = config or MIssionScannerAPIConfig()
        if not cache_dir.is_absolute():
            cache_dir = cache_dir.resolve()
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)
            
        self._scanner = MissionScanner(max_workers=self.config.max_workers)
        self._cache = MissionCacheManager(max_size=self.config.cache_max_size)
        self._logger = logging.getLogger(__name__)
        self._stats_lock = threading.Lock()
        self._scan_stats: Dict[str, int] = {'total_scans': 0, 'failed_scans': 0}
        self._executor = ThreadPoolExecutor(max_workers=self.config.max_workers)

    def cleanup(self):
        """Clean up scanner resources."""
        self._scanner.cleanup()
        self._executor.shutdown(wait=True)

    def scan_directory(self, path: Path, patterns: Optional[List[Pattern]] = None) -> ScanResult:
        """Scan directory for mission files."""
        try:
            with self._stats_lock:
                self._scan_stats['total_scans'] += 1
                
            if not path.exists():
                raise FileNotFoundError(f"Directory not found: {path}")

            self._logger.debug(f"Scanning directory {path}")
            result = self._scanner.scan_directory(path, patterns)
            
            return result
            
        except Exception as e:
            self._handle_error(e, f"scan_directory {path}")
            raise

    def get_all_classes(self) -> Set[str]:
        """Get all class names found in scanned files."""
        return self._cache.get_all_classes()

    def get_all_equipment(self) -> Set[str]:
        """Get all equipment found in scanned files."""
        return self._cache.get_all_equipment()
    

    def get_stats(self) -> Dict[str, int]:
        """Get scan statistics."""
        with self._stats_lock:
            stats = dict(self._scan_stats)
        
        classes = len(self.get_all_classes())
        equipment = len(self.get_all_equipment())
        
        return {
            'total_scans': stats['total_scans'],
            'failed_scans': stats['failed_scans'],
            'total_classes': classes,
            'total_equipment': equipment
        }

    def _handle_error(self, error: Exception, context: str = "") -> None:
        """Central error handling"""
        if self.config and self.config.error_handler:
            try:
                self.config.error_handler(error)
            except Exception as e:
                self._logger.error(f"Error handler failed: {e}")
                return

        self._logger.error(f"Error in {context}: {error}")
        with self._stats_lock:
            self._scan_stats['failed_scans'] += 1
