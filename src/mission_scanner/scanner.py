import os
from pathlib import Path
from typing import Set, Dict, Optional, List, Pattern
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from .models import ScanResult, MissionClass, Equipment
from .parsers import get_parser

logger = logging.getLogger(__name__)

class MissionScanner:
    """Scanner for mission files to extract class and equipment definitions"""
    
    VALID_EXTENSIONS = {'.sqf', '.hpp', '.ext', '.xml'}

    def __init__(self, max_workers: int | None = None):
        """Initialize scanner with optional thread pool size"""
        self._max_workers = max(1, (os.cpu_count() or 2) - 1) if max_workers is None else max_workers
        self._executor = ThreadPoolExecutor(max_workers=self._max_workers)
        self.progress_callback = None

    def scan_directory(self, path: Path, patterns: List[Pattern] = None) -> ScanResult:
        """Scan directory for class and equipment definitions"""
        classes: Dict[str, MissionClass] = {}
        equipment: Dict[str, Equipment] = {}
        errors: List[str] = []
        futures = []

        # Collect all mission files
        for file_path in path.rglob('*'):
            if not file_path.is_file() or file_path.suffix.lower() not in self.VALID_EXTENSIONS:
                continue

            if self.progress_callback:
                self.progress_callback(str(file_path))

            if patterns and not any(p.match(str(file_path)) for p in patterns):
                continue

            futures.append(self._executor.submit(self._scan_file, file_path))

        # Process results
        for future in as_completed(futures):
            try:
                file_classes, file_equipment = future.result()
                classes.update(file_classes)
                equipment.update(file_equipment)
            except Exception as e:
                errors.append(str(e))
                logger.error(f"Error processing file: {e}")

        return ScanResult(classes=classes, equipment=equipment, errors=errors)

    def _scan_file(self, file_path: Path) -> tuple[Dict[str, MissionClass], Dict[str, Equipment]]: 
        """Scan a single file for class and equipment definitions"""
        parser = get_parser(file_path)
        if not parser:
            return {}, {}

        try:
            file_classes, file_equipment = parser.parse(file_path)
            return (
                {cls.name: cls for cls in file_classes},
                {eq.name: eq for eq in file_equipment}
            )
        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {e}")
            raise

    def cleanup(self):
        """Clean up resources"""
        self._executor.shutdown(wait=True)
