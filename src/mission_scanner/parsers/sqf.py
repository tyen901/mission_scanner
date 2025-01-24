import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
import xml.etree.ElementTree as ET
import json

from mission_scanner.models import Equipment, MissionClass
from mission_scanner.parser import BaseParser

class SQFParser(BaseParser):
    """Parser for SQF script files"""
    def parse(self, file_path: Path) -> Tuple[Set[MissionClass], Set[Equipment]]:
        classes = set()
        equipment = set()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find class definitions
        class_matches = re.finditer(
            r'class\s+(\w+)(?:\s*:\s*(\w+))?\s*\{([^}]*)\}',
            content,
            re.MULTILINE
        )
        
        for match in class_matches:
            name = match.group(1)
            parent = match.group(2)
            properties = {}
            
            # Extract properties from class body
            if match.group(3):
                prop_matches = re.finditer(
                    r'(\w+)\s*=\s*"([^"]*)"',
                    match.group(3)
                )
                properties = {m.group(1): m.group(2) for m in prop_matches}
            
            classes.add(MissionClass(
                name=name,
                parent=parent,
                file_path=file_path,
                properties=properties
            ))
            
            # If this is an equipment class, also add it as equipment
            if parent in {'Rifle', 'Pistol', 'Launcher', 'Item'}:
                equipment.add(Equipment(
                    name=name,
                    type=parent,
                    class_name=name,
                    properties=properties,
                    file_path=file_path
                ))
                
        return classes, equipment
