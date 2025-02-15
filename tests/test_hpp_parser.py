import pytest
from pathlib import Path
from mission_scanner.parsers import HppParser
from class_scanner.models import PropertyValue

@pytest.fixture
def hpp_parser():
    return HppParser()

@pytest.fixture
def sample_base_man_class(sample_data_path):
    """Get path to a file containing the baseMan class"""
    return sample_data_path / 'loadouts' / 'blufor_loadout.hpp'

def test_hpp_parser_loads(hpp_parser, sample_base_man_class):
    """Test that parser loads and parses files correctly"""
    classes, equipment = hpp_parser.parse(sample_base_man_class)
    assert len(classes) > 0
    
    # Test base class was found
    base_man = next((c for c in classes if c.name == "baseMan"), None)
    assert base_man is not None
    assert isinstance(base_man.properties.get('linkedItems'), PropertyValue)

def test_hpp_parser_equipment_arrays(hpp_parser, sample_base_man_class):
    """Test parsing of equipment array properties"""
    _, equipment = hpp_parser.parse(sample_base_man_class)
    
    # Check basic equipment items
    items = {e.name for e in equipment if e.category == 'items'}
    assert 'ACE_fieldDressing' in items
    assert 'ACE_morphine' in items
    
    # Check linked items
    linked = {e.name for e in equipment if e.category == 'linkedItems'}
    assert 'ItemMap' in linked
    assert 'ItemCompass' in linked

def test_hpp_parser_class_inheritance(hpp_parser, sample_base_man_class):
    """Test that class inheritance is correctly tracked"""
    classes, _ = hpp_parser.parse(sample_base_man_class)
    
    # Find rifleman class
    rifleman = next((c for c in classes if c.name == "rm"), None)
    assert rifleman is not None
    assert rifleman.parent == "baseMan"
    
    # Check inherited and overridden properties
    assert isinstance(rifleman.properties.get('uniform'), PropertyValue)
    assert rifleman.properties['uniform'].is_array

def test_hpp_parser_property_values(hpp_parser, sample_base_man_class):
    """Test that property values are correctly parsed"""
    classes, _ = hpp_parser.parse(sample_base_man_class)
    base_man = next(c for c in classes if c.name == "baseMan")
    
    # Test string property
    display_name = base_man.properties.get('displayName')
    assert isinstance(display_name, PropertyValue)
    assert display_name.value == "Unarmed"
    
    # Test array property
    linked_items = base_man.properties.get('linkedItems')
    assert isinstance(linked_items, PropertyValue)
    assert linked_items.is_array
    assert "ItemWatch" in linked_items.array_values

def test_hpp_parser_equipment_categories(hpp_parser, sample_base_man_class):
    """Test that equipment categories are correctly assigned"""
    _, equipment = hpp_parser.parse(sample_base_man_class)
    
    categories = {e.category for e in equipment}
    expected_categories = {'magazines', 'items', 'linkedItems', 'weapons'}
    assert categories.intersection(expected_categories)
    
    # Test specific equipment items have correct categories
    for item in equipment:
        if 'ACRE_' in item.name or 'ACE_' in item.name:
            assert item.category == 'items'
        elif item.name.endswith('_mag'):
            assert item.category == 'magazines'

def test_hpp_parser_handles_errors(hpp_parser):
    """Test parser error handling"""
    with pytest.raises(FileNotFoundError):
        hpp_parser.parse(Path('nonexistent.hpp'))
    
    # Test with invalid file content
    invalid_file = Path('test.hpp')
    invalid_file.write_text('invalid { content')
    try:
        classes, equipment = hpp_parser.parse(invalid_file)
        assert len(classes) == 0
        assert len(equipment) == 0
    finally:
        invalid_file.unlink()

@pytest.mark.parametrize('class_name,expected_items', [
    ('rm', ['ACRE_PRC343', 'ACE_fieldDressing']),
    ('ar', ['sps_200Rnd_556x45_M855A1_Mixed_KAC_Box']),
    ('cls', ['ACE_surgicalKit', 'ACE_bloodIV'])
])
def test_hpp_parser_class_specific_equipment(hpp_parser, sample_base_man_class, class_name, expected_items):
    """Test that class-specific equipment is correctly parsed"""
    _, equipment = hpp_parser.parse(sample_base_man_class)
    
    # Get all equipment names for the items category
    items = {e.name for e in equipment}
    
    # Check that expected items are present
    for item in expected_items:
        assert item in items

