import re
from pathlib import Path
from typing import Dict, Set

from mission_scanner.models import Equipment, MissionClass
from mission_scanner.parser import BaseParser, ParseResult
from mission_scanner.parser import read_file_content

class SqfParser(BaseParser):
    """Parser for SQF script files"""
    
    def __init__(self):
        # Match common equipment addition patterns
        self._patterns = [
            # Match addItemToX commands: _unit addItemToUniform "ItemName";
            r'addItemTo(?:Uniform|Vest|Backpack)\s+"([^"]+)"',
            
            # Match addX commands with direct strings
            r'(?:add|forceAdd)(?:Weapon|Magazine|Item|Goggles|Headgear|BackPack|Binocular|Uniform)\s+"([^"]+)"',
            
            # Match variable assignments: _varname = "ItemName";
            r'(?:private\s+)?_(\w+)\s*=\s*"([^"]+)"',
            
            # Match linked item additions: _unit linkItem "ItemName";
            r'linkItem\s+"([^"]+)"',
            
            # Match weapon item additions: _unit addWeaponItem ["WeaponClass", "ItemName"];
            r'addWeaponItem\s*\[[^,]+,\s*"([^"]+)"',
            
            # Match commands using variable references
            r'(?:add|forceAdd)(?:Weapon|Magazine|Item|Goggles|Headgear|BackPack|Binocular|Uniform)\s+_(\w+)',

            # Match inventory class assignments
            r'(?:uniform|vest|backpack|headgear)\s*=\s*"([^"]+)"',
            
            # Match weapon and magazine class assignments in class blocks
            r'(?:name|typeName)\s*=\s*"([^"]+)"',
            
            # Match class property assignments in mission.sqm
            r'(?:name|optics|typeName)\s*=\s*"([^"]+)"',
            
            # Match magazine references in mission.sqm
            r'(?:primary|secondary|handgun)MuzzleMag\s*\{\s*name\s*=\s*"([^"]+)"',
            
            # Match array item definitions: "_itemUniform = ["ItemName1", "ItemName2"];"
            r'(?:private\s+)?_\w+\s*=\s*\[((?:"[^"]+"\s*,?\s*)+)\]',
            
            # Match array item assignments: [arsenal, (_itemGear + _itemUniform)]
            r'\[arsenal,\s*\((.+?)\)\]',
            
            # Match individual items in arrays: "ItemName",
            r'"([^"]+)"(?:\s*,\s*\d*)?'
        ]
        
        # Common script variables to ignore
        self._ignored_vars = {
            '_i',  # Loop counter
            '_x',  # forEach iterator
            '_unit',  # Unit reference
            '_player'  # Player reference
        }
        
        self._compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self._patterns]
        self._variables = {}
        self._arrays = {}  # Store array variables
        self._in_class_block = False

    def _clean_sqf_code(self, content: str) -> str:
        """Clean SQF code and convert to single line for processing"""
        # Remove comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)  # Single line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # Multi-line comments
        
        # Handle class blocks by adding spaces around braces
        content = re.sub(r'(class\s+\w+\s*{)', r'\1 ', content)
        content = re.sub(r'}', ' } ', content)
        
        # Remove line continuations and newlines
        content = re.sub(r'\\\s*\n', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        
        # Convert all brackets and semicolons to have spaces
        content = re.sub(r'([{};])', r' \1 ', content)
        
        # Remove extra whitespace
        content = ' '.join(content.split())
        
        # Preserve array structure
        content = re.sub(r'\[\s*', '[', content)
        content = re.sub(r'\s*\]', ']', content)
        content = re.sub(r'\s*\+\s*', '+', content)
        
        return content

    def _extract_variables(self, code: str) -> Dict[str, str]:
        """Extract variable assignments from cleaned code"""
        variables = {}
        matches = re.finditer(r'(?:private\s+)?_(\w+)\s*=\s*"([^"]+)"', code)
        for match in matches:
            var_name, var_value = match.groups()
            # Skip common script variables and non-equipment values
            if (var_name not in self._ignored_vars and 
                not var_value.startswith(('$', 'WhiteHead_'))):
                variables[var_name] = var_value
        return variables

    def _extract_arrays(self, code: str) -> None:
        """Extract array assignments from cleaned code"""
        array_matches = re.finditer(r'(?:private\s+)?_(\w+)\s*=\s*\[((?:"[^"]+"\s*,?\s*)+)\]', code)
        for match in array_matches:
            array_name = match.group(1)
            items = re.findall(r'"([^"]+)"(?:\s*,\s*\d*)?', match.group(2))
            self._arrays[array_name] = [i for i in items if not i.startswith(('$', 'WhiteHead_', ''))]

    def parse(self, file_path: Path) -> ParseResult:
        """Parse SQF file and extract equipment references"""
        classes: Dict[str, MissionClass] = {}
        equipment: Set[Equipment] = set()
        
        try:
            content, _ = read_file_content(file_path)
            if not content:
                return ParseResult(classes, equipment)

            # Clean and prepare code
            cleaned_code = self._clean_sqf_code(content)
            
            # Extract variables and arrays
            self._variables = self._extract_variables(cleaned_code)
            self._extract_arrays(cleaned_code)
            
            # Add equipment from variable values
            for var_value in self._variables.values():
                self._add_equipment(equipment, var_value, file_path)

            # Process arrays
            for items in self._arrays.values():
                for item in items:
                    self._add_equipment(equipment, item, file_path)

            # Process arsenal array combinations
            arsenal_matches = re.finditer(r'\[arsenal,\s*\((.+?)\)\]', cleaned_code)
            for match in arsenal_matches:
                array_refs = re.findall(r'_(\w+)', match.group(1))
                for ref in array_refs:
                    if ref in self._arrays:
                        for item in self._arrays[ref]:
                            self._add_equipment(equipment, item, file_path)

            # Split into class blocks for better parsing
            blocks = re.split(r'(class\s+\w+\s*{|})', cleaned_code)
            
            for block in blocks:
                if 'class' in block:
                    self._in_class_block = True
                elif '}' in block:
                    self._in_class_block = False
                
                # Process all patterns
                for pattern in self._compiled_patterns:
                    matches = pattern.finditer(block)
                    for match in matches:
                        groups = match.groups()
                        if len(groups) == 1:  # Direct string reference
                            item = groups[0]
                            if item not in self._ignored_vars:  # Skip script variables
                                if item in self._variables:  # Variable reference
                                    item = self._variables[item]
                                self._add_equipment(equipment, item, file_path)
                        elif len(groups) == 2:  # Variable assignment
                            var_name, var_value = groups
                            if var_name not in self._ignored_vars:
                                self._add_equipment(equipment, var_value, file_path)

        except Exception as e:
            print(f"Error parsing SQF file {file_path}: {e}")
            
        return ParseResult(classes, equipment)

    def _add_equipment(self, equipment: Set[Equipment], item_name: str, file_path: Path) -> None:
        """Helper method to add equipment items"""
        if not item_name or item_name.startswith(('$', 'WhiteHead_')):
            return
            
        equipment.add(Equipment(
            name=item_name,
            type='unknown',
            category='equipment',
            file_path=file_path
        ))
