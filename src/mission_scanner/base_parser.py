from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Dict, Set, Tuple
from .models import MissionClass, Equipment

logger = logging.getLogger(__name__)

@dataclass
class ParseResult:
    """Result structure matching test expectations"""
    classes: Dict[str, MissionClass]
    equipment: Set[Equipment]

    def to_tuple(self) -> Tuple[Dict[str, MissionClass], Set[Equipment]]:
        """Convert result to tuple format for backward compatibility"""
        return (self.classes, self.equipment)

class BaseParser:
    """Base class for file parsers"""
    
    def parse(self, file_path: Path) -> ParseResult:
        """Parse file and return found classes and equipment"""
        content, encoding = self._read_file_content(file_path)
        if content is None:
            logger.error(f"Could not read {file_path} with any encoding")
            return ParseResult({}, set())
            
        if encoding != 'utf-8':
            logger.debug(f"File {file_path} using {encoding} encoding")
            
        return self._parse_content(content, file_path)
        
    def _parse_content(self, content: str, file_path: Path) -> ParseResult:
        """Parse string content and return found classes and equipment"""
        raise NotImplementedError

    def _read_file_content(self, file_path: Path) -> tuple[str | None, str]:
        """Read file content with encoding detection"""
        encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read(), encoding
            except UnicodeDecodeError:
                continue
                
        return None, 'unknown'
