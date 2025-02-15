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
            
            # Modify array item definitions pattern to not capture entire array content
            r'(?:private\s+)?_\w+\s*=\s*\[(?:[^]]+)\]',
            
            # Only match individual quoted items
            r'"([^"]+)"(?:\s*,\s*|\s*$)'
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

        # Add patterns for identifying parameter-like values
        self._param_patterns = [
            re.compile(r'^-?\d+$'),  # Numeric values
            re.compile(r'^(?:true|false)$', re.IGNORECASE),  # Boolean values
            re.compile(r'^\[\s*\]$'),  # Empty arrays
            re.compile(r'^"?(?:NONE|DEFAULT|FLY|FLYING)"?$', re.IGNORECASE),  # Common default strings with optional quotes
            re.compile(r'^""?$'),  # Empty string with or without quotes
        ]

        # Add pattern to identify settings
        self._settings_pattern = re.compile(r'^[a-z0-9_]+_[a-z0-9_]+_[a-z0-9_]+\s*=', re.IGNORECASE)

        # Add pattern to identify briefing content
        self._briefing_patterns = [
            re.compile(r'createDiaryRecord'),  # Diary record creation
            re.compile(r'\["diary",\s*\['),    # Diary array structure
            re.compile(r'<br\s*/?>'),          # HTML line breaks
            re.compile(r'<font\s+size='),      # Font size tags
        ]

        # Array parsing patterns
        self._array_item_pattern = re.compile(r'"([^"]+)"(?:\s*,\s*|\s*$)')
        self._array_def_pattern = re.compile(r'(?:private\s+)?_(\w+)\s*=\s*\[((?:[^]]+))\]')
        self._array_section_pattern = re.compile(r'//[^\n]*(?:\n|$)|/\*.*?\*/|^\s*$', re.MULTILINE | re.DOTALL)

        # Add pattern for strict class detection
        self._class_pattern = re.compile(r'^\s*class\s+[a-zA-Z_][a-zA-Z0-9_]*\s*{', re.MULTILINE)

        # Add patterns for UI/script elements to ignore
        self._ui_patterns = [
            re.compile(r'\\[A-Za-z0-9_\\]+'),  # File paths
            re.compile(r'^[a-z_]+_arsenal$', re.IGNORECASE),  # Arsenal action names
            re.compile(r'startpos'),  # Variable references
            re.compile(r'^Personal\s+Arsenal$'),  # UI labels
            re.compile(r'^\([^)]+\)$'),  # Expressions in parentheses
        ]

    def _clean_sqf_code(self, content: str) -> str:
        """Clean SQF code and convert to single line for processing"""
        # Remove comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)  # Single line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # Multi-line comments
        
        # Preserve class blocks before general formatting
        class_blocks = []
        def preserve_class(match):
            class_blocks.append(match.group(0))
            return f"__CLASS_BLOCK_{len(class_blocks)-1}__"
            
        content = self._class_pattern.sub(preserve_class, content)
        
        # Handle general formatting
        content = re.sub(r'\\\s*\n', ' ', content)  # Line continuations
        content = re.sub(r'\s+', ' ', content)  # Whitespace
        content = re.sub(r'([{};])', r' \1 ', content)  # Spacing around symbols
        
        # Restore class blocks
        for i, block in enumerate(class_blocks):
            content = content.replace(f"__CLASS_BLOCK_{i}__", block)
            
        # Preserve array structure
        content = re.sub(r'\[\s*', '[', content)
        content = re.sub(r'\s*\]', ']', content)
        content = re.sub(r'\s*\+\s*', '+', content)
        
        return content.strip()

    def _is_script_parameter(self, value: str) -> bool:
        """Check if a value matches common script parameter patterns"""
        if not value:
            return True
            
        # Remove quotes for string comparison
        clean_value = value.strip('"')
        
        # Check for script control flags and special modes
        script_flags = {'NONE', 'DEFAULT', 'FLY', 'FLYING', 'GUARD', 'DEBUG'}
        if clean_value.upper() in script_flags:
            return True
            
        # Also check if it's a simple numeric assignment
        try:
            float(clean_value)
            return True
        except ValueError:
            pass
            
        # Check against parameter patterns
        return any(pattern.match(clean_value) for pattern in self._param_patterns)

    def _is_ui_string(self, value: str) -> bool:
        """Check if string is UI-related and should be ignored"""
        return any(pattern.search(value) for pattern in self._ui_patterns)

    def _extract_variables(self, code: str) -> Dict[str, str]:
        """Extract variable assignments from cleaned code"""
        variables = {}
        matches = re.finditer(r'(?:private\s+)?_(\w+)\s*=\s*"([^"]+)"', code)
        for match in matches:
            var_name, var_value = match.groups()
            # Skip common script variables and parameter-like values
            if (var_name not in self._ignored_vars and 
                not var_value.startswith(('$', 'WhiteHead_')) and
                not self._is_script_parameter(var_value)):
                variables[var_name] = var_value
        return variables

    def _clean_array_section(self, array_text: str) -> str:
        """Clean array section by removing comments and fixing formatting"""
        # Handle empty sections
        if not array_text.strip():
            return ""
            
        # Remove comments
        lines = []
        for line in array_text.splitlines():
            line = re.sub(r'//.*$', '', line)  # Remove single line comments
            line = line.strip()
            if line:  # Only keep non-empty lines
                lines.append(line)
                
        # Join and clean
        cleaned = ' '.join(lines)
        cleaned = re.sub(r'\s*,\s*', ', ', cleaned)  # Normalize comma spacing
        cleaned = cleaned.strip().rstrip(',')  # Remove trailing comma
        return cleaned

    def _extract_arrays(self, code: str) -> None:
        """Extract array assignments from cleaned code"""
        # Find array definitions
        array_pattern = re.compile(r'(?:private\s+)?_(\w+)\s*=\s*\[(.*?)\]', re.DOTALL)
        # Only match individual quoted items
        item_pattern = re.compile(r'"([^"]+)"(?:\s*,\s*|\s*$)')
        
        array_matches = array_pattern.finditer(code)
        for match in array_matches:
            array_name = match.group(1)

            array_content = self._clean_array_section(match.group(2))
            
            if array_content:
                # Extract individual quoted items
                items = []
                for item_match in item_pattern.finditer(array_content):
                    item = item_match.group(1)
                    if (item and 
                        not self._is_script_parameter(item) and 
                        not self._is_ui_string(item) and
                        not item.startswith('WhiteHead_')):
                        items.append(item)
                        
                if items:
                    self._arrays[array_name] = items

    def _is_settings_line(self, line: str) -> bool:
        """Check if a line is a settings assignment"""
        return bool(self._settings_pattern.match(line.strip()))

    def _contains_settings(self, content: str) -> bool:
        """Check if content contains settings definitions"""
        # Count settings-like lines
        settings_count = sum(1 for line in content.splitlines() 
                           if self._is_settings_line(line))
        # If more than 25% of non-empty lines are settings, consider it a settings file
        non_empty_lines = sum(1 for line in content.splitlines() if line.strip())
        return non_empty_lines > 0 and settings_count / non_empty_lines > 0.25

    def _is_briefing_content(self, content: str) -> bool:
        """Check if content matches briefing file patterns"""
        # Look for common briefing file patterns
        matches = sum(1 for pattern in self._briefing_patterns 
                     if pattern.search(content))
        # If at least 2 patterns match, consider it a briefing file
        return matches >= 2

    def parse(self, file_path: Path) -> ParseResult:
        """Parse SQF file and extract equipment references"""
        classes: Dict[str, MissionClass] = {}
        equipment: Set[Equipment] = set()
        
        try:
            content, _ = read_file_content(file_path)
            if not content:
                return ParseResult(classes, equipment)

            # Skip parsing if file contains briefing content or settings
            if self._is_briefing_content(content) or self._contains_settings(content):
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

            # Split into class blocks using strict pattern
            blocks = []
            current_block = ""
            in_class = False
            for line in cleaned_code.splitlines():
                if self._class_pattern.match(line):
                    if current_block:
                        blocks.append(current_block)
                    current_block = line
                    in_class = True
                elif in_class and "}" in line:
                    current_block += " " + line
                    blocks.append(current_block)
                    current_block = ""
                    in_class = False
                else:
                    current_block += " " + line
            if current_block:
                blocks.append(current_block)

            # Process blocks
            for block in blocks:
                self._in_class_block = bool(self._class_pattern.match(block))
                
                # Process patterns
                for pattern in self._compiled_patterns:
                    matches = pattern.finditer(block)
                    for match in matches:
                        groups = match.groups()
                        if len(groups) == 1:  # Direct string reference
                            item = groups[0]
                            if item not in self._ignored_vars:  # Skip script variables
                                if item in self._variables:  # Variable reference
                                    item = self._variables[item]
                                if not self._is_script_parameter(item):  # Skip parameter-like values
                                    self._add_equipment(equipment, item, file_path)
                        elif len(groups) == 2:  # Variable assignment
                            var_name, var_value = groups
                            if (var_name not in self._ignored_vars and 
                                not self._is_script_parameter(var_value)):
                                self._add_equipment(equipment, var_value, file_path)

        except Exception as e:
            print(f"Error parsing SQF file {file_path}: {e}")
            
        return ParseResult(classes, equipment)

    def _add_equipment(self, equipment: Set[Equipment], item_name: str, file_path: Path) -> None:
        """Helper method to add equipment items"""
        if (not item_name or 
            self._is_script_parameter(item_name) or
            self._is_ui_string(item_name)):
            return
            
        equipment.add(Equipment(
            name=item_name,
            type='unknown',
            category='equipment',
            file_path=file_path
        ))
