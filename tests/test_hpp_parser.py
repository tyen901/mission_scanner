import pytest
from pathlib import Path
from mission_scanner.parsers import HppParser
from class_scanner.models import PropertyValue

from tests.conftest import EXAMPLE_LOADOUT

@pytest.fixture
def hpp_parser():
    return HppParser()

@pytest.fixture
def sample_loadout():
    return EXAMPLE_LOADOUT

def test_hpp_parser_loads(hpp_parser, sample_loadout):
    """Test that parser loads and parses files correctly"""
    result = hpp_parser.parse(sample_loadout)
    assert len(result.classes) > 0
    
    # Test base class was found
    base_man = next((c for c in result.classes.values() if c.name == "baseMan"), None)
    assert base_man is not None
    assert isinstance(base_man.properties.get('linkedItems'), PropertyValue)

def test_hpp_parser_equipment_arrays(hpp_parser, sample_loadout):
    """Test parsing of equipment array properties"""
    result = hpp_parser.parse(sample_loadout)
    
    # Check basic equipment items
    items = {e.name for e in result.equipment if e.category == 'items'}
    assert 'ACE_fieldDressing' in items
    assert 'ACE_morphine' in items
    
    # Check linked items
    linked = {e.name for e in result.equipment if e.category == 'linkedItems'}
    assert 'ItemMap' in linked
    assert 'ItemCompass' in linked

def test_hpp_parser_class_inheritance(hpp_parser, sample_loadout):
    """Test that class inheritance is correctly tracked"""
    result = hpp_parser.parse(sample_loadout)
    
    # Find rifleman class
    rifleman = next((c for c in result.classes.values() if c.name == "rm"), None)
    assert rifleman is not None
    assert rifleman.parent == "baseMan"
    
    # Check inherited and overridden properties
    assert isinstance(rifleman.properties.get('uniform'), PropertyValue)
    assert rifleman.properties['uniform'].is_array

def test_hpp_parser_property_values(hpp_parser, sample_loadout):
    """Test that property values are correctly parsed"""
    result = hpp_parser.parse(sample_loadout)
    base_man = next(c for c in result.classes.values() if c.name == "baseMan")
    
    # Test string property
    display_name = base_man.properties.get('displayName')
    assert isinstance(display_name, PropertyValue)
    assert display_name.value == "Unarmed"
    
    # Test array property
    linked_items = base_man.properties.get('linkedItems')
    assert isinstance(linked_items, PropertyValue)
    assert linked_items.is_array
    assert "ItemWatch" in linked_items.array_values


def test_hpp_parser_handles_errors(hpp_parser):
    """Test parser error handling"""
    with pytest.raises(FileNotFoundError):
        hpp_parser.parse(Path('nonexistent.hpp'))
    
    # Test with invalid file content
    invalid_file = Path('test.hpp')
    invalid_file.write_text('invalid { content')
    try:
        result = hpp_parser.parse(invalid_file)
        assert len(result.classes) == 0
        assert len(result.equipment) == 0
    finally:
        invalid_file.unlink()

@pytest.mark.parametrize('class_name,expected_items', [
    ('rm', ['ACRE_PRC343', 'ACE_fieldDressing']),
    ('ar', ['sps_200Rnd_556x45_M855A1_Mixed_KAC_Box']),
    ('cls', ['ACE_surgicalKit', 'ACE_bloodIV'])
])
def test_hpp_parser_class_specific_equipment(hpp_parser, sample_loadout, class_name, expected_items):
    """Test that class-specific equipment is correctly parsed"""
    result = hpp_parser.parse(sample_loadout)
    
    # Get all equipment names for the items category
    items = {e.name for e in result.equipment}
    
    # Check that expected items are present
    for item in expected_items:
        assert item in items

