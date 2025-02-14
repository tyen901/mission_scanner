/*
	DESC: Underequipped Militia, c.20XX
	CAMO: M88 partially-Leska
	VEST: Storage Only
	AMMO: Whatever is available
*/

class baseMan 
{
	displayName = "Unarmed";
	// All Randomized
	uniform[] = 
	{
		"TC_U_aegis_guerilla_garb_m81_sudan",
		"TC_U_aegis_guerilla_jacket_m81_sudan",
		"TC_U_aegis_guerilla_tshirt_m81_sudan",
		"aegis_guerilla_tshirt_m81_alt",
		"rhsgref_uniform_TLA_2"
	};
	vest[] = 
	{
		"bear_chicom_drab",
		"rhsgref_chicom",
		"aegis_chestrig_rgr",
		"aegis_chestrig_oli"
	};
	backpack[] = {};
	headgear[] = 
	{
		"pca_ssh68_camo_des",
		"pca_ssh68_camo_mix",
		"pca_headband",
		"CUP_H_FR_BandanaGreen",
		"H_Booniehat_oli",
		"",
		"pca_m88_fieldcap",
		"CUP_H_US_patrol_cap_OD",
		"H_Cap_oli"
	};
	goggles[] = {};
	hmd[] = {};
	// Leave empty to not change faces and Insignias
	faces[] = 
	{
		"AfricanHead_01", 
		"AfricanHead_02",
		"AfricanHead_03",
		"PersianHead_A3_01",
		"PersianHead_A3_02",
		"TanoanHead_A3_01",
		"TanoanHead_A3_02",
		"TanoanHead_A3_03",
		"TanoanHead_A3_04",
		"TanoanHead_A3_05"
	};
	insignias[] = {};
	// All Randomized. Add Primary Weapon and attachments
	// Leave Empty to remove all. {"Default"} for using original items the character start with
	primaryWeapon[] = {};
	scope[] = {};
	bipod[] = {};
	attachment[] = {};
	silencer[] = {};
	// SecondaryAttachments[] arrays are NOT randomized
	secondaryWeapon[] = {};
	secondaryAttachments[] = {};
	sidearmWeapon[] = {};
	sidearmAttachments[] = {};
	// These are added to the uniform or vest first - overflow goes to backpack if there's any
	magazines[] = {};
	items[] = {
		"rhs_mag_rdg2_white",
		"rhs_mag_rgd5"
	};
	// These are added directly into their respective slots
	linkedItems[] = 
	{
		"ItemWatch",
		"ItemMap",
		"ItemCompass"
	};
	// These are put directly into the backpack
	backpackItems[] = {};
	// Ths is executed after the unit init is complete. Argument: _this = _unit
	code = "";
};

class rm : baseMan
{
	displayName = "Rifleman";
	primaryWeapon[] = 
	{
		"fwa_weap_type56",
		"CUP_arifle_AKM_Early"
	};
	backpack[] = 
	{
		""
	};
	items[] =
	{
		LIST_2("ACE_fieldDressing"),
		LIST_2("ACE_splint"),
		"ACE_morphine"
	};
	magazines[] += 
	{
		LIST_7("rhs_30Rnd_762x39mm"),
		
	};
};

class ar : rm 
{
	displayName = "Automatic Rifleman";
	primaryWeapon[] = 
	{
		"fwa_weap_rpd"
	};
	magazines[] = 
	{
		LIST_3("fwa_100rnd_762x39mm_rpd_mixed")
	};
};

class aar : rm 
{
	displayName = "Assistant Automatic Rifleman";
	backpackItems[] += 
	{
		LIST_4("fwa_100rnd_762x39mm_rpd_mixed")
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
		"rhs_weap_rpg26"
	};
	backpackItems[] += 
	{
		"rhs_weap_rpg26"
	};
};

class manpad : rm 
{
	displayName = "Rifleman (MANPAD)";
	secondaryWeapon[] = 
	{
		"rhs_weap_igla"
	};
};
class gren : rm 
{
	displayName = "Grenadier";
	primaryWeapon[] = 
	{
		"rhs_weap_akms_gp25"
	};
	magazines[] += 
	{
		LIST_3("rhs_VOG25"),
		LIST_1("rhs_GRD40_White")
	};
};

class tl : gren 
{
	displayName = "Team Leader";
	linkedItems[] += 
	{
		"Binocular"
	};
};

class sl : tl 
{
	displayName = "Squad Leader";
	items[] += 
	{
		"ACRE_PRC148"
	};
	sidearmWeapon[] = 
	{
		"rhs_weap_makarov_pm"
	};
	magazines[] += 
	{
		LIST_2("rhs_mag_9x18_8_57N181S")
	};
	backpackItems[] =
	{
		LIST_21("rhs_VOG25"),
		LIST_6("rhs_GRD40_White"),
		LIST_2("rhs_GRD40_Green"),
		LIST_2("rhs_GRD40_Red")
	};
};

class sgt : sl 
{
	displayName = "Platoon Sergeant";
	backpackItems[] =
	{
		LIST_13("rhs_VOG25"),
		LIST_4("rhs_GRD40_White"),
		LIST_2("rhs_GRD40_Green"),
		LIST_2("rhs_GRD40_Red"),
		LIST_2("SmokeShellBlue"),
		LIST_2("SmokeShellGreen"),
		LIST_2("SmokeShellRed")
	};
};

class co : sl 
{
	displayName = "Platoon Commander";
	primaryWeapon[] = 
	{
		"rhs_weap_akm"
	};
	backpackItems[] =
	{
		LIST_2("SmokeShellBlue"),
		LIST_2("SmokeShellGreen"),
		LIST_2("SmokeShellRed")
	};
};

class fac : sl 
{
	displayName = "Forward Air Controller";
	backpackItems[] =
	{
		"Laserbatteries",
		LIST_11("rhs_VOG25"),
		LIST_4("rhs_GRD40_White"),
		LIST_4("rhs_GRD40_Green"),
		LIST_4("rhs_GRD40_Red"),
		LIST_2("SmokeShellBlue"),
		LIST_2("SmokeShellGreen"),
		LIST_2("SmokeShellRed")
	};
	linkedItems[] += 
	{
		"Laserdesignator"
	};
};

class rm_fa : rm 
{
	displayName = "Rifleman (First-Aid)";
	traits[] = {"medic"};
	backpack[] =
	{
		"CUP_B_SLA_Medicbag",
		"rhs_medic_bag"
	};
	backpackItems[] =
	{
		LIST_20("ACE_fieldDressing"),
		LIST_15("ACE_packingBandage"),
		LIST_15("ACE_elasticBandage"),
		LIST_10("ACE_epinephrine"),
		LIST_10("ACE_morphine"),
		LIST_8("ACE_bloodIV"),
		LIST_4("ACE_splint"),
		LIST_4("ACE_tourniquet"),
		LIST_2("ACE_adenosine")
	};
};

class cls : rm_fa
{
	displayName = "Combat Life Saver";
	sidearmWeapon[] = 
	{
		"rhs_weap_makarov_pm"
	};
	magazines[] += 
	{
		LIST_2("rhs_mag_9x18_8_57N181S")
	};
	backpackItems[] =
	{
		"ACE_surgicalKit",
		LIST_30("ACE_elasticBandage"),
		LIST_30("ACE_packingBandage"),
		LIST_20("ACE_fieldDressing"),
		LIST_20("ACE_epinephrine"),
		LIST_20("ACE_morphine"),
		LIST_12("ACE_bloodIV"),
		LIST_10("ACE_splint"),
		LIST_4("ACE_tourniquet"),
		LIST_2("ACE_adenosine")
	};
};

class mmg : baseMan
{
	displayName = "Medium Machine Gunner";
	primaryWeapon[] = 
	{
		"hlc_lmg_mg3"
	};
	bipod[] = {};
	attachment[] = {};
	sidearmWeapon[] = 
	{
		"rhs_weap_makarov_pm"
	};
	magazines[] += 
	{
		LIST_2("rhs_mag_9x18_8_57N181S"),
		LIST_3("hlc_50Rnd_762x51_B_MG3")
	};
};

class ammg : rm 
{
	displayName = "Assistant Medium Machine Gunner";
	magazines[] += 
	{
		LIST_3("hlc_50Rnd_762x51_B_MG3")
	};
	linkedItems[] += 
	{
		"Binocular"
	};
};

class mat : rm 
{
	displayName = "Medium Anti-Tank Gunner";
	sidearmWeapon[] = 
	{
		"rhs_weap_makarov_pm"
	};
	secondaryWeapon[] = 
	{
		"rhs_weap_rpg7"
	};
	secondaryAttachments[] = 
	{
		"rhs_acc_pgo7v"
	};
	backpack[] = {
		"rhs_rpg_2"
	};
	magazines[] += 
	{
		LIST_2("rhs_mag_9x18_8_57N181S"),
		LIST_2("rhs_rpg7_PG7VL_mag")
	};
};

class amat : rm 
{
	displayName = "Assistant Medium Anti-Tank Gunner";
	sidearmWeapon[] = 
	{
		"rhs_weap_makarov_pm"
	};
	magazines[] += 
	{
		LIST_2("rhs_mag_9x18_8_57N181S")
	};
	backpackItems[] = 
	{
		LIST_2("rhs_rpg7_PG7VL_mag"),
	};
	linkedItems[] += 
	{
		"Binocular"
	};
};

class crew : rm 
{
	displayName = "Crewman";
	traits[] = {"engineer"};
	headgear[] = 
	{
		"rhs_tsh4",
		"rhs_tsh4_bala",
		"rhs_tsh4_ess"
	};
	items[] = 
	{
		"ToolKit"
	};
};

class crew_co : crew 
{
	displayName = "Crewman Commander";
	items[] +=
	{
		"ACRE_PRC148"
	};
	magazines[] += 
	{
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
	headgear[] = 
	{
		"CUP_H_RUS_Bandana_GSSh_Headphones",
		"CUP_H_PMC_EP_Headset",
		"aegis_cap_headphones_gry"
	};
	items[] +=
	{
		"ACRE_PRC148"
	};
	sidearmWeapon[] = 
	{
		"rhs_weap_makarov_pm"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_7("fwa_10rnd_762x39_sks"),
		LIST_3("rhs_mag_9x18_8_57N181S"),
		LIST_2("SmokeShellBlue"),
		LIST_2("SmokeShellGreen"),
		LIST_2("SmokeShellRed")
	};
};

class eng : rm 
{
	displayName = "Engineer";
	traits[] = {"engineer","explosiveSpecialist"};
	backpack[] = 
	{
		"pca_rd54_tan"
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

//********************************************************************************//
//Uncommon Roles - !!! CUSTOM ENTRIES NEEDED FOR CURATED ARSENAL !!!
//********************************************************************************//
class jp : rm 
{
	displayName = "Jet Pilot";
	uniform[] = 
	{
		"CUP_U_O_SLA_Overalls_Pilot"
	};
	headgear[] = 
	{
		"rhs_zsh7a_alt"
	};
	backpack[] = 
	{
		"B_Parachute"
	};
	items[] +=
	{
		"ACRE_PRC148"
	};
	primaryWeapon[] = {};
	sidearmWeapon[] = 
	{
		"rhs_weap_makarov_pm"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_5("rhs_mag_9x18_8_57N181S"),
		LIST_2("SmokeShellBlue"),
		LIST_2("SmokeShellGreen"),
		LIST_2("SmokeShellRed")
	};
	backpackItems[] = {};
};

class dm : rm 
{
	displayName = "Designated Marksman";
	primaryWeapon[] = 
	{
		"CUP_srifle_CZ550"
	};
	attachment[] = {};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("rhs_mag_f1"),
		LIST_9("CUP_5x_22_LR_17_HMR_M")
	};
	backpackItems[] = 
	{
		LIST_12("CUP_5x_22_LR_17_HMR_M")
	};
	linkedItems[] += 
	{
		"Binocular"
	};
};

class spt : rm 
{
	displayName = "Spotter";
	headgear[] = 
	{
		"rhsusf_ach_helmet_camo_ocp"
	};
	scope[] = 
	{
		"rhs_acc_pso1m21"
	};
	backpackItems[] += 
	{
		LIST_2("SmokeShell"),
		"ACE_SpottingScope",
		"ACE_Tripod"
	};
	linkedItems[] += 
	{
		"Rangefinder"
	};
};

class hmg : rm 
{
	displayName = "Heavy Machine Gunner";
	backpack[] = 
	{
		"ace_compat_rhs_usf3_m2_carry"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("rhs_mag_f1"),
		LIST_9("fwa_10rnd_762x39_sks"),
		"ace_csw_100Rnd_127x99_mag_red"
	};
	backpackItems[] = 
	{
		LIST_3("ace_csw_100Rnd_127x99_mag_red")
	};
};

class ahmg : rm 
{
	displayName = "Assistant Heavy Machine Gunner";
	backpack[] = 
	{
		"ace_csw_m3CarryTripodLow"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("rhs_mag_f1"),
		LIST_9("fwa_10rnd_762x39_sks"),
		"ace_csw_100Rnd_127x99_mag_red"
	};
	backpackItems[] = 
	{
		LIST_3("ace_csw_100Rnd_127x99_mag_red")
	};
	linkedItems[] += 
	{
		"Binocular"
	};
};

class atgm : rm 
{
	displayName = "Antitank Guided Missile Operator";
	backpack[] = 
	{
	};
	magazines[] = 
	{
	};
	backpackItems[] = 
	{
	};
};

class aatgm : rm 
{
	displayName = "Assistant Antitank Guided Missile Operator";
	backpack[] = 
	{
	};
	magazines[] = 
	{
	};
	backpackItems[] = 
	{
	};
	linkedItems[] += 
	{
		"Binocular"
	};
};