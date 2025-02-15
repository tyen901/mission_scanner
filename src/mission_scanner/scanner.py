import os
from pathlib import Path
from typing import Dict, List, Pattern, Optional
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from .base_parser import ParseResult
from .models import ScanResult, MissionClass, Equipment
from .parsers import get_parser

logger = logging.getLogger(__name__)

class MissionScanner:
    """Scanner for mission files to extract class and equipment definitions"""
    
    VALID_EXTENSIONS = {'.sqf', '.hpp', '.ext', '.xml'}
    
    # Define filters per file extension
    DEFAULT_FILTERS = {
        '.sqf': {'loadout', 'arsenal', 'curated', 'config'},
        '.hpp': set(),  # No filters for hpp files
        '.ext': set(),  # No filters for ext files
        '.xml': set()   # No filters for xml files
    }

    def __init__(self, max_workers: int | None = None, filename_filters: Dict[str, set[str]] | None = None):
        """Initialize scanner with optional thread pool size and filename filters"""
        self._max_workers = max(1, (os.cpu_count() or 2) - 1) if max_workers is None else max_workers
        self._executor = ThreadPoolExecutor(max_workers=self._max_workers)
        self.progress_callback = None
        self._filename_filters = filename_filters or self.DEFAULT_FILTERS

    def scan_directory(self, path: Path, patterns: Optional[List[Pattern]] = None) -> ScanResult:
        """Scan directory for class and equipment definitions"""
        classes: Dict[str, MissionClass] = {}
        equipment: Dict[str, Equipment] = {}
        errors: List[str] = []
        futures = []

        patterns = patterns or []  # Convert None to empty list

        # Collect all mission files
        for file_path in path.rglob('*'):
            suffix = file_path.suffix.lower()
            if not file_path.is_file() or suffix not in self.VALID_EXTENSIONS:
                continue

            # Apply extension-specific filters
            filters = self._filename_filters.get(suffix, set())
            if filters and not any(filter_term.lower() in file_path.stem.lower() for filter_term in filters):
                continue

            if self.progress_callback:
                self.progress_callback(str(file_path))

            if patterns and not any(p.match(str(file_path)) for p in patterns):
                continue

            futures.append(self._executor.submit(self._scan_file, file_path))

        # Process results
        for future in as_completed(futures):
            try:
                result = future.result()
                classes.update(result.classes)
                equipment.update({eq.name: eq for eq in result.equipment})
            except Exception as e:
                errors.append(str(e))
                logger.error(f"Error processing file: {e}")

        return ScanResult(classes=classes, equipment=equipment, errors=errors)

    def _scan_file(self, file_path: Path) -> ParseResult:
        """Scan a single file for class and equipment definitions"""
        parser = get_parser(file_path)
        if not parser:
            return ParseResult({}, set())

        try:
            return parser.parse(file_path)
        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {e}")
            raise

    def cleanup(self):
        """Clean up resources"""
        self._executor.shutdown(wait=True)
