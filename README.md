# Mission Scanner

A tool for scanning and analyzing mission files to extract class definitions and equipment.

## Overview

Mission Scanner is focused on parsing various file formats commonly found in mission files:
- .sqf (Arma 3 scripting files)
- .hpp (Header files)
- .ext (Configuration files) 
- .xml (String tables)
- .json (Configuration files)
- .txt (Plain text files)

## Features

- Extract class definitions and equipment information
- Parse multiple file formats
- Thread-safe caching
- Database storage of findings
- Progress tracking and logging

## Implementation Plan

1. **Core Models**
   - Class definitions
   - Equipment definitions
   - Scan results
   - Asset representations

2. **File Parsers**
   - SQF parser for script files
   - HPP parser for header files
   - EXT parser for config files
   - XML parser for string tables
   - JSON parser for config files
   - TXT parser for plain text

3. **Cache System**
   - Thread-safe cache manager
   - Immutable cache container
   - Bulk loading support
   - Cache invalidation

4. **Database Integration**
   - Store class definitions
   - Store equipment information
   - Track relationships
   - Query capabilities

## Usage

```python
from mission_scanner import AssetAPI
from pathlib import Path

# Initialize scanner
api = AssetAPI(Path("cache"))

# Scan directory
result = api.scan_directory(Path("sample_data"))

# Access findings
classes = result.classes
equipment = result.equipment

# Query database
class_info = api.get_class("SoldierWB")
equipment_info = api.get_equipment("rifle_mk20")
```

## Development

Requirements:
- Python 3.8+
- SQLite support
- Threading support

## License

MIT License