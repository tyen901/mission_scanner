from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Dict, Set
from .models import MissionClass, Equipment
from .parsers.parser_utils import read_file_content

logger = logging.getLogger(__name__)

@dataclass
class ParseResult:
    """Result structure matching test expectations"""
    classes: Dict[str, MissionClass]
    equipment: Set[Equipment]

class BaseParser:
    """Base class for file parsers"""
    
    def parse(self, file_path: Path) -> ParseResult:
        """Parse file and return found classes and equipment"""
        content, encoding = read_file_content(file_path)
        if content is None:
            logger.error(f"Could not read {file_path} with any encoding")
            return ParseResult({}, set())
            
        if encoding != 'utf-8':
            logger.debug(f"File {file_path} using {encoding} encoding")
            
        return self._parse_content(content, file_path)
        
    def _parse_content(self, content: str, file_path: Path) -> ParseResult:
        """Parse string content and return found classes and equipment"""
        raise NotImplementedError
