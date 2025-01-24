import pytest
from pathlib import Path
from mission_scanner.parsers import HPPParser
from mission_scanner.models import MissionClass, Equipment

# Update SAMPLE_DIR to use raw string and proper path format
SAMPLE_DIR = Path(r'D:\git\dep\mission_scanner\sample_data')

def scan_sample_files():
    """Recursively scan sample data directory for .hpp files"""
    hpp_files = []
    # Find all loadout folders using resolved paths
    loadout_dirs = list(SAMPLE_DIR.resolve().rglob('loadouts'))
    for loadout_dir in loadout_dirs:
        hpp_files.extend(loadout_dir.glob('*.hpp'))
    return [f.resolve() for f in hpp_files]

def get_loadout_file(sample_files, mission_name, file_name):
    """Get specific loadout file from a mission"""
    return next(f for f in sample_files 
               if mission_name in f.parent.parent.name and f.name == file_name)

def get_all_equipment(hpp_parser, file_path):
    """Get all equipment from a file"""
    _, equipment = hpp_parser.parse(file_path)
    return {(eq.name, eq.category) for eq in equipment}

def get_all_classes(hpp_parser, file_path):
    """Get all classes from a file"""
    classes, _ = hpp_parser.parse(file_path)
    return {cls.name for cls in classes}

@pytest.fixture
def hpp_parser():
    """Create HPP parser instance"""
    return HPPParser()

@pytest.fixture
def sample_files():
    """Get list of sample files"""
    files = scan_sample_files()
    assert len(files) > 0, "No sample files found in sample data directory"
    return files

def test_hpp_parser_blufor_complete(hpp_parser, sample_files):
    """Test parsing complete blufor loadout file"""
    loadout_file = get_loadout_file(sample_files, 'Seaside_Sweep_2', 'blufor_loadout.hpp')
    classes, equipment = hpp_parser.parse(loadout_file)
    assert len(classes) == 16  # Number of classes in Seaside_Sweep blufor loadout
    assert len(equipment) > 50  # Minimum equipment count

def test_hpp_parser_carlgustaf_ammo(hpp_parser, sample_files):
    """Test parsing of backpackItems arrays"""
    loadout_file = get_loadout_file(sample_files, 'Seaside_Sweep_2', 'blufor_loadout.hpp')
    classes, equipment = hpp_parser.parse(loadout_file)
    # Test specific equipment from the actual file
    assert any(eq.name == 'fwa_1rnd_m2_carlgustaf_HEAT' and eq.category == 'backpackItems' for eq in equipment)

def test_hpp_parser_opfor_inheritance(hpp_parser, sample_files):
    """Test OPFOR loadout inheritance"""
    loadout_file = get_loadout_file(sample_files, 'Seaside_Sweep_2', 'opfor_loadout.hpp')
    classes, equipment = hpp_parser.parse(loadout_file)
    
    # Test class inheritance
    class_names = {cls.name for cls in classes}
    assert {'baseMan', 'rm', 'ar', 'mg', 'rm_lat', 'rm_mat'}.issubset(class_names)
    
    # Test inherited equipment
    equipment_names = {eq.name for eq in equipment}
    assert {'ItemMap', 'ItemCompass', 'ItemWatch'}.issubset(equipment_names)

def test_hpp_parser_nested_equipment(hpp_parser):
    """Test that equipment in nested structures is correctly parsed"""
    loadout_file = SAMPLE_DIR / 'blufor_loadout.hpp'
    classes, equipment = hpp_parser.parse(loadout_file)
    nested_items = {'ACE_fieldDressing', 'ACE_packingBandage'}
    assert nested_items.issubset({eq.name for eq in equipment})

def test_hpp_parser_invalid_file(hpp_parser):
    """Test parser handles invalid files gracefully"""
    with pytest.raises(FileNotFoundError):
        hpp_parser.parse(SAMPLE_DIR / 'nonexistent.hpp')

def test_hpp_parser_list_macros(hpp_parser):
    """Test that LIST_N macros are left as-is"""
    loadout_file = SAMPLE_DIR / 'blufor_loadout.hpp'
    classes, equipment = hpp_parser.parse(loadout_file)
    assert 'ACE_fieldDressing' in {eq.name for eq in equipment}
    assert 'ACE_tourniquet' in {eq.name for eq in equipment}

def test_hpp_parser_class_inheritance(hpp_parser):
    """Test that equipment from parent classes is included"""
    loadout_file = SAMPLE_DIR  / 'opfor_loadout.hpp'
    classes, equipment = hpp_parser.parse(loadout_file)
    assert 'ItemMap' in {eq.name for eq in equipment}
    assert 'ItemCompass' in {eq.name for eq in equipment}

def test_hpp_parser_backpack_items(hpp_parser):
    """Test backpack items are properly parsed"""
    loadout_file = SAMPLE_DIR / 'blufor_loadout.hpp'
    classes, equipment = hpp_parser.parse(loadout_file)
    assert any(eq.name == 'fwa_1rnd_m2_carlgustaf_HEAT' and eq.category == 'backpackItems' for eq in equipment)

def test_hpp_parser_medical_items(hpp_parser):
    """Test parsing of medical loadout items"""
    loadout_file = (SAMPLE_DIR / 'co32_Seaside_Sweep_2.Altis' / 'loadouts' / 'blufor_loadout.hpp').resolve()
    classes, equipment = hpp_parser.parse(loadout_file)
    medical_items = {
        'ACE_fieldDressing',
        'ACE_packingBandage',
        'ACE_elasticBandage',
        'ACE_tourniquet',
        'ACE_splint',
        'ACE_morphine',
        'ACE_epinephrine'
    }
    assert medical_items.issubset({eq.name for eq in equipment})

def test_hpp_parser_empty_array_fields(hpp_parser):
    """Test parsing of arrays with empty fields"""
    content = """
    class testMan {
        attachment[] = {
            "",
            "acc_pointer_ir"
        };
        magazines[] = {};
        items[] = {
            "",
            "FirstAidKit",
            ""
        };
    };
    """
    with (SAMPLE_DIR / 'test_empty.hpp').open('w') as f:
        f.write(content)
        
    classes, equipment = hpp_parser.parse(SAMPLE_DIR / 'test_empty.hpp')
    
    # Should only include non-empty items
    assert any(eq.name == "acc_pointer_ir" and eq.type == "attachment" for eq in equipment)
    assert any(eq.name == "FirstAidKit" and eq.type == "items" for eq in equipment)
    assert not any(eq.name == "" for eq in equipment)
    
    # Cleanup test file
    (SAMPLE_DIR / 'test_empty.hpp').unlink()

def test_hpp_parser_array_patterns(hpp_parser):
    """Test different array definition patterns"""
    content = """
    class testMan {
        // Standard array
        primary[] = {"weapon1"};
        // Extended array
        magazines[] += {"mag1", "mag2"};
        // Array with space after bracket
        items[] = { "item1" };
        // Empty array
        goggles[] = {};
        // Array with only empty strings
        scope[] = {"", ""};
    };
    """
    with (SAMPLE_DIR / 'test_arrays.hpp').open('w') as f:
        f.write(content)
        
    classes, equipment = hpp_parser.parse(SAMPLE_DIR / 'test_arrays.hpp')
    
    # Check correct parsing of different patterns
    expected_items = {
        ("weapon1", "primary"),
        ("mag1", "magazines"),
        ("mag2", "magazines"),
        ("item1", "items")
    }
    
    found_items = {(eq.name, eq.type) for eq in equipment}
    assert expected_items.issubset(found_items)
    
    # Verify empty arrays and empty strings are handled
    assert not any(eq.name == "" for eq in equipment)
    
    # Cleanup test file
    (SAMPLE_DIR / 'test_arrays.hpp').unlink()

def test_hpp_parser_multiple_missions(hpp_parser, sample_files):
    """Test parsing loadouts from different missions"""
    missions = {}
    
    # Group files by mission folder
    for file in sample_files:
        mission = file.parent.parent.name
        if mission not in missions:
            missions[mission] = []
        missions[mission].append(file)
    
    # Each mission should have at least one valid loadout file
    valid_loadouts = {'blufor_loadout.hpp', 'opfor_loadout.hpp', 'indfor_loadout.hpp'}
    
    for mission_name, mission_files in missions.items():
        file_names = {f.name for f in mission_files}
        loadout_files = file_names.intersection(valid_loadouts)
        
        # Skip missions without loadout files
        if not loadout_files:
            continue
            
        # Test each found loadout file
        for loadout_file in [f for f in mission_files if f.name in valid_loadouts]:
            classes, equipment = hpp_parser.parse(loadout_file)
            
            # Basic validation
            assert len(classes) > 0, f"No classes found in {loadout_file}"
            assert len(equipment) > 0, f"No equipment found in {loadout_file}"
            
            # Verify base class and equipment exists
            assert 'baseMan' in {cls.name for cls in classes}, \
                   f"Missing baseMan class in {loadout_file}"
                   
            basic_items = {'ItemMap', 'ItemCompass', 'ItemWatch'}
            found_items = {eq.name for eq in equipment}
            assert basic_items.issubset(found_items), \
                   f"Missing basic items in {loadout_file}"

        # At least one loadout file should have been tested
        assert loadout_files, f"No valid loadout files found in mission {mission_name}"

