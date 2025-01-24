import logging
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def read_file_content(file_path: Path) -> Tuple[Optional[str], str]:
    """
    Read file content trying multiple encodings.
    Returns tuple of (content, encoding_used)
    """
    encodings = [
        'utf-8',
        'cp1252',     # Windows Western European
        'iso-8859-1', # Latin-1
        'cp850',      # DOS Western European
        'latin1',     # Fallback
        'ascii',      # Last resort
    ]
    
    content = None
    used_encoding = None
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                used_encoding = encoding
                break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            logger.warning(f"Error reading {file_path} with {encoding}: {e}")
            continue
            
    if content is None:
        # Last resort - read as bytes and decode with replace
        try:
            with open(file_path, 'rb') as f:
                content = f.read().decode('utf-8', errors='replace')
                used_encoding = 'utf-8-replace'
        except Exception as e:
            logger.error(f"Failed to read {file_path} with any encoding: {e}")
            return None, ''
            
    return content, used_encoding
