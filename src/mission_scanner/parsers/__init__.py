from typing import Optional
from .base import BaseParser
from .sqf import SQFParser
from .hpp import HPPParser
from .ext import EXTParser
from .xml import XMLParser

def get_parser(file_path) -> Optional[BaseParser]:
    """Get appropriate parser for file type"""
    ext = file_path.suffix.lower()
    
    PARSER_MAP = {
        '.sqf': SQFParser(),
        '.hpp': HPPParser(),
        '.ext': EXTParser(),
        '.xml': XMLParser(),
    }
    
    return PARSER_MAP.get(ext)

__all__ = [
    'BaseParser',
    'SQFParser', 
    'HPPParser',
    'EXTParser',
    'XMLParser',
    'get_parser'
]
