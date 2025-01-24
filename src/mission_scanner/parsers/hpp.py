import logging
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass

from mission_scanner.parser import BaseParser
from mission_scanner.models import MissionClass, Equipment
from ..parsers.utils import read_file_content

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
            content, _ = read_file_content(file_path)
            if content is None:
                return classes, equipment

            return self._parse_content(content, file_path)
        except FileNotFoundError:
            raise  # Re-raise FileNotFoundError
        except Exception as e:
            logger.debug(f"Error parsing HPP file {file_path}: {e}")
            return classes, equipment

    def _parse_content(self, content: str, file_path: Path) -> Tuple[Set[MissionClass], Set[Equipment]]:
        """Parse content string and return classes and equipment"""
        classes = set()
        equipment = set()
        
        try:
            # Remove comments and empty lines
            content = re.sub(r'//.*?\n|/\*.*?\*/', '', content, flags=re.S)
            content = re.sub(r'\n\s*\n', '\n', content)

            # Updated class pattern to better handle nested content
            class_pattern = r'class\s+(\w+)(?:\s*:\s*(\w+))?\s*{((?:[^{}]|{(?:[^{}]|{[^{}]*})*})*?)}'
            
            for match in re.finditer(class_pattern, content, re.DOTALL):
                class_content = match.group(3)
                name = match.group(1)
                parent = match.group(2)
                
                if name in ('CfgPatches', 'CfgFunctions'):
                    continue

                # Extract properties
                properties = self._process_properties(class_content)

                # Create class
                cls = MissionClass(
                    name=name,
                    parent=parent,
                    properties=properties,
                    file_path=file_path
                )
                classes.add(cls)

                # Process all equipment arrays
                self._process_equipment_arrays(class_content, equipment, file_path)

        except Exception as e:
            logger.debug(f"Error parsing content from {file_path}: {e}")
            raise

        return classes, equipment

    def _process_properties(self, content: str) -> Dict[str, str]:
        """Extract all properties including arrays from class content"""
        properties = {}

        # Handle simple properties
        prop_pattern = r'(\w+)\s*=\s*"([^"]*)"'
        for prop_match in re.finditer(prop_pattern, content):
            prop_name, prop_value = prop_match.groups()
            properties[prop_name] = prop_value

        # Handle array properties
        array_patterns = [
            r'(\w+)\[\]\s*=\s*{([^}]*)}',      # Standard arrays
            r'(\w+)\[\]\s*\+=\s*{([^}]*)}',    # Extended arrays
        ]
        
        for pattern in array_patterns:
            for match in re.finditer(pattern, content, re.DOTALL):
                prop_name, items_str = match.groups()
                prop_key = f"{prop_name}[]"
                
                # Handle existing array extensions (+=)
                if "+=" in match.group(0):
                    if prop_key in properties:
                        items_str = properties[prop_key] + "," + items_str

                # Clean and store array content
                items = []
                for item_match in re.finditer(r'"([^"]*)"', items_str):
                    item = item_match.group(1).strip()
                    if item:
                        items.append(item)  # Store without quotes
                
                if items:
                    properties[prop_key] = ",".join(items)

        return properties

    def _process_equipment_arrays(self, content: str, equipment: Set[Equipment], file_path: Path) -> None:
        """Process equipment arrays from class content"""
        # Define equipment array types
        EQUIPMENT_TYPES = {
            'magazines', 'items', 'linkedItems', 'uniformItems', 'vestItems', 
            'backpackItems', 'weapons', 'primary', 'secondary', 'handgun',
            'attachment', 'uniform', 'vest', 'backpack', 'goggles', 'binocular',
            'map', 'gps', 'compass', 'watch', 'radio'
        }
        
        # Updated array patterns with consistent spacing
        array_patterns = [
            # Standard array definitions
            r'(\w+)\[\]\s*=\s*{([^}]*)}',
            # Array extensions
            r'(\w+)\[\]\s*\+=\s*{([^}]*)}',
            # Single item assignments
            r'(\w+)\s*=\s*"([^"]*)"',
            # Additional pattern for linked items
            r'(\w+)\[\]\s*=\s*\{([^}]*?)\}'  # Less greedy match
        ]

        for pattern in array_patterns:
            for match in re.finditer(pattern, content, re.DOTALL):
                category, items_str = match.groups()
                
                # Skip non-equipment arrays
                if category not in EQUIPMENT_TYPES:
                    continue

                # Process items string
                items = []
                
                # Handle quoted strings
                for item_match in re.finditer(r'"([^"]*)"', items_str):
                    item = item_match.group(1).strip()
                    if item:  # Skip empty strings
                        items.append(item)
                
                # Handle LIST_N macros
                for macro_match in re.finditer(r'LIST_(\d+)\("([^"]+)"\)', items_str):
                    count = int(macro_match.group(1))
                    item = macro_match.group(2).strip()
                    if item:
                        items.extend([item] * count)

                # Add equipment items
                for item in items:
                    equipment.add(Equipment(
                        name=item,
                        type=category,
                        category=category,
                        file_path=file_path
                    ))
