import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
import xml.etree.ElementTree as ET
import json
from .models import MissionClass, Equipment

class BaseParser:
    """Base class for file parsers"""
    def parse(self, file_path: Path) -> Tuple[Set[MissionClass], Set[Equipment]]:
        """Parse file and return found classes and equipment"""
        raise NotImplementedError
