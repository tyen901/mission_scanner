import logging
import re
from pathlib import Path
from typing import Dict, Set, Any

from mission_scanner.parser import BaseParser, ParseResult
from mission_scanner.models import MissionClass, Equipment
from mission_scanner.parser import read_file_content

from class_scanner import ClassParser, PropertyValue

logger = logging.getLogger(__name__)

class HppParser(BaseParser):
    """Parser for HPP configuration files"""
    
    def __init__(self):
        self.class_parser = ClassParser()
        # Add regex for matching macros
        self.macro_pattern = re.compile(r'LIST_\d+\("([^"]*)"\)')

    def parse(self, file_path: Path) -> ParseResult:
        """Parse HPP file and return classes and equipment"""
        classes: Dict[str, MissionClass] = {}
        equipment: Set[Equipment] = set()
        
        try:
            content, _ = read_file_content(file_path)
            if content is None:
                return ParseResult(classes, equipment)

            # Parse with ClassParser
            parsed = self.class_parser.parse_class_definitions(content)
            
            # Convert parsed data to MissionClass and Equipment
            for section_name, section_data in parsed.items():
                for class_name, class_data in section_data.items():
                    # Create MissionClass
                    mission_class = MissionClass(
                        name=class_name,
                        parent=class_data["parent"],
                        properties=class_data["properties"],
                        file_path=file_path
                    )
                    classes[class_name] = mission_class
                    
                    # Process equipment arrays
                    self._process_equipment_arrays(
                        class_data["properties"],
                        equipment,
                        file_path
                    )

        except FileNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error parsing HPP file {file_path}: {e}", exc_info=True)
            
        return ParseResult(classes, equipment)

    def _process_equipment_arrays(self, properties: Dict[str, Any], equipment: Set[Equipment], file_path: Path) -> None:
        """Process equipment arrays from class properties"""
        EQUIPMENT_TYPES = {
            'magazines', 'items', 'linkedItems', 'uniformItems', 'vestItems', 
            'backpackItems', 'weapons', 'primary', 'secondary', 'handgun',
            'uniform', 'vest', 'backpack', 'goggles', 'binocular',
            'map', 'gps', 'compass', 'watch', 'radio'
        }
        
        for key, value in properties.items():
            if not isinstance(value, PropertyValue):
                continue
                
            base_name = key.rstrip('[]')
            if base_name not in EQUIPMENT_TYPES:
                continue
                
            # Handle array values
            if value.is_array:
                # Clean macro from each array value
                cleaned_values = [
                    self._clean_macro(item) for item in value.array_values
                    if item  # Skip empty strings
                ]
                
                # Update the PropertyValue with cleaned values
                value.array_values = cleaned_values
                
                # Add equipment items
                for item in cleaned_values:
                    equipment.add(Equipment(
                        name=item,
                        type=base_name,
                        category=base_name,
                        file_path=file_path
                    ))
            # Handle single values
            elif value.raw_value:
                cleaned_value = self._clean_macro(value.raw_value)
                value.raw_value = cleaned_value
                equipment.add(Equipment(
                    name=cleaned_value,
                    type=base_name,
                    category=base_name,
                    file_path=file_path
                ))

    def _clean_macro(self, value: str) -> str:
        """Clean macros from a value string"""
        if match := self.macro_pattern.match(value.strip()):
            return match.group(1)
        return value.strip('" ')
