import logging
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def read_file_content(file_path: Path) -> Tuple[Optional[str], Optional[str]]:
    """
    Read file content trying multiple encodings.
    Returns tuple of (content, encoding_used)
    Both values may be None if file cannot be read.
    Raises FileNotFoundError if file doesn't exist.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
        
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
            logger.debug(f"Failed to decode {file_path} with {encoding}")
            continue
        except FileNotFoundError:
            raise  # Re-raise FileNotFoundError
        except Exception as e:
            logger.warning(f"Error reading {file_path} with {encoding}: {e}")
            continue
            
    if content is None:
        # Last resort - read as bytes and decode with replace
        try:
            with open(file_path, 'rb') as f:
                content = f.read().decode('utf-8', errors='replace')
                used_encoding = 'utf-8-replace'
        except FileNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to read {file_path} with any encoding: {e}")
            return None, None
            
    return content, used_encoding
