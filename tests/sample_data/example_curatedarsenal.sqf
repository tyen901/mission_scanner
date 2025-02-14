/**
	Adds a curated personal arsenal that can be accessed via ACE Self Interact by the players.
	
	Parameters:
	0: unit <OBJECT>
	
	UNIT MUST BE LOCAL
	
	Example:
	[player] call pca_fnc_curatedArsenal;
	
	Returns: 
	NONE
*/

params ["_unit"];

if !(hasInterface) exitWith {};

private _unitRole = _unit getVariable ["tmf_assignGear_role", nil];

arsenal = "building" createVehicleLocal [0,0,0];
_unit setVariable ["startPos", getPosASL _unit];

//********************************************************************************//
// Unit Equipment
//********************************************************************************//
//Common
private _itemGear = [];

//Uniform
private _itemUniform = 
[
	"U_BG_Guerrilla_6_1",
	"U_BG_Guerilla1_1",
	"U_BG_Guerilla2_2",
	"U_BG_Guerilla2_1",
	"U_BG_Guerilla2_3",
	"U_BG_leader",
	"rhsgref_uniform_TLA_1",
	"rhsgref_uniform_TLA_2",
	"aegis_guerilla_garb_m81",
	"aegis_guerilla_jacket_m81",
	"aegis_sweater_grn",
	"aegis_guerilla_tshirt_m81",
	"aegis_guerilla_tshirt_m81_alt",
	"aegis_merc_polo_blu",
	"aegis_merc_polo_camo",
	"aegis_merc_polo_m81",
	"aegis_merc_tshirt_blk"
];

private _itemUniformCrew = 
[];

private _itemUniformPilot = 
[];

//Vest
private _itemVest = 
[
	"milgp_v_mmac_assaulter_belt_rgr",
	"milgp_v_mmac_assaulter_belt_cb",
	"milgp_v_mmac_assaulter_belt_mc",
	"milgp_v_mmac_assaulter_belt_khk",
	"milgp_v_mmac_hgunner_belt_rgr",
	"milgp_v_mmac_hgunner_belt_cb",
	"milgp_v_mmac_hgunner_belt_mc",
	"milgp_v_mmac_hgunner_belt_khk",
	"milgp_v_mmac_medic_belt_rgr",
	"milgp_v_mmac_medic_belt_cb",
	"milgp_v_mmac_medic_belt_mc",
	"milgp_v_mmac_medic_belt_khk",
	"milgp_v_mmac_teamleader_belt_rgr",
	"milgp_v_mmac_teamleader_belt_cb",
	"milgp_v_mmac_teamleader_belt_mc",
	"milgp_v_mmac_teamleader_belt_khk"
	
];

private _itemVestCrew = 
[];

private _itemVestPilot = 
[];

//Headgear 
private _itemHeadgear = 
[
	"pca_headband_blk",
	"pca_headband",
	"pca_headband_red",
	"pca_headband_tan",
	"H_Bandanna_gry",
	"H_Bandanna_blu",
	"H_Bandanna_cbr",
	"H_Bandanna_khk_hs",
	"H_Bandanna_khk",
	"H_Beret_blk",
	"H_Booniehat_khk",
	"H_Booniehat_oli",
	"H_Booniehat_tan",
	
	"H_Shemag_olive",
	"H_ShemagOpen_tan",
	"H_ShemagOpen_khk",
	"aegis_boonie_blk",
	"CUP_H_FR_BandanaGreen",
	"milgp_h_cap_01_cb",
	"milgp_h_cap_01_gry",
	"milgp_h_cap_01_khk",
	"milgp_h_cap_01_tan",
	"milgp_h_cap_backwards_01_cb",
	"milgp_h_cap_backwards_01_gry",
	"milgp_h_cap_backwards_01_khk",
	"milgp_h_cap_backwards_01_tan",
	"rhs_fieldcap_m88",
	"rhs_fieldcap_m88_back"
];

//Backpack 
private _itemBackpack = 
[
	"wsx_tacticalpack_oli",
	"pca_backpack_invisible",
	"pca_backpack_invisible_large",
	"aegis_tacticalpack_cbr",
	"rhs_rk_sht_30_olive",
	"rhssaf_kitbag_md2camo",
	"B_Carryall_oli",
	"B_Carryall_khk",
	"B_Carryall_cbr",
	"rhssaf_kitbag_md2camo",
	"B_Kitbag_rgr",
	"B_Kitbag_cbr",
	"wsx_eagle_a3_khk",
	"wsx_eagle_a3_rgr",
	"aegis_tacticalpack_khk"
];

//Cosmetic 
private _itemCosmetic = 
[
	"G_Bandanna_blk",
	"G_Bandanna_khk",
	"G_Bandanna_oli",
	"bear_bandana_m81",
	"G_Aviator",
	"G_Balaclava_blk",
	"G_Bandanna_aviator",
	"G_Bandanna_beast",
	"G_Bandanna_shades",
	"G_Bandanna_sport",
	
	"G_Bandanna_BlueFlame1",
	"G_Bandanna_RedFlame1",
	"G_Bandanna_CandySkull",
	"G_Balaclava_BlueStrips",
	"G_Bandanna_Vampire_01",
	"G_Combat",
	"G_Shades_Black",
	"G_Shades_Blue",
	"G_Shades_Green",
	"G_Shades_Red",
	"G_Spectacles",
	"G_Sport_Red",
	"G_Sport_Blackyellow",
	
	"G_Sport_BlackWhite",
	"G_Sport_Checkered",
	"G_Sport_Blackred",
	"G_Sport_Greenblack",
	"G_Squares_Tinted",
	"G_Squares",
	"G_Spectacles_Tinted",
	"aegis_bandanna_kawaii",
	"aegis_shemag_cbr",
	"aegis_shemag_shades_cbr",
	"aegis_shemag_tactical_cbr",
	"aegis_shemag_khk",
	"aegis_shemag_shades_khk",
	
	"aegis_shemag_tactical_khk",
	"aegis_shemag_oli",
	"aegis_shemag_shades_oli",
	"aegis_shemag_tactical_oli",
	"aegis_shemag_red",
	"aegis_shemag_shades_red",
	"aegis_shemag_tactical_red",
	"aegis_shemag_tan",
	"aegis_shemag_shades_tan",
	"aegis_shemag_tactical_tan",
	"aegis_shemag_white",
	"aegis_shemag_shades_white",
	"aegis_shemag_tactical_white",
	
	"bear_balaclava1_black",
	"CUP_G_TK_RoundGlasses",
	"CUP_G_TK_RoundGlasses_blk",
	"CUP_G_TK_RoundGlasses_gold",
	"milgp_f_face_shield_blk",
	"milgp_f_face_shield_cb",
	"milgp_f_face_shield_khk",
	
	"milgp_f_face_shield_rgr",
	"milgp_f_face_shield_tan",
	"milgp_f_face_shield_shemagh_blk",
	"milgp_f_face_shield_shemagh_cb",
	"milgp_f_face_shield_shemagh_khk",
	"milgp_f_face_shield_shemagh_tan",
	"milgp_f_face_shield_shemagh_rgr",
	
	"milgp_f_face_shield_shades_blk",
	"milgp_f_face_shield_shades_cb",
	"milgp_f_face_shield_shades_khk",
	"milgp_f_face_shield_shades_tan",
	"milgp_f_face_shield_shades_rgr",
	"milgp_f_face_shield_shades_shemagh_blk",
	"milgp_f_face_shield_shades_shemagh_cb",
	"milgp_f_face_shield_shades_shemagh_khk",
	"milgp_f_face_shield_shades_shemagh_tan",
	"milgp_f_face_shield_shades_shemagh_rgr",
	
	"pca_nvg_face_shield_blk",
	"pca_nvg_face_shield_cb",
	"pca_nvg_face_shield_khk",
	"pca_nvg_face_shield_tan",
	"pca_nvg_face_shield_rgr",

	"pca_nvg_face_shield_shemagh_blk",
	"pca_nvg_face_shield_shemagh_cb",
	"pca_nvg_face_shield_shemagh_khk",
	"pca_nvg_face_shield_shemagh_tan",
	"pca_nvg_face_shield_shemagh_rgr",

	"pca_nvg_shemagh_lowered_oli",
	"pca_nvg_shemagh_lowered_red",
	"pca_nvg_shemagh_lowered_tan",
	"pca_nvg_shemagh_lowered_white",
	"murshun_cigs_cigpack",
	"murshun_cigs_lighter"
];

//********************************************************************************//
// Miscellaneous Items
//********************************************************************************//

private _itemMisc = 
[
	"ACRE_PRC343",
	"ACE_MapTools",
	"ACE_RangeCard",
	"ItemCompass",
	"ItemMap",
	"ItemWatch",
	"ToolKit"
];

private _itemBino = 
[
	"Binocular"
];

private _itemRadio = 
[
	"ACRE_PRC148",
	"ACRE_PRC152",
	"ACRE_PRC117F"
];

private _itemMedBasic = 
[
	//Bandages
	"ACE_fieldDressing",
	"ACE_elasticBandage",
	"ACE_packingBandage",
	"ACE_quikclot",
	//Specialized Equipments
	"ACE_splint",
	"ACE_tourniquet"
];

private _itemMedAdv = 
[
	//Fluids
	"ACE_bloodIV",
	"ACE_bloodIV_250",
	"ACE_bloodIV_500",
	"ACE_plasmaIV",
	"ACE_plasmaIV_250",
	"ACE_plasmaIV_500",
	"ACE_salineIV",
	"ACE_salineIV_250",
	"ACE_salineIV_500",
	//Medications
	"ACE_adenosine",
	"ACE_epinephrine",
	"ACE_morphine",
	//Specialized Equipments
	"ACE_surgicalKit"
];

//********************************************************************************//
// Weapons
//********************************************************************************//

private _itemAcc = 
[
	//Optic
	"optic_mrco",
	"ace_optic_mrco_2d",
	"optic_arco_ak_blk_f",
	"rhsusf_acc_acog",
	"cup_optic_elcan_specterdr_black",
	"optic_hamr",
	"optic_arco",
	"ace_optic_arco_2d",
	"ace_optic_hamr_2d",
	"cup_optic_acog_ta01b_black",
	"cup_optic_acog_ta01b_coyote"
];

private _itemWeapRifle = 
[
	"sfp_weap_ak5c_blk",
	"sfp_weap_ak5c_vfg_blk"
];

private _itemWeapRifleUGL = 
[
	"sfp_weap_ak5c_m203_blk",
	"rhsusf_m112_mag"
];

private _itemWeapAR = 
[
	"sps_weap_kac_lamg_hg_blk",
	"sps_weap_kac_lamg_blk",
	"CUP_bipod_VLTOR_Modpod_black"
];

private _itemWeapLAT = 
[
	"fwa_weap_m2_carlgustaf_no78",
	"fwa_1rnd_m2_carlgustaf_HEAT",
	"fwa_1rnd_m2_carlgustaf_HE",
	"fwa_1rnd_m2_carlgustaf_WP"
];

private _itemWeapPistol = 
[
	"aegis_weap_fnx45_blk",
	"11Rnd_45ACP_Mag"
];

//Special
private _itemWeapMG = 
[
	"sps_weap_kac_amg_blk"
];

private _itemWeapSnipe = 
[
	"pca_weap_svd_wood_npz",
	"rhs_10Rnd_762x54mmR_7N14",
	"cup_optic_sb_3_12x50_pmii_pip"
];

//********************************************************************************//
// Ammunitions
//********************************************************************************//

private _itemAmmo = 
[
	//Rifle Ammo
	"pca_mag_30Rnd_556x45_M855A1_PMAG_Blk",
	"pca_mag_30Rnd_556x45_M856A1_PMAG_Blk",
	
	//Pistol Ammo
	"11Rnd_45ACP_Mag"
];

private _itemAmmoTracer = 
[
	"pca_mag_30Rnd_556x45_M856A1_PMAG_Blk"
];

private _itemAmmoAR = 
[
	"sps_200Rnd_556x45_M855A1_Mixed_KAC_Box",
	"sps_200Rnd_556x45_M856A1_Tracer_Red_KAC_Box"
];

private _itemAmmoSignal = 
[
	"SmokeShellBlue",
	"SmokeShellGreen",
	"SmokeShellOrange",
	"SmokeShellPurple",
	"SmokeShellRed",
	"SmokeShellYellow",
	"1Rnd_SmokeBlue_Grenade_shell",
	"1Rnd_SmokeGreen_Grenade_shell",
	"1Rnd_SmokeOrange_Grenade_shell",
	"1Rnd_SmokePurple_Grenade_shell",
	"1Rnd_SmokeRed_Grenade_shell",
	"1Rnd_SmokeYellow_Grenade_shell",
	"rhs_mag_m715_Green",
	"rhs_mag_m713_Red",
	"rhs_mag_m716_yellow",
	"ACE_40mm_Flare_red",
	"ACE_40mm_Flare_green",
	"ACE_40mm_Flare_white"
];

private _itemExplosive = 
[
	"1Rnd_Smoke_Grenade_shell",
	"rhs_mag_m714_White",
	"SmokeShell",
	"rhs_mag_M397_HET",
	"rhs_mag_M433_HEDP",
	"rhs_mag_M441_HE",
	"rhs_mag_m67"
];

//Special
private _itemAmmoMG = 
[
	"sps_100Rnd_762x51_M80A1_Mixed_KAC_Box",
	"sps_100Rnd_762x51_M62_Tracer_Red_KAC_Box"
];

private _itemEngineer = 
[
	"ACE_Clacker",
	"ACE_DefusalKit",
	"ACE_EntrenchingTool",
	"ACE_M26_Clacker",
	"ACE_wirecutter",
	"rhsusf_m112_mag",
	"rhsusf_m112x4_mag",
	"MineDetector",
	"ToolKit"
];

//********************************************************************************//
// Add Current Gear
//********************************************************************************//

{
	_itemGear pushBackUnique _x;
} forEach (primaryWeaponItems _unit);

{
	_itemGear pushBackUnique _x;
} forEach (handgunItems _unit);

{
	_itemGear pushBackUnique _x;
} forEach (assignedItems _unit);

_itemGear pushBack uniform _unit;
_itemGear pushBack vest _unit;
_itemGear pushBack headgear _unit;
_itemGear pushBack backpack _unit;

//********************************************************************************//
// Add Items
//********************************************************************************//

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
	//Assistant Automatic Rifle
	case (_unitRole == "aar") : 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemBino + _itemAcc + _itemWeapRifle + _itemAmmo + _itemAmmoAR + _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
	//Sharpshooter 
	case (_unitRole == "sh") : 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemAcc + _itemWeapSnipe + _itemAmmo+ _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
	//Team Leader 
	case (_unitRole == "tl") : 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemBino + _itemRadio + _itemAcc + _itemWeapRifle + _itemWeapPistol + _itemAmmo + _itemAmmoTracer + _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
	//Squad Leader 
	case (_unitRole == "sl") : 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemBino + _itemRadio + _itemAcc + _itemWeapRifle + _itemWeapRifleUGL + _itemWeapPistol + _itemAmmo + _itemAmmoTracer + _itemAmmoSignal + _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
	//Platoon Sergeant 
	case (_unitRole == "sgt") : 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemBino + _itemRadio + _itemAcc + _itemWeapRifle + _itemWeapRifleUGL + _itemWeapPistol + _itemAmmo + _itemAmmoTracer + _itemAmmoSignal + _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
	//Platoon Commander 
	case (_unitRole == "co") : 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemBino + _itemRadio + _itemAcc + _itemWeapRifle + _itemWeapPistol + _itemAmmo + _itemAmmoTracer + _itemAmmoSignal + _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
	//Rifle First-Aid
	case (_unitRole == "rm_fa") : 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemMedBasic + _itemAcc + _itemWeapRifle + _itemAmmo + _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
	//Combat Life Saver
	case (_unitRole == "cls") : 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemMedBasic + _itemMedAdv + _itemAcc + _itemWeapRifle + _itemWeapPistol + _itemAmmo + _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
	//Medium Machine Gunner
	case (_unitRole == "mmg") : 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemAcc + _itemWeapMG + _itemWeapPistol + _itemAmmoMG + _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
	//Assistant Medium Machine Gunner
	case (_unitRole == "ammg") : 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemBino + _itemAcc + _itemWeapRifle + _itemWeapPistol + _itemAmmo + _itemAmmoMG + _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
	//Assistant Medium Machine Gunner
	case (_unitRole == "tlmmg") : 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemBino + _itemRadio + _itemAcc + _itemWeapRifle + _itemWeapPistol + _itemAmmo + _itemAmmoMG + _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
	default 
	{
		[arsenal, (_itemGear + _itemUniform + _itemVest + _itemHeadgear + _itemBackpack + _itemCosmetic + _itemMisc + _itemAcc + _itemWeapRifle + _itemAmmo + _itemExplosive)] call ace_arsenal_fnc_initBox;
	};
};

//********************************************************************************//
// Add Actions
//********************************************************************************//

_action = 
[
	"personal_arsenal", "Personal Arsenal", "\a3\ui_f\data\igui\cfg\weaponicons\mg_ca.paa",
	{
		[arsenal, _player] call ace_arsenal_fnc_openBox
	},
	{
		(player distance2D (player getVariable ["startPos", [0,0,0]])) < 100
	},
	{},
	[],
	[0,0,0],
	3
] call ace_interact_menu_fnc_createAction;

[_unit, 1, ["ACE_SelfActions"], _action] call ace_interact_menu_fnc_addActionToObject;