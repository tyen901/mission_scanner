import pytest
import logging
from pathlib import Path
from mission_scanner.parsers import SqmParser

# Setup debug logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@pytest.fixture
def mission_path(request):
    return Path(__file__).parent / "sample_data" / "example_mission.sqm"

@pytest.fixture
def sqm_parser():
    return SqmParser()

def test_parse_basic_equipment(mission_path, sqm_parser):
    """Test parsing of basic equipment items"""
    result = sqm_parser.parse(mission_path)
    equipment = result.equipment
    
    # Debug output
    logger.debug("Found equipment items:")
    for item in equipment:
        logger.debug(f"- {item.name} (type: {item.type}, category: {item.category})")
    
    # Check basic equipment items
    basic_items = {item.name for item in equipment if item.category in ['map', 'compass', 'watch']}
    logger.debug(f"Basic items found: {basic_items}")
    
    assert "ItemMap" in basic_items, f"ItemMap not found in basic items: {basic_items}"
    assert "ItemCompass" in basic_items, f"ItemCompass not found in basic items: {basic_items}"
    assert "ItemWatch" in basic_items, f"ItemWatch not found in basic items: {basic_items}"

def test_parse_primary_weapon(mission_path, sqm_parser):
    """Test parsing of primary weapon and attachments"""
    result = sqm_parser.parse(mission_path)
    equipment = result.equipment
    
    # Debug output
    logger.debug("Found weapons and attachments:")
    for item in equipment:
        if item.type == "weapon" or item.category == "optics":
            logger.debug(f"- {item.name} (type: {item.type}, category: {item.category})")
    
    # Check primary weapon
    weapons = {item.name for item in equipment if item.type == "weapon"}
    logger.debug(f"Weapons found: {weapons}")
    
    assert "CUP_srifle_LeeEnfield" in weapons, f"LeeEnfield not found in weapons: {weapons}"
    assert "rhs_weap_mg42" in weapons, f"MG42 not found in weapons: {weapons}"
    
    # Check optics
    optics = {item.name for item in equipment if item.category == "optics"}
    logger.debug(f"Optics found: {optics}")
    
    assert "CUP_optic_no23mk2" in optics, f"no23mk2 optic not found in optics: {optics}"

def test_parse_containers(mission_path, sqm_parser):
    """Test parsing of uniform, vest, and backpack"""
    result = sqm_parser.parse(mission_path)
    equipment = result.equipment
    
    # Debug output
    logger.debug("Found containers:")
    for item in equipment:
        if item.category in ['uniform', 'vest', 'backpack']:
            logger.debug(f"- {item.name} (type: {item.type}, category: {item.category})")
    
    containers = {item.name for item in equipment if item.category in ['uniform', 'vest', 'backpack']}
    logger.debug(f"Containers found: {containers}")
    
    assert "TC_U_aegis_guerilla_garb_m81_sudan" in containers, f"Uniform not found in containers: {containers}"
    assert "simc_vest_pasgt_lc2_alt_od3" in containers, f"Vest not found in containers: {containers}"
    assert "pca_eagle_a3_od" in containers, f"Backpack not found in containers: {containers}"

def test_parse_magazines(mission_path, sqm_parser):
    """Test parsing of magazines from cargo"""
    result = sqm_parser.parse(mission_path)
    equipment = result.equipment
    
    # Debug output
    logger.debug("Found magazines:")
    for item in equipment:
        if item.type == "magazine":
            logger.debug(f"- {item.name} (type: {item.type}, category: {item.category})")
    
    magazines = {item.name for item in equipment if item.type == "magazine"}
    logger.debug(f"Magazines found: {magazines}")
    
    assert "CUP_10x_303_M" in magazines, f"303 magazine not found in magazines: {magazines}"
    assert "SmokeShell" in magazines, f"Smoke grenade not found in magazines: {magazines}"
    assert "rhs_mag_m67" in magazines, f"Frag grenade not found in magazines: {magazines}"

def test_parse_inventory_items(mission_path, sqm_parser):
    """Test parsing of inventory items"""
    result = sqm_parser.parse(mission_path)
    equipment = result.equipment
    
    # Debug output
    logger.debug("Found inventory items:")
    for item in equipment:
        if item.type == "item":
            logger.debug(f"- {item.name} (type: {item.type}, category: {item.category})")
    
    items = {item.name for item in equipment if item.type == "item"}
    logger.debug(f"Items found: {items}")
    
    # Check medical items with detailed output
    medical_items = {"ACE_fieldDressing", "ACE_tourniquet", "ACE_morphine"}
    found_medical = medical_items.intersection(items)
    missing_medical = medical_items - items
    
    logger.debug(f"Medical items found: {found_medical}")
    logger.debug(f"Medical items missing: {missing_medical}")
    
    assert "ACE_fieldDressing" in items, f"Field dressing not found in items: {items}"
    assert "ACE_tourniquet" in items, f"Tourniquet not found in items: {items}"
    assert "ACE_morphine" in items, f"Morphine not found in items: {items}"
    
    # Check other equipment
    assert "ACRE_BF888S" in items, f"Radio not found in items: {items}"
