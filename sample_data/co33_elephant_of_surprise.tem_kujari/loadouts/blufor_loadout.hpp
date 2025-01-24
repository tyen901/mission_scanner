class baseMan 
{
	displayName = "Unarmed";
	// All Randomized
	uniform[] = {
		"usm_bdu_bnu_tan",
		"usm_bdu_bnu_dcu2",
		"usm_bdu_srl_dcu2",
		"usm_bdu_srh_dcu2",
		"usm_bdu_bti_dcu2"
	};
	vest[] = {};
	backpack[] = {};
	headgear[] = 
	{
		"pca_opscore_tan",
		"pca_opscore_ct_tan",
		"pca_opscore_ct_cb_tan",
		"pca_opscore_ct_cm_tan",
		"pca_opscore_ct_cw_tan"
	};
	goggles[] = {};
	hmd[] = 
	{
		"NVGoggles"
	};
	// Leave empty to not change faces and Insignias
	faces[] = {};
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
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("rhs_mag_m67")
	};
	items[] =
	{
		"ACRE_PRC343",
		LIST_10("ACE_fieldDressing"),
		LIST_10("ACE_packingBandage"),
		LIST_4("ACE_tourniquet"),
		LIST_2("ACE_epinephrine"),
		LIST_2("ACE_morphine"),
		LIST_2("ACE_splint")
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
	// This is executed after the unit init is complete. Argument: _this = _unit
	code = "";
};

class rm : baseMan
{
	displayName = "Rifleman";
	vest[] = 
	{
		"simc_vest_pasgt_lbv_alt_dcu",
		"simc_vest_pasgt_lbv_dcu"
	};
	primaryWeapon[] = 
	{
		"hlc_rifle_m16a3"
	};
	hmd[] = 
	{
		"NVGoggles"
	};
	backpack[] = 
	{
		"pca_backpack_invisible"
	};
	magazines[] += 
	{
		LIST_7("rhs_mag_30Rnd_556x45_M855_Stanag")
	};
};

class ar : baseMan 
{
	displayName = "Automatic Rifleman";
	vest[] = 
	{
		"simc_vest_pasgt_lc2_saw_dcu"
	};
	primaryWeapon[] = 
	{
		"rhs_weap_m249_light_S"
	};
	bipod[] = 
	{
		"rhsusf_acc_saw_lw_bipod"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("rhs_mag_m67"),
		LIST_3("rhsusf_200Rnd_556x45_mixed_soft_pouch")
	};
};

class aar : rm 
{
	displayName = "Assistant Automatic Rifleman";
	backpack[] = 
	{
		"rhsusf_assault_eagleaiii_ocp"
	};
	backpackItems[] += 
	{
		LIST_4("rhsusf_200Rnd_556x45_mixed_soft_pouch")
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
		"rhs_weap_M136"
	};
};

class gren : rm 
{
	displayName = "Grenadier";
	primaryWeapon[] = 
	{
		"hlc_rifle_m16a3_m203"
	};
	vest[] = 
	{
		"simc_vest_pasgt_lc2_gren_dcu"
	};
	magazines[] += 
	{
		LIST_10("1Rnd_HE_Grenade_shell"),
		LIST_5("ACE_40mm_Flare_ir")
	};
};

class tl : gren 
{
	displayName = "Team Leader";
	primaryWeapon[] = 
	{
		"hlc_rifle_m16a3_m203"
	};
	backpackItems[] =
	{
		LIST_11("rhs_mag_M441_HE"),
		LIST_11("ACE_40mm_Flare_ir")
	};
	linkedItems[] += 
	{
		"CUP_Vector21Nite"
	};
};

class sl : tl 
{
	displayName = "Squad Leader";
	items[] += 
	{
		"ACRE_PRC148"
	};
};

class sgt : rm 
{
	displayName = "Drone Operator";
	backpack[] = 
	{
		"B_UAV_01_backpack_F"
	};
	linkedItems[] +=
	{
		"B_UavTerminal"
	};
};

class co : sl 
{
	displayName = "Platoon Commander";
	primaryWeapon[] = 
	{
		"hlc_rifle_m16a3_m203"
	};
	backpackItems[] =
	{
		LIST_11("rhs_mag_M441_HE"),
		LIST_11("ACE_40mm_Flare_ir")
	};
};

class fac : sl 
{
	displayName = "Forward Air Controller";
	backpackItems[] =
	{
		"Laserbatteries",
		LIST_11("rhs_mag_M441_HE"),
		LIST_4("1Rnd_Smoke_Grenade_shell"),
		LIST_4("1Rnd_SmokeBlue_Grenade_shell"),
		LIST_4("1Rnd_SmokeGreen_Grenade_shell"),
		LIST_4("1Rnd_SmokeRed_Grenade_shell"),
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
	items[] =
	{
		LIST_20("ACE_fieldDressing"),
		LIST_15("ACE_elasticBandage"),
		LIST_5("ACE_epinephrine"),
		LIST_5("ACE_morphine"),
		LIST_8("ACE_bloodIV"),
		LIST_4("ACE_splint"),
		LIST_4("ACE_tourniquet"),
		LIST_2("ACE_adenosine")
	};
};

class cls : rm_fa
{
	displayName = "Combat Life Saver";
	items[] +=
	{
		"ACE_surgicalKit"
	};
};

class crew : rm 
{
	displayName = "Crewman";
	traits[] = {"engineer"};
	vest[] = 
	{
		"simc_vest_pasgt_lbv_alt_dcu",
		"simc_vest_pasgt_lbv_dcu"
	};
	headgear[] = 
	{
		"rhsusf_cvc_helmet",
		"rhsusf_cvc_alt_helmet",
		"rhsusf_cvc_ess"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("rhs_mag_m67"),
		LIST_7("rhs_mag_30Rnd_556x45_M855_Stanag")
	};
	items[] = 
	{
		"ToolKit"
	};
};

class crew_co : crew 
{
	displayName = "Crewman Commander";
	primaryWeapon[] = 
	{
		"hlc_rifle_m16a3_m203"
	};
	backpackItems[] =
	{
		LIST_11("rhs_mag_M441_HE"),
		LIST_11("ACE_40mm_Flare_ir")
	};
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
		"CUP_Vector21Nite"
	};
};

class hp : rm 
{
	displayName = "Helicopter Pilot";
	uniform[] = 
	{
		"CUP_U_B_USMC_PilotOverall"
	};
	vest[] = 
	{
		"CUP_V_B_USArmy_PilotVest"
	};
	headgear[] = 
	{
		"rhsusf_ihadss"
	};
	items[] +=
	{
		"ACRE_PRC148"
	};
	sidearmWeapon[] = 
	{
		"rhsusf_weap_glock17g4"
	};
	magazines[] += 
	{
		LIST_3("rhsusf_mag_17Rnd_9x19_JHP"),
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
		"rhsusf_assault_eagleaiii_ocp"
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
		"CUP_U_B_USArmy_PilotOverall"
	};
	vest[] = 
	{
		"CUP_V_B_PilotVest"
	};
	headgear[] = 
	{
		"rhsusf_hgu56p_visor_mask"
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
		"rhsusf_weap_glock17g4"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_5("rhsusf_mag_17Rnd_9x19_JHP"),
		LIST_2("SmokeShellBlue"),
		LIST_2("SmokeShellGreen"),
		LIST_2("SmokeShellRed")
	};
	backpackItems[] = {};
};

class dm : rm 
{
	displayName = "Designated Marksman";
	vest[] = 
	{
		"rhsusf_spcs_ocp_sniper"
	};
	headgear[] = 
	{
		"rhsusf_ach_helmet_camo_ocp"
	};
	primaryWeapon[] = 
	{
		"rhs_weap_m14ebrri"
	};
	scope[] = 
	{
		"rhsusf_acc_ACOG"
	};
	attachment[] = {};
	bipod[] = 
	{
		"rhsusf_acc_harris_bipod"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("rhs_mag_m67"),
		LIST_9("rhsusf_20Rnd_762x51_m118_special_Mag")
	};
	backpackItems[] = 
	{
		LIST_12("rhsusf_20Rnd_762x51_m118_special_Mag")
	};
	linkedItems[] += 
	{
		"CUP_Vector21Nite"
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
		"rhsusf_acc_ACOG"
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
		LIST_2("rhs_mag_m67"),
		LIST_9("rhs_mag_30Rnd_556x45_M855A1_Stanag"),
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
		LIST_2("rhs_mag_m67"),
		LIST_9("rhs_mag_30Rnd_556x45_M855A1_Stanag"),
		"ace_csw_100Rnd_127x99_mag_red"
	};
	backpackItems[] = 
	{
		LIST_3("ace_csw_100Rnd_127x99_mag_red")
	};
	linkedItems[] += 
	{
		"CUP_Vector21Nite"
	};
};