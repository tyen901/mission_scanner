class baseMan 
{
	displayName = "Unarmed";
	// All Randomized
	uniform[] = {};
	vest[] = {};
	backpack[] = {};
	headgear[] = {};
	goggles[] = {};
	hmd[] = {};
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
	magazines[] = {};
	items[] = {};
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
	uniform[] = 
	{
		LIST_1("U_BG_Guerrilla_6_1"),
		LIST_1("U_BG_Guerilla1_1"),
		LIST_1("U_BG_Guerilla2_2"),
		LIST_1("U_BG_Guerilla2_1"),
		LIST_1("U_BG_Guerilla2_3"),
		LIST_1("U_BG_leader"),
		LIST_1("aegis_guerilla_garb_m81"),
		LIST_1("aegis_sweater_grn"),
		LIST_1("aegis_guerilla_tshirt_m81"),
		LIST_1("aegis_guerilla_tshirt_m81_alt")
	};
	vest[] = 
	{
		LIST_1("milgp_v_mmac_assaulter_belt_cb"),
		LIST_1("milgp_v_mmac_assaulter_belt_rgr"),
		LIST_1("milgp_v_mmac_assaulter_belt_khk")
	};
	headgear[] = 
	{
		LIST_1("pca_headband_blk"),
		LIST_1("pca_headband"),
		LIST_1("pca_headband_red"),
		LIST_1("pca_headband_tan")
	};
	backpack[] = 
	{
		LIST_1("wsx_tacticalpack_oli"),
		LIST_1("aegis_tacticalpack_cbr"),
		LIST_1("rhs_rk_sht_30_olive"),
		LIST_1("rhssaf_kitbag_md2camo")
	};
	goggles[] = 
	{
		LIST_1("G_Bandanna_blk"),
		LIST_1("G_Bandanna_khk"),
		LIST_1("G_Bandanna_oli"),
		LIST_1("bear_bandana_m81")
	};
	primaryWeapon[] = 
	{
		"sfp_weap_ak5c_blk"
	};
	scope[] = 
	{
		"optic_mrco"
	};
	items[] =
	{
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
		LIST_2("rhs_mag_m67"),
		LIST_13("pca_mag_30Rnd_556x45_M855A1_PMAG_Blk")
	};
	backpackItems[] = 
	{
		LIST_4("pca_mag_30Rnd_556x45_M855A1_PMAG_Blk")
	};
};

class ar : rm 
{
	displayName = "Automatic Rifleman";
	primaryWeapon[] = 
	{
		"sps_weap_kac_lamg_hg_blk"
	};
	sidearmWeapon[] = 
	{
		"aegis_weap_fnx45_blk"
	};
	vest[] = 
	{
		LIST_1("milgp_v_mmac_hgunner_belt_cb"),
		LIST_1("milgp_v_mmac_hgunner_belt_rgr"),
		LIST_1("milgp_v_mmac_hgunner_belt_khk")
	};
	backpack[] = 
	{
		"B_Carryall_cbr"
	};
	bipod[] = 
	{
		"CUP_bipod_VLTOR_Modpod_black"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("rhs_mag_m67"),
		LIST_2("11Rnd_45ACP_Mag"),
		LIST_3("sps_200Rnd_556x45_M855A1_Mixed_KAC_Box")
	};
	backpackItems[] = 
	{
		LIST_4("sps_200Rnd_556x45_M855A1_Mixed_KAC_Box")
	};
};

class aar : rm 
{
	displayName = "Assistant Automatic Rifleman";
	backpack[] = 
	{
		"B_Carryall_cbr"
	};
	backpackItems[] += 
	{
		LIST_4("sps_200Rnd_556x45_M855A1_Mixed_KAC_Box")
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
		"fwa_weap_m2_carlgustaf_no78"
	};
	backpack[] = 
	{
		"B_Carryall_cbr"
	};
	backpackItems[] += 
	{
		LIST_4("fwa_1rnd_m2_carlgustaf_HEAT"),
		LIST_1("fwa_1rnd_m2_carlgustaf_HE")
	};
};

class sh : rm 
{
	displayName = "Sharpshooter";
	primaryWeapon[] = 
	{
		"pca_weap_svd_wood_npz"
	};
	sidearmWeapon[] = 
	{
		"aegis_weap_fnx45_blk"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("rhs_mag_f1"),
		LIST_2("11Rnd_45ACP_Mag"),
		LIST_20("rhs_10Rnd_762x54mmR_7N14")
	};
	backpackItems[] = 
	{
		LIST_4("rhs_10Rnd_762x54mmR_7N14")
	};
	scope[] = 
	{
		"cup_optic_sb_3_12x50_pmii_pip"
	};
};

class gren : rm 
{
	displayName = "Grenadier";
	primaryWeapon[] = 
	{
		"sfp_weap_ak5c_m203_blk"
	};
	backpackItems[] = 
	{
		LIST_21("rhs_mag_M441_HE"),
		LIST_21("rhs_mag_M433_HEDP"),
		LIST_4("1Rnd_Smoke_Grenade_shell")
	};
};

class tl : rm 
{
	displayName = "Team Leader";
	primaryWeapon[] = 
	{
		"sfp_weap_ak5c_m203_blk"
	};
	backpackItems[] = 
	{
		LIST_2("pca_mag_30Rnd_556x45_M856A1_PMAG_Blk"),
		LIST_21("rhs_mag_M441_HE"),
		LIST_6("1Rnd_Smoke_Grenade_shell"),
		LIST_2("1Rnd_SmokeGreen_Grenade_shell"),
		LIST_2("1Rnd_SmokeRed_Grenade_shell"),
		LIST_2("rhsusf_m112_mag")
	};
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
	primaryWeapon[] = 
	{
		"sfp_weap_ak5c_m203_blk"
	};
	sidearmWeapon[] = 
	{
		"aegis_weap_fnx45_blk"
	};
	magazines[] += 
	{
		LIST_2("11Rnd_45ACP_Mag")
	};
};

class sgt : sl 
{};

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
		"rhs_rk_sht_30_olive"
	};
	backpackItems[] =
	{
		LIST_20("ACE_fieldDressing"),
		LIST_15("ACE_packingBandage"),
		LIST_15("ACE_elasticBandage"),
		LIST_10("ACE_quikclot"),
		LIST_10("ACE_epinephrine"),
		LIST_10("ACE_morphine"),
		LIST_8("ACE_bloodIV"),
		LIST_4("ACE_splint"),
		LIST_4("ACE_tourniquet"),
		LIST_2("ACE_adenosine"),
		LIST_1("ACE_personalAidKit"),
		LIST_30("ACE_suture")
	};
};

class cls : rm_fa
{
	displayName = "Combat Life Saver";
	sidearmWeapon[] = 
	{
		"aegis_weap_fnx45_blk"
	};
	magazines[] += 
	{
		LIST_2("11Rnd_45ACP_Mag")
	};
	backpackItems[] =
	{
		"ACE_surgicalKit",
		LIST_30("ACE_elasticBandage"),
		LIST_30("ACE_packingBandage"),
		LIST_20("ACE_fieldDressing"),
		LIST_10("ACE_quikclot"),
		LIST_20("ACE_epinephrine"),
		LIST_20("ACE_morphine"),
		LIST_12("ACE_bloodIV"),
		LIST_10("ACE_splint"),
		LIST_4("ACE_tourniquet"),
		LIST_2("ACE_adenosine"),
		LIST_1("ACE_personalAidKit")
	};
};

class mmg : rm 
{
	displayName = "Medium Machine Gunner";
	backpack[] = 
	{
		"rhs_rk_sht_30_olive"
	};
	primaryWeapon[] = 
	{
		"sps_weap_kac_amg_blk"
	};
	sidearmWeapon[] = 
	{
		"aegis_weap_fnx45_blk"
	};
	bipod[] = 
	{
		"CUP_bipod_VLTOR_Modpod_black"
	};
	magazines[] = 
	{
		LIST_2("SmokeShell"),
		LIST_2("rhs_mag_m67"),
		LIST_2("11Rnd_45ACP_Mag"),
		LIST_3("rhsusf_100Rnd_762x51_m80a1epr")
	};
	backpackItems[] = 
	{
		LIST_6("rhsusf_100Rnd_762x51_m80a1epr")
	};
};

class ammg : rm 
{
	displayName = "Assistant Medium Machine Gunner";
	backpack[] = 
	{
		"rhs_rk_sht_30_olive"
	};
	sidearmWeapon[] = 
	{
		"aegis_weap_fnx45_blk"
	};
	magazines[] += 
	{
		LIST_2("11Rnd_45ACP_Mag")
	};
	backpackItems[] = 
	{
		LIST_8("rhsusf_100Rnd_762x51_m80a1epr")
	};
	linkedItems[] += 
	{
		"Binocular"
	};
};

class drone : rm 
{
	displayName = "Drone Operator";
	linkedItems[] = 
	{
		"B_UavTerminal"
	};
	backpack[] = 
	{
		"B_UAV_01_backpack_F"
	};
	sidearmWeapon[] = 
	{
		"aegis_weap_fnx45_blk"
	};
	magazines[] += 
	{
		LIST_2("11Rnd_45ACP_Mag")
	};
};
