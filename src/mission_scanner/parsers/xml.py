from pathlib import Path
from typing import Set, Tuple
import xml.etree.ElementTree as ET

from mission_scanner.parser import BaseParser
from ..models import MissionClass, Equipment

class XmlParser(BaseParser):
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
