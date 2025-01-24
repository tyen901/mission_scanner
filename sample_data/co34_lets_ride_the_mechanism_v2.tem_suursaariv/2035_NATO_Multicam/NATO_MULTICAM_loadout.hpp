/*
	* Faction: NATO (Multicam, 2035)
*/

// Weaponless Baseclass
class baseMan 
{
	displayName = "Unarmed";
	// All Randomized.
	uniform[] = {};
	vest[] = {};
	backpack[] = {};
	headgear[] = {};
	goggles[] = {"default"};
	hmd[] = {};
	// Leave empty to not change faces and Insignias -> example: faces[] = {};
	faces[] = {"faceset:african", "faceset:caucasian"};
	insignias[] = {};
	//All Randomized. Add Primary Weapon and attachments.
	//Leave Empty to remove all. {"Default"} for using original items the character start with.
	primaryWeapon[] = {};
	scope[] = {};
	bipod[] = {};
	attachment[] = {};
	silencer[] = {};
	//SecondaryAttachments[] arrays are NOT randomized.
	secondaryWeapon[] = {};
	secondaryAttachments[] = {};
	sidearmWeapon[] = {};
	sidearmAttachments[] = {};
	// These are added to the uniform or vest first - overflow goes to backpack if there is space.
	magazines[] = {};
	items[] = {};
	// These are added directly into their respective slots
	linkedItems[] = 
	{
		"ItemWatch",
		"ItemMap",
		"ItemCompass"
	};
	// These are put directly into the backpack.
	backpackItems[] = {};
	// This is executed after the unit init is complete. Argument: _this = _unit.
	code = "";
};

class rm : baseMan
{
	displayName = "Rifleman";
	uniform[] = 
	{
		"U_B_CombatUniform_mcam",
		"U_B_CombatUniform_mcam_vest"
	};
	vest[] = 
	{
		"milgp_v_marciras_assaulter_mc"
	};
	headgear[] = 
	{
		"aegis_ech_mtp"
	};
	backpack[] = 
	{
		"aegis_assaultpack_mtp"
	};
	primaryWeapon[] = 
	{
		"arifle_MX_F"
	};
	scope[] = 
	{
		"cup_optic_trijiconrx01_black"
	};
	bipod[] = {};
	attachment[] = 
	{
		LIST_2(""),
		"acc_pointer_ir",
	};
	items[] =
	{
		//Standard Start Items for player
		"ACRE_PRC343",
		LIST_10("ACE_fieldDressing"),
		LIST_5("ACE_packingBandage"),
		LIST_5("ACE_quikclot"),
		LIST_4("ACE_tourniquet"),
		LIST_2("ACE_epinephrine"),
		LIST_2("ACE_morphine"),
		LIST_2("ACE_splint")
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("HandGrenade"),
		LIST_13("30Rnd_65x39_caseless_mag")
	};
	backpackItems[] = 
	{
		LIST_4("30Rnd_65x39_caseless_mag")
	};
};

class ar : rm 
{
	displayName = "Automatic Rifleman";
	vest[] = 
	{
		"milgp_v_marciras_hgunner_belt_mc"
	};
	backpack[] = 
	{
		"pca_eagle_a3_oefcp"
	};
	primaryWeapon[] = 
	{
		"arifle_MX_SW_F"
	};
	bipod[] = {};
	attachment[] = 
	{
		"",
		"acc_pointer_ir"
	};
	sidearmWeapon[] = 
	{
		"hgun_P07_F"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("rhs_mag_m67"),
		LIST_3("16Rnd_9x21_Mag"),
		LIST_5("100Rnd_65x39_caseless_mag")
	};
	backpackItems[] = 
	{
		LIST_4("100Rnd_65x39_caseless_mag")
	};
};

class aar : rm 
{
	displayName = "Assistant Automatic Rifleman";
	backpack[] = 
	{
		"pca_eagle_a3_oefcp"
	};
	backpackItems[] += 
	{
		LIST_6("100Rnd_65x39_caseless_mag")
	};
	linkedItems[] += 
	{
		"Binocular"
	};
};

class rm_lat : rm 
{
	displayName = "Rifleman (LAT)";
	secondaryWeapon[] = 
	{
		"pca_weap_m136cs"
	};
	backpackItems[] = 
	{
		"pca_weap_m136cs"
	};
};

class gren : rm 
{
	displayName = "Grenadier";
	vest[] = 
	{
		"rhsusf_spcs_ocp_grenadier"
	};
	primaryWeapon[] = 
	{
		"arifle_MX_GL_F"
	};
	backpackItems[] = 
	{
		LIST_10("3Rnd_HE_Grenade_shell"),
		LIST_4("1Rnd_Smoke_Grenade_shell")
	};
};

class tl : rm 
{
	displayName = "Team Leader";
	vest[] = 
	{
		"milgp_v_marciras_teamleader_mc"
	};
	headgear[] = 
	{
		"aegis_lch_mtp"
	};
	backpackItems[] = 
	{
		LIST_2("SmokeShell")
	};
	linkedItems[] += 
	{
		"Binocular"
	};
};

class sl : tl 
{
	displayName = "Squad Leader";
	primaryWeapon[] = 
	{
		"arifle_MX_GL_F"
	};
	items[] += 
	{
		"ACRE_PRC148"
	};
	backpackItems[] =
	{
		LIST_5("3Rnd_HE_Grenade_shell"),
		LIST_3("3Rnd_Smoke_Grenade_shell"),
		LIST_2("1Rnd_SmokeBlue_Grenade_shell"),
		LIST_2("1Rnd_SmokeGreen_Grenade_shell"),
		LIST_2("1Rnd_SmokeRed_Grenade_shell")
	};
};

class co : sl 
{
	displayName = "Platoon Commander";
};

class rm_fa : rm 
{
	displayName = "Rifleman (First-Aid)";
	traits[] = {"medic"};
	backpack[] = 
	{
		"pca_eagle_a3_oefcp"
	};
	backpackItems[] +=
	{
		LIST_15("ACE_fieldDressing"),
		LIST_15("ACE_packingBandage"),
		LIST_10("ACE_epinephrine"),
		LIST_10("ACE_morphine"),
		LIST_8("ACE_bloodIV"),
		LIST_4("ACE_personalAidKit"),
		LIST_4("ACE_splint"),
		LIST_4("ACE_tourniquet"),
		LIST_2("ACE_adenosine")
	};
};

class cls : rm_fa
{
	displayName = "Combat Life Saver";
	backpackItems[] =
	{
		"ACE_surgicalKit",
		LIST_20("ACE_elasticBandage"),
		LIST_20("ACE_fieldDressing"),
		LIST_20("ACE_packingBandage"),
		LIST_20("ACE_epinephrine"),
		LIST_20("ACE_morphine"),
		LIST_12("ACE_bloodIV"),
		LIST_10("ACE_splint"),
		LIST_4("ACE_personalAidKit"),
		LIST_4("ACE_tourniquet"),
		LIST_2("ACE_adenosine")
	};
};

class mmg : rm 
{
	displayName = "Medium Machine Gunner";
	vest[] = 
	{
		"milgp_v_marciras_hgunner_belt_mc"
	};
	backpack[] = 
	{
		"pca_eagle_a3_oefcp"
	};
	primaryWeapon[] = 
	{
		"sps_weap_kac_amg_tan"
	};
	bipod[] = 
	{
		"hlc_bipod_utgshooters"
	};
	attachment[] = {};
	sidearmWeapon[] = 
	{
		"hgun_P07_F"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("HandGrenade"),
		LIST_3("16Rnd_9x21_Mag"),
		LIST_3("sps_100Rnd_762x51_M80A1_Mixed_KAC_Box")
	};
	backpackItems[] = 
	{
		LIST_6("sps_100Rnd_762x51_M80A1_Mixed_KAC_Box")
	};
};

class ammg : rm 
{
	displayName = "Assistant Medium Machine Gunner";
	backpack[] = 
	{
		"pca_eagle_a3_oefcp"
	};
	backpackItems[] = 
	{
		LIST_8("sps_100Rnd_762x51_M80A1_Mixed_KAC_Box")
	};
	linkedItems[] = 
	{
		"Binocular"
	};
};

class mat : rm 
{
	displayName = "Medium Anti-Tank Gunner";
	backpack[] = 
	{
		"pca_eagle_a3_oefcp"
	};
	secondaryWeapon[] = 
	{
		"launch_MRAWS_green_rail_F"
	};
	sidearmWeapon[] = 
	{
		"hgun_P07_F"
	};
	magazines[] += 
	{
		LIST_3("16Rnd_9x21_Mag")
	};
	backpackItems[] = 
	{
		LIST_2("MRAWS_HEAT_F")
	};
};

class amat : rm 
{
	displayName = "Assistant Medium Anti-Tank Gunner";
	backpack[] = 
	{
		"pca_eagle_a3_oefcp"
	};
	backpackItems[] = 
	{
		LIST_2("MRAWS_HEAT_F"),
		"MRAWS_HEAT55_F",
		"MRAWS_HE_F"
	};
	linkedItems[] = 
	{
		"Binocular"
	};
};

//////// ROLES NOT USED IN BASE TEMPLATE ///////////////////////////////////////////

class eng : rm 
{
	displayName = "Engineer";
	traits[] = {"engineer","explosiveSpecialist"};
	backpack[] = 
	{
		"pca_eagle_a3_oefcp"
	};
	sidearmWeapon[] = 
	{
		"hgun_P07_F"
	};
	magazines[] += 
	{
		LIST_3("16Rnd_9x21_Mag")
	};
	backpackItems[] = 
	{
		"ToolKit",
		"ACE_DefusalKit",
		"ACE_M26_Clacker",
		"ACE_wirecutter",
		LIST_4("rhsusf_m112_mag"),
		LIST_2("rhsusf_m112x4_mag")
	};
};

class dm : rm 
{
	displayName = "Designated Marksman";
	vest[] = 
	{
		"milgp_v_marciras_marksman_belt_mc"
	};
	headgear[] = 
	{
		"usp_cap_ct_mc"
	};
	primaryWeapon[] = 
	{
		"arifle_MXM_F"
	};
	scope[] = 
	{
		"optic_dms"
	};
	attachment[] = {};
	bipod[] = 
	{
		"ptv_acc_hbrs"
	};
	sidearmWeapon[] = 
	{
		"hgun_P07_F"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("HandGrenade"),
		LIST_3("16Rnd_9x21_Mag"),
		LIST_9("30Rnd_65x39_caseless_mag")
	};
	backpackItems[] = 
	{
		LIST_12("30Rnd_65x39_caseless_mag")
	};
	linkedItems[] = 
	{
		"Binocular"
	};
};

class crew : rm 
{
	displayName = "Crewman";
	traits[] = {"engineer"};
	vest[] = 
	{
		"milgp_v_marciras_light_mc"
	};
	primaryWeapon[] = 
	{
		"arifle_MXC_F"
	};
	headgear[] = 
	{
		"H_HelmetCrew_B"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("HandGrenade"),
		LIST_9("30Rnd_65x39_caseless_mag")
	};
	backpackItems[] = 
	{
		"ToolKit"
	};
};

class crew_co : crew 
{
	displayName = "Crewman Commander";
	sidearmWeapon[] = 
	{
		"hgun_P07_F"
	};
	items[] +=
	{
		"ACRE_PRC148"
	};
	magazines[] += 
	{
		LIST_3("16Rnd_9x21_Mag"),
		LIST_2("SmokeShellBlue"),
		LIST_2("SmokeShellGreen"),
		LIST_2("SmokeShellRed")
	};
	linkedItems[] +=
	{
		"Binocular"
	};
};

class hp : rm 
{
	displayName = "Helicopter Pilot";
	vest[] = 
	{
		"milgp_v_marciras_light_mc"
	};
	headgear[] = 
	{
		"H_PilotHelmetHeli_B"
	};
	primaryWeapon[] = 
	{
		"arifle_MXC_F"
	};
	sidearmWeapon[] = 
	{
		"hgun_P07_F"
	};
	items[] +=
	{
		"ACRE_PRC148"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_7("30Rnd_65x39_caseless_mag"),
		LIST_3("16Rnd_9x21_Mag"),
		LIST_2("SmokeShellBlue"),
		LIST_2("SmokeShellGreen"),
		LIST_2("SmokeShellRed")
	};
};