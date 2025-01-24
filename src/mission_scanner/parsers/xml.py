import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
import xml.etree.ElementTree as ET
import json

from mission_scanner.parser import BaseParser
from ..models import MissionClass, Equipment

class XMLParser(BaseParser):
    """Parser for XML files"""
    def parse(self, file_path: Path) -> Tuple[Set[MissionClass], Set[Equipment]]:
        classes = set()
        equipment = set()
        
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        for elem in root.findall(".//class"):
            name = elem.get('name')
            parent = elem.get('extends')
            properties = {
                child.tag: child.text
                for child in elem
                if child.text
            }
            
            if name:
                classes.add(MissionClass(
                    name=name,
                    parent=parent,
                    file_path=file_path,
                    properties=properties
                ))
                
        return classes, equipment
