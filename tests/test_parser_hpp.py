import pytest
from pathlib import Path
from mission_scanner.parsers import HppParser

@pytest.fixture
def loadout_path(request):
    return Path(__file__).parent / "sample_data" / "example_loadout.hpp"

@pytest.fixture
def hpp_parser():
    return HppParser()

def test_parse_base_class(loadout_path, hpp_parser):
    result = hpp_parser.parse(loadout_path)
    assert "baseMan" in result.classes
    base_man = result.classes["baseMan"]
    
    # Check basic properties
    assert base_man.name == "baseMan"
    assert base_man.properties["displayName"].value == "Unarmed"
    
    # Check empty arrays
    assert base_man.properties["uniform"].array_values == []  # Changed: use array_values instead of value
    assert base_man.properties["vest"].array_values == []     # Changed: use array_values instead of value
    
    # Check non-empty arrays
    linked_items = base_man.properties["linkedItems"].array_values  # Changed: use array_values
    assert len(linked_items) == 3
    assert "ItemWatch" in linked_items
    assert "ItemMap" in linked_items
    assert "ItemCompass" in linked_items

def test_parse_inheritance(loadout_path, hpp_parser):
    result = hpp_parser.parse(loadout_path)
    
    # Test rifleman inherits from baseMan
    assert "rm" in result.classes
    rm_class = result.classes["rm"]
    assert rm_class.parent == "baseMan"
    
    # Test squad leader inherits from team leader
    assert "sl" in result.classes
    sl_class = result.classes["sl"]
    assert sl_class.parent == "tl"

def test_parse_arrays(loadout_path, hpp_parser):
    result = hpp_parser.parse(loadout_path)
    rm_class = result.classes["rm"]
    
    # Test uniform array with LIST_1 macros
    uniforms = rm_class.properties["uniform"].array_values  # Changed: use array_values
    assert len(uniforms) == 10
    assert "U_BG_Guerrilla_6_1" in uniforms
    
    # Test magazines array with LIST_n macros
    magazines = rm_class.properties["magazines"].array_values  # Changed: use array_values
    assert "SmokeShell" in magazines
    assert "rhs_mag_m67" in magazines
    assert "pca_mag_30Rnd_556x45_M855A1_PMAG_Blk" in magazines

def test_parse_medic_class(loadout_path, hpp_parser):
    result = hpp_parser.parse(loadout_path)
    
    # Test CLS class properties
    assert "cls" in result.classes
    cls_class = result.classes["cls"]
    assert cls_class.parent == "rm_fa"
    
    # Verify medical supplies in backpackItems
    backpack_items = cls_class.properties["backpackItems"].value
    assert "ACE_surgicalKit" in backpack_items
    assert "ACE_personalAidKit" in backpack_items
