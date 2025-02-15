from pathlib import Path
from mission_scanner.parsers.sqf_parser import SqfParser
from .conftest import EXAMPLE_CURATED_ARSENAL, EXAMPLE_CURATED_ARSENAL_EXPECTED_ITEMS, EXAMPLE_CURATED_GEAR_FILE, EXAMPLE_CURATED_GEAR_EXPECTED_DATA, EXAMPLE_MISSION_EXPECTED_ITEMS, EXAMPLE_MISSION_FILE, EXAMPLE_BRIEFING_FILE
import logging

logger = logging.getLogger(__name__)

def test_parse_curated_gear():
    parser = SqfParser()
    result = parser.parse(EXAMPLE_CURATED_GEAR_FILE)
    found_items = {eq.name for eq in result.equipment}

    expected_items = EXAMPLE_CURATED_GEAR_EXPECTED_DATA

    assert expected_items.issubset(found_items), f"Missing items: {expected_items - found_items}"


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


def test_parse_equipment_additions_type_a():
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

def test_parse_equipment_additions_type_b():
    parser = SqfParser()
    test_content = '''
        _unit linkItem "ItemMap";
        _unit addWeaponItem ["rhs_weap_m4a1", "rhsusf_acc_acog", true];
    '''

    path = Path("test.sqf")
    with open(path, "w") as f:
        f.write(test_content)

    result = parser.parse(path)

    expected_items = {
        "rhs_weap_m4a1",
        "ItemMap",
        "rhsusf_acc_acog"
    }

    found_items = {eq.name for eq in result.equipment}
    assert found_items == expected_items

    path.unlink()


def test_parse_equipment_additions_type_c():
    parser = SqfParser()
    test_content = '''
        _unit addWeapon "rhs_weap_m4a1";
        _unit addWeaponItem ["rhs_weap_m4a2", "rhsusf_acc_acog", true];
    '''

    path = Path("test.sqf")
    with open(path, "w") as f:
        f.write(test_content)

    result = parser.parse(path)

    expected_items = {
        "rhs_weap_m4a1",
        "rhs_weap_m4a2",
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


def test_parse_briefing():
    """Test parsing briefing file which should not contain any equipment"""
    parser = SqfParser()
    result = parser.parse(EXAMPLE_BRIEFING_FILE)
    assert len(result.equipment) == 0, "Briefing file should not contain any equipment"
    assert len(result.classes) == 0, "Briefing file should not contain any classes"


def test_parse_settings():
    """Test that settings aren't parsed as equipment"""
    parser = SqfParser()
    test_content = '''
// LAMBS Danger WP
force lambs_wp_autoAddArtillery = false;

// LAMBS Main
force lambs_main_combatShareRange = 200;
force lambs_main_debug_drawAllUnitsInVehicles = false;
force lambs_main_debug_Drawing = false;
force lambs_main_debug_FSM = false;
force lambs_main_debug_FSM_civ = false;
force lambs_main_debug_functions = false;
force lambs_main_debug_RenderExpectedDestination = false;
force lambs_main_disableAICallouts = true;
force lambs_main_disableAIDodge = true;
force lambs_main_disableAIFleeing = true;
force lambs_main_disableAIGestures = true;
// DUI - Squad Radar - Main
diwako_dui_ace_hide_interaction = true;
diwako_dui_colors = "standard";
diwako_dui_font = "RobotoCondensed";
diwako_dui_icon_style = "standard";
diwako_dui_main_hide_dialog = true;
diwako_dui_main_hide_ui_by_default = false;
diwako_dui_main_squadBlue = [0,0,1,1];
diwako_dui_main_squadGreen = [0,1,0,1];
diwako_dui_main_squadMain = [1,1,1,1];
diwako_dui_main_squadRed = [1,0,0,1];
diwako_dui_main_squadYellow = [1,1,0,1];
diwako_dui_main_trackingColor = [0.93,0.26,0.93,1];
diwako_dui_reset_ui_pos = false;
zen_compat_ace_hideModules = false;
zen_context_menu_enabled = 2;
zen_editor_addGroupIcons = false;
zen_editor_declutterEmptyTree = true;
zen_editor_disableLiveSearch = false;
zen_editor_moveDisplayToEdge = true;
force zen_editor_parachuteSounds = true;
zen_editor_previews_enabled = true;
    '''

    path = Path("test.sqf") 
    with open(path, "w") as f:
        f.write(test_content)

    result = parser.parse(path)
    assert len(result.equipment) == 0, "CBA settings should not be parsed as equipment"
    
    path.unlink()


def test_parse_script_parameters():
    """Test that script parameters aren't parsed as equipment"""
    parser = SqfParser()
    test_content = '''
        //Set up default parameters
        _lives = -1;
        _cacheRadius = 0;
        _reduceRadius = 0;
        _pauseRadius = 0;
        _respawnDelay = 30;
        _initialDelay = 0;
        _guard = false;
        _special = "NONE";
        _respawnMarkers = [];
        _initString = "";
        _debug = false;
    '''

    path = Path("test.sqf") 
    with open(path, "w") as f:
        f.write(test_content)

    result = parser.parse(path)
    print (result.equipment)
    assert len(result.equipment) == 0, "Script parameters should not be parsed as equipment"
    
    path.unlink()


def test_parse_mixed_script():
    """Test parsing Jebus script file which should not treat parameters as equipment"""
    parser = SqfParser()
    test_content = '''
        params ["_unit"];
        private [
            "_unit",
            "_cacheRadius",
            "_debug",
            "_exitTrigger",
            "_firstLoop",
            "_initString",
            "_initialDelay",
            "_lives",
            "_newGroup"
        ];
        
        _lives = -1;
        _cacheRadius = 0;
        _reduceRadius = 0;
        _pauseRadius = 0;
        _respawnDelay = 30;
        _initialDelay = 0;
        _guard = false;
        _special = "NONE";
        _respawnMarkers = [];
        _initString = "";
        _debug = false;

        // But should still detect equipment
        _unit addWeapon "real_weapon_classname";
        _unit addMagazine "real_magazine_classname";
    '''

    path = Path("test.sqf")
    with open(path, "w") as f:
        f.write(test_content)

    result = parser.parse(path)
    
    # Should find real equipment
    assert "real_weapon_classname" in {eq.name for eq in result.equipment}
    assert "real_magazine_classname" in {eq.name for eq in result.equipment}
    
    # Should not have script parameters
    assert not any(name in {eq.name for eq in result.equipment} 
                  for name in ["NONE", "-1", "0", "30", "false"])
    
    path.unlink()


def test_formatting_issues():
    parser = SqfParser()
    test_content = '''
private _itemMod =
[	
	//Optics
	"rhsusf_acc_eotech_552",
	"rhsusf_acc_compm4",
	//Muzzle Devices
	
	
	//Bipod & Foregrips
		"rhsusf_acc_grip1",
		"rhsusf_acc_grip2",
		"rhsusf_acc_grip3",
		"rhsusf_acc_grip4",
		"rhsusf_acc_grip4_bipod",
		"rhsusf_acc_saw_lw_bipod"
	
	//Tactical Devices
];
    '''
    
    path = Path("test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
        
    result = parser.parse(path)
    assert len(result.equipment) == 8, "Should parse 8 items"

def test_edge_cases_A(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
//Match unitrole name with the classnames in loadout.
[arsenal, (_itemEquipment + _itemMod + _itemLAT + _itemWeaponRifle + _itemWeaponAmmo)] call ace_arsenal_fnc_initBox;

_action = 
[
    "personal_arsenal","Personal Arsenal","\\A3\\ui_f\\data\\igui\\cfg\\weaponicons\\MG_ca.paa",
    {
        [arsenal, _player] call ace_arsenal_fnc_openBox
    },
    { 
        (player distance2d (player getVariable ["startpos",[0,0,0]])) < 200
    },
    {},
    [],
    [0,0,0],
    3
] call ace_interact_menu_fnc_createAction;
'''

    path = Path(tmp_path / "test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
        
    result = parser.parse(path)
    print (result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"
    
    
def test_edge_cases_B(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
_action = 
[
    "personal_arsenal","Personal Arsenal","\\A3\\ui_f\\data\\igui\\cfg\\weaponicons\\MG_ca.paa",
    {
        [arsenal, _player] call ace_arsenal_fnc_openBox
    },
    { 
        (player distance2d (player getVariable ["startpos",[0,0,0]])) < 200
    },
    {},
    [],
    [0,0,0],
    3
] call ace_interact_menu_fnc_createAction;
'''

    path = Path(tmp_path / "test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
        
    result = parser.parse(path)
    print (result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"
 
    
def test_edge_cases_C(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
//Get parameters
for "_parameterIndex" from 1 to (count _this - 1) do 
{
	switch (_this select _parameterIndex) do 
	{
		case "LIVES=" : {_lives = _this select (_parameterIndex + 1)};
		case "DELAY=" : {_respawnDelay =  _this select (_parameterIndex + 1)};
		case "START=" : {_initialDelay = _this select (_parameterIndex + 1)};
		case "CACHE=" : {_cacheRadius =  _this select (_parameterIndex + 1)};
		case "REDUCE=" : {_reduceRadius =  _this select (_parameterIndex + 1)};
		case "GUARD" : {_guard = true};
		case "FLYING" : {_special = "FLY"};
		case "RESPAWNMARKERS=" : {_respawnMarkers = _this select (_parameterIndex + 1)};
		case "PAUSE=" : {_pauseRadius = _this select (_parameterIndex + 1)};
		case "EXIT=" : {_exitTrigger = _this select (_parameterIndex + 1)};
		case "INIT=" : {_initString = _this select (_parameterIndex + 1)};
		case "DEBUG" : {_debug = true};
	};
};
'''

    path = Path(tmp_path / "test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
        
    result = parser.parse(path)
    print (result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"


def test_edge_cases_D(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
    while {{alive _x} count (units _group) > 0} do 
{
	sleep 10;
	
	if ([getPos (leader _group), _radius] call jebus_fnc_playerInRadius) then 
	{
		if (_group getVariable "IsCached") then 
		{
			if (_debug) then {systemChat format["%1 - Uncaching group.", _group]};
			{
				(vehicle _x) hideObjectGlobal false;
				_x enableSimulationGlobal true;
			} forEach units _group;
			
			_group setVariable ["IsCached", false];
		};
	} 
	else 
	{
		if (!(_group getVariable "IsCached")) then 
		{
			if (_debug) then {systemChat format["%1 - Caching group.", _group]};
			{
				(vehicle _x) hideObjectGlobal true;
				_x enableSimulationGlobal false;
			} forEach units _group;
			
			_group setVariable ["IsCached", true];
		};
	};
};
'''
    path = Path(tmp_path / "test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
        
    result = parser.parse(path)
    print (result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"
    
    
def test_edge_cases_E(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
private _response = 
[
	"
		Welcome to the Mission! 
		<br/><br/>
		You can use the 'TELEPORT TO GROUP' action in your ACE self interaction menu to teleport to your group. 
		<br/><br/>
		The action will disappear once 10 minutes has passed since you've joined or moving too far away from the spawn area.
	", "JIP TELEPORT AVAILABLE", true, false
] call BIS_fnc_guiMessage;
'''
    path = Path(tmp_path / "test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
        
    result = parser.parse(path)
    print (result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"
    
    
def test_edge_cases_F(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
private _jipActionCode = 
{
	private _target = [] call pca_fnc_jipChooseTarget;
	private _vehSpot = [_target] call pca_fnc_jipEmptySeat;
	
	if (!_vehSpot && {speed _target > 19 || {(getPosATL _target) select 2 > 5}}) exitWith 
	{
		private _title1 = "<t color = '#FFBA26' size='1'>CAN NOT TELEPORT!</t><br/>";
		private _title2 = "<t color = '#FFFFFF' size='1'>Teleport target moving too fast or currently in air. Try again in a little bit!</t><br/>";
		[_title1 + _title2, 2, player, 14] call ace_common_fnc_displayTextStructured;
	};
	
	player allowDamage false;
	
	cutText ["", "BLACKOUT", 1, true];
	
	if (_vehSpot) then 
	{
		player moveInAny vehicle _target;
	}
	else
	{
		player setPosATL (_target getPos [3, getDir _target - 180]);
	};
	
	cutText ["", "BLACK IN", 1, true];
	player allowDamage true;
};
'''
    path = Path(tmp_path / "test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
        
    result = parser.parse(path)
    print (result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"


def test_edge_cases_G(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
//0 = player execVM "loadouts\arsenal.sqf";

"ColorCorrections" ppEffectEnable true;
"ColorCorrections" ppEffectAdjust 
[
	1.04, 
	1.02, 
	-0.02, 
	[0.1, 0.4, 0.4, 0.04], 
	[1, 1, 1, 1.04], 
	[0.299, 0.587, 0.114, 0]
];
"ColorCorrections" ppEffectCommit 0;
'''
    path = Path(tmp_path / "test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
        
    result = parser.parse(path)
    print (result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"


def test_edge_cases_H(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
private 
[
	"_unit",
	"_cacheRadius",
	"_debug",
	"_exitTrigger",
	"_firstLoop",
	"_initString",
	"_initialDelay",
    "_lives",
	"_newGroup",
	"_pauseRadius",
	"_reduceRadius",
	"_respawnDelay",
	"_respawnMarkers",
	"_respawnPos",
	"_special",
	"_tmpRespawnPos",
	"_tmpZone",
	"_trigger",
	"_unitSide",
	"_synchronizedObjectsList"
];
'''
    path = Path(tmp_path / "test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
        
    result = parser.parse(path)
    print (result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"


def test_edge_cases_I(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
if (_overwatch isEqualTo []) then 
{
	private _distance2D = ((_unit distance2D _target) * 0.66) min 250;
	_overwatch = selectBestPlaces [_target, _distance2D, "(2*hills) + (2*forest+trees+houses) - (2*meadow) - (2*windy) - (2*sea) - (10*deadBody)", 100, 3] apply {[(_x select 0) distance2D _unit, _x select 0]};
	_overwatch = _overwatch select {!(surfaceIsWater (_x select 1))};
	_overwatch sort true;
	_overwatch = _overwatch apply {_x select 1};
	
	if (_overwatch isEqualTo []) then 
	{
		_overwatch pushBack ([getPos _unit, _distance2D, 100, 8, _target] call pca_fnc_findOverwatch);
	};
	
	_overwatch = _overwatch select 0;
};'''
    path = Path(tmp_path / "test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
    
    result = parser.parse(path)
    print (result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"

            
def test_edge_cases_J(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
_unit setVariable ["ace_medical_damageThreshold", (random [0.8, 1.2, 1.5]), true];
_unit setVariable ["BIS_enableRandomization", false];
'''
    path = Path(tmp_path / "test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
        
    result = parser.parse(path)
    print (result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"


def test_edge_cases_K(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
private _facewearPoolWeighted = selectRandomWeighted 
[
	"", 4,
	"", 1
];
'''
    path = Path(tmp_path / "test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
        
    result = parser.parse(path)
    print (result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"


def test_edge_cases_L(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
switch (true) do 
{
	//Rifleman
	case (_unitRole == "rm") : 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemAcc + _itemWeapRifle + _itemAmmo + _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
	//Rifleman (LAT)
	case (_unitRole == "rm_lat") : 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemAcc + _itemWeapRifle + _itemWeapLAT + _itemAmmo + _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
	//Automatic Rifle
	case (_unitRole == "ar") : 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemAcc + _itemWeapAR + _itemWeapPistol + _itemAmmoAR + _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
'''
    path = Path(tmp_path / "test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
        
    result = parser.parse(path)
    print (result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"

 
def test_edge_cases_M(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
else
{
	if (_backpackChance > random 100) then 
	{
		_unit addBackpack _backpackPoolWeighted;
	};
};'''
    path = Path(tmp_path / "test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
    
    result = parser.parse(path)
    print (result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"
    
def test_edge_cases_N(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
/**
 * Launch the tool helping to edit the logistics configuration.
 * 
 * THIS TOOL IS UNOFFICIAL AND FOR EXPERT ONLY !
 * READ THE PDF DOCUMENTATION TO KNOW HOW TO USE IT !
 * 
 * @usage Don't forget to fill the list of class names to configure in list_of_objects_to_config.sqf.
 * @usage execVM "R3F_LOG\addons_config\logistics_config_maker_tool\launch_config_tool.sqf";
 * 
 * Copyright (C) 2014 Team ~R3F~
 * 
 * This program is free software under the terms of the GNU General Public License version 3.
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
TAB_class_names_to_config = [
	#include "list_of_objects_to_config.sqf"
];
'''
    path = Path(tmp_path / "test.sqf")
    with open(path
                , "w") as f:
            f.write(test_content)
            
    result = parser.parse(path)
    logger.debug(result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"

 
def test_edge_cases_O(tmp_path : Path):
    parser = SqfParser()
    test_content = '''
player addAction ["Dump config to RPT", "R3F_LOG\addons_config\logistics_config_maker_tool\dump_config.sqf"];
player addAction ["Set new spawn position", {R3F_LOG_spawn_position = player modelToWorld [0, 30, 0]; systemChat "New spawn position defined.";}];
player addEventHandler ["HandleDamage", {0}];
'''
    path = Path(tmp_path / "test.sqf")
    with open(path, "w") as f:
        f.write(test_content)
        
    result = parser.parse(path)
    logger.debug(result.equipment)
    assert len(result.equipment) == 0, "Should not parse equipment from script"