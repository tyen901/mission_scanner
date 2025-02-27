from typing import Optional
from pathlib import Path
from .base_parser import BaseParser
from .sqf_parser import SqfParser
from .hpp_parser import HppParser
from .sqm_parser import SqmParser

PARSER_MAP = {
    '.sqf': SqfParser(),
    '.hpp': HppParser(), 
    '.sqm': SqmParser(),
}
def get_parser(file_path: Path) -> Optional[BaseParser]:
    """Get appropriate parser for file type
    
    Args:
        file_path: Path-like object with a suffix attribute
        
    Returns:
        BaseParser instance or None if extension not supported
        
    Raises:
        AttributeError: If file_path doesn't have suffix attribute
        ValueError: If file_path suffix is empty
    """
    try:
        ext = file_path.suffix.lower()
        if not ext:
            raise ValueError("File has no extension")
            

        return PARSER_MAP.get(ext)
        
    except AttributeError:
        raise AttributeError(f"Invalid file path object: {file_path}")

__all__ = [
    'get_parser',
    'HppParser',
    'SqmParser',
    'SqfParser',
]
