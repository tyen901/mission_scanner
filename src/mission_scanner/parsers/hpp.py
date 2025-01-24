import logging
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass

from mission_scanner.parser import BaseParser
from mission_scanner.models import MissionClass, Equipment

logger = logging.getLogger(__name__)

class HPPParser(BaseParser):
    """Parser for HPP configuration files"""
    
    def __init__(self):
        self._nested_level = 0
        self._max_nested_level = 10
        self._class_cache = {}
        self._nested_content = set()
        self._classes = {}
        self._equipment = []

    def parse(self, file_path: Path) -> Tuple[Set[MissionClass], Set[Equipment]]:
        """Parse HPP file and return classes and equipment"""
        classes = set()
        equipment = set()
        
        try:
            # Try UTF-8 first, then fallback to other encodings
            content = None
            encodings = ['utf-8', 'latin1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
                    
            if content is None:
                raise UnicodeDecodeError(f"Failed to decode {file_path} with any encoding")

            # Remove comments and empty lines
            content = re.sub(r'//.*?\n|/\*.*?\*/', '', content, flags=re.S)
            content = re.sub(r'\n\s*\n', '\n', content)

            # Updated class pattern to better handle nested content
            class_pattern = r'class\s+(\w+)(?:\s*:\s*(\w+))?\s*{((?:[^{}]|{(?:[^{}]|{[^{}]*})*})*?)}'
            
            # First pass - extract all classes and their basic info
            for match in re.finditer(class_pattern, content, re.DOTALL):
                class_content = match.group(3)  # Class content is in group 3
                name = match.group(1)
                parent = match.group(2)
                
                # Skip config classes
                if name in ('CfgPatches', 'CfgFunctions'):
                    continue

                # Extract properties
                properties = {}
                # Handle simple properties
                prop_pattern = r'(\w+)\s*=\s*"([^"]*)"'
                for prop_match in re.finditer(prop_pattern, class_content):
                    prop_name, prop_value = prop_match.groups()
                    properties[prop_name] = prop_value

                # Create class
                cls = MissionClass(
                    name=name,
                    parent=parent,
                    properties=properties,
                    file_path=file_path
                )
                classes.add(cls)

                # Parse arrays with fixed patterns
                array_patterns = [
                    r'(\w+)\[\]\s*=\s*{([^}]*)}',      # Standard arrays
                    r'(\w+)\[\]\s*\+=\s*{([^}]*)}',    # Extended arrays
                ]
                
                # Process equipment arrays
                self._process_equipment_arrays(class_content, array_patterns, equipment, file_path)

            return classes, equipment

        except Exception as e:
            logger.error(f"Error parsing HPP file {file_path}: {e}")
            raise

    def _process_equipment_arrays(self, content: str, patterns: List[str], 
                                equipment: Set[Equipment], file_path: Path) -> None:
        """Process equipment arrays from class content"""
        # Process regular string arrays
        for pattern in patterns:
            for match in re.finditer(pattern, content, re.DOTALL):  # Add re.DOTALL flag
                category, items_str = match.groups()
                
                if not items_str.strip():
                    continue

                # Process direct string items and LIST_N macros
                items = []
                
                # Handle direct string items - update pattern to handle multi-line
                direct_items = []
                for item_match in re.finditer(r'"([^"]*)"', items_str):
                    item = item_match.group(1).strip()
                    if item:  # Only add non-empty strings
                        direct_items.append(item)
                items.extend(direct_items)
                
                # Handle LIST_N macros - no changes needed
                for macro_match in re.finditer(r'LIST_(\d+)\("([^"]+)"\)', items_str):
                    count = int(macro_match.group(1))
                    item = macro_match.group(2)
                    if item.strip():
                        items.extend([item] * count)

                # Add all found items
                for item in items:
                    equipment.add(Equipment(
                        name=item,
                        type=category,
                        category=category,
                        file_path=file_path
                    ))
