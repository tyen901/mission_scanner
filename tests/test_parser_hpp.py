import pytest
from pathlib import Path
from mission_scanner.parsers import HPPParser
from mission_scanner.models import MissionClass, Equipment

SAMPLE_DIR = Path(__file__).parent / 'sample_data'

@pytest.fixture
def hpp_parser():
    """Create HPP parser instance"""
    return HPPParser()

def test_hpp_parser_blufor_complete(hpp_parser):
    """Test parsing complete blufor loadout file"""
    loadout_file = SAMPLE_DIR / 'blufor_loadout.hpp'
    classes, equipment = hpp_parser.parse(loadout_file)
    assert len(classes) > 0
    assert len(equipment) > 0

def test_hpp_parser_carlgustaf_ammo(hpp_parser):
    """Test parsing of backpackItems arrays"""
    loadout_file = SAMPLE_DIR / 'blufor_loadout.hpp'
    classes, equipment = hpp_parser.parse(loadout_file)
    assert any(eq.name == 'fwa_1rnd_m2_carlgustaf_HEAT' and eq.category == 'backpackItems' for eq in equipment)

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
    loadout_file = SAMPLE_DIR / 'blufor_loadout.hpp'
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

def test_hpp_parser_all_classes(hpp_parser):
    """Test that all classes are extracted from loadout file"""
    loadout_file = SAMPLE_DIR / 'blufor_loadout.hpp'
    classes, _ = hpp_parser.parse(loadout_file)
    
    # Classes actually defined in blufor_loadout.hpp
    expected_classes = {
        'baseMan',    # Base class
        'rm',        # Rifleman
        'ar',        # Automatic Rifleman
        'aar',       # Assistant Automatic Rifleman
        'rm_lat',    # Rifleman (LAT)
        'sh',        # Sharpshooter
        'gren',      # Grenadier
        'tl',        # Team Leader
        'sl',        # Squad Leader
        'sgt',       # Sergeant
        'co',        # Platoon Commander
        'rm_fa',     # Rifleman (First-Aid)
        'cls',       # Combat Life Saver
        'mmg',       # Medium Machine Gunner
        'ammg',      # Assistant Medium Machine Gunner
        'drone'      # Drone Operator
    }
    
    found_classes = {cls.name for cls in classes}
    assert found_classes == expected_classes, \
           f"Missing classes: {expected_classes - found_classes}"

