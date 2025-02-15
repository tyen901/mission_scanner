from pathlib import Path
from mission_scanner.parsers.sqf_parser import SqfParser
from .conftest import EXAMPLE_CURATED_ARSENAL, EXAMPLE_CURATED_ARSENAL_EXPECTED_ITEMS, EXAMPLE_CURATED_GEAR_FILE, EXAMPLE_CURATED_GEAR_EXPECTED_DATA, EXAMPLE_MISSION_EXPECTED_ITEMS, EXAMPLE_MISSION_FILE, SAMPLE_DATA_FOLDER


def test_parse_curated_gear():
    parser = SqfParser()
    result = parser.parse(EXAMPLE_CURATED_GEAR_FILE)
    found_items = {eq.name for eq in result.equipment}

    expected_items = EXAMPLE_CURATED_GEAR_EXPECTED_DATA

    assert expected_items.issubset(found_items), f"Missing items: {expected_items - found_items}"

    head_items = {item for item in found_items if item.startswith('WhiteHead_')}
    assert not head_items, f"Found face references that should be filtered: {head_items}"


def test_parse_mission_inventory():
    """Test parsing equipment from mission.sqm inventory blocks"""
    parser = SqfParser()
    expected_items = EXAMPLE_MISSION_EXPECTED_ITEMS
    result = parser.parse(EXAMPLE_MISSION_FILE)
    found_items = {eq.name for eq in result.equipment}
    assert expected_items.issubset(found_items),  f"Missing items: {expected_items - found_items}"


def test_parse_curated_arsenal():
    """Test parsing equipment from curated arsenal definitions"""
    parser = SqfParser()
    result = parser.parse(EXAMPLE_CURATED_ARSENAL)
    found_items = {eq.name for eq in result.equipment}
    expected_items = EXAMPLE_CURATED_ARSENAL_EXPECTED_ITEMS

    assert expected_items.issubset(found_items), f"Missing items: {expected_items - found_items}"

    filtered_items = {
        'WhiteHead_01', 'WhiteHead_02',
        '$',
        ''
    }

    assert not (filtered_items & found_items), f"Found items that should be filtered: {filtered_items & found_items}"

    array_items = {
        "ACE_Clacker",
        "ACE_DefusalKit",
        "ACE_EntrenchingTool",
        "rhsusf_m112_mag",
        "MineDetector"
    }

    assert array_items.issubset(found_items), f"Missing array items: {array_items - found_items}"


def test_parse_equipment_assignments():
    parser = SqfParser()
    test_content = '''
        private _bp = "rhs_rpg_empty";
        private _mat = "rhs_weap_rpg7";
        private _matAT = "rhs_rpg7_PG7VL_mag";
    '''

    path = Path("test.sqf")
    with open(path, "w") as f:
        f.write(test_content)

    result = parser.parse(path)

    expected_items = {
        "rhs_rpg_empty",
        "rhs_weap_rpg7",
        "rhs_rpg7_PG7VL_mag"
    }

    found_items = {eq.name for eq in result.equipment}
    assert found_items == expected_items

    path.unlink()


def test_parse_equipment_additions():
    parser = SqfParser()
    test_content = '''
        for "_i" from 1 to 4 do {_unit addItemToUniform "ACE_fieldDressing";};
        _unit addWeapon "rhs_weap_m4a1";
        _unit addMagazine "rhs_mag_30Rnd_556x45_M855A1_Stanag";
        _unit addGoggles "G_Combat";
        _unit linkItem "ItemMap";
        _unit addWeaponItem ["rhs_weap_m4a1", "rhsusf_acc_acog", true];
    '''

    path = Path("test.sqf")
    with open(path, "w") as f:
        f.write(test_content)

    result = parser.parse(path)

    expected_items = {
        "ACE_fieldDressing",
        "rhs_weap_m4a1",
        "rhs_mag_30Rnd_556x45_M855A1_Stanag",
        "G_Combat",
        "ItemMap",
        "rhsusf_acc_acog"
    }

    found_items = {eq.name for eq in result.equipment}
    assert found_items == expected_items

    path.unlink()


def test_parse_mixed_content():
    parser = SqfParser()
    test_content = '''
        private _uniform = "U_B_CombatUniform_mcam";
        _unit forceAddUniform _uniform;

        for "_i" from 1 to 3 do {
            _unit addItemToVest "FirstAidKit";
            _unit addMagazine "30Rnd_65x39_caseless_mag";
        };

        // Comment line
        _unit addBackpack "B_AssaultPack_mcamo";
    '''

    path = Path("test.sqf")
    with open(path, "w") as f:
        f.write(test_content)

    result = parser.parse(path)

    expected_items = {
        "U_B_CombatUniform_mcam",
        "FirstAidKit",
        "30Rnd_65x39_caseless_mag",
        "B_AssaultPack_mcamo"
    }

    found_items = {eq.name for eq in result.equipment}
    assert found_items == expected_items

    path.unlink()
