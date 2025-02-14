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
	items[] = 
	{
		LIST_2("ACE_fieldDressing"),
		"ACE_packingBandage",
		"ACE_quikclot",
		"ACE_tourniquet",
		"ACE_morphine",
		"ACE_splint"
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
	code = "_this call pca_fnc_unlimitedAmmo";
};

class rm : baseMan
{
	displayName = "Rifleman (SKS)";
	uniform[] = 
	{
		"CUP_U_O_TK_Green",
		"CUP_U_O_TK_MixedCamo"
	};
	vest[] = 
	{
		LIST_4("CUP_V_O_TK_Vest_1"),
		"CUP_V_O_SLA_M23_1_OD"
	};
	headgear[] = 
	{
		LIST_3("CUP_H_TK_Helmet"),
		LIST_2("CUP_H_SLA_Helmet_DES")
	};
	goggles[] =
	{
		LIST_3(""),
		"CUP_FR_NeckScarf",
		"CUP_G_Scarf_Face_Grn"
	};
	primaryWeapon[] = 
	{
		"CUP_SKS"
	};
	magazines[] = 
	{
		"rhs_mag_rgd5",
		"rhs_mag_rdg2_white",
		LIST_21("CUP_10Rnd_762x39_SKS_M")
	};
};

class ar : rm 
{
	displayName = "Rifleman (AKM)";
	primaryWeapon[] = 
	{
		"CUP_arifle_AKM_Early"
	};
	magazines[] = 
	{
		"rhs_mag_rgd5",
		"rhs_mag_rdg2_white",
		LIST_13("CUP_30Rnd_762x39_AK47_bakelite_M")
	};
};

class mg : rm 
{
	displayName = "Machinegunner";
	primaryWeapon[] = 
	{
		"rhs_weap_pkm"
	};
	backpack[] =
	{
		"bear_rd54_sand"
	};
	magazines[] = 
	{
		"rhs_mag_rgd5",
		"rhs_mag_rdg2_white",
		LIST_5("rhs_100Rnd_762x54mmR")
	};
};

class rm_lat : rm 
{
	displayName = "Rifleman (LAT)";
	secondaryWeapon[] = 
	{
		"rhs_weap_rpg26"
	};
};

class rm_mat : rm 
{
	displayName = "Rifleman (MAT)";
	backpack[] = 
	{
		"rhs_rk_sht_30_emr",
		"rhs_tortila_emr"
	};
	secondaryWeapon[] = 
	{
		"rhs_weap_rpg7"
	};
	secondaryAttachments[] = 
	{
		"rhs_acc_pgo7v3"
	};
	backpackItems[] = 
	{
		LIST_4("rhs_rpg7_PG7VL_mag"),
		"rhs_rpg7_PG7VR_mag",
		"rhs_rpg7_OG7V_mag"
	};
};

class gren : ar 
{
	displayName = "Grenadier";
	primaryWeapon[] = 
	{
		"CUP_arifle_AKM_GL_Early"
	};
	magazines[] += 
	{
		LIST_3("rhs_VOG25"),
		LIST_2("rhs_GRD40_White")
	};
};

class medic : rm 
{
	displayName = "Medic";
	vest[] = 
	{
		"rhs_6b23_digi_medic"
	};
	backpack[] = 
	{
		"rhs_rk_sht_30_emr",
		"rhs_tortila_emr"
	};
	backpackItems[] = 
	{
		LIST_10("ACE_fieldDressing"),
		LIST_5("ACE_elasticBandage"),
		LIST_5("ACE_packingBandage"),
		LIST_4("ACE_epinephrine"),
		LIST_4("ACE_morphine"),
		LIST_4("ACE_splint"),
		LIST_4("ACE_tourniquet"),
		LIST_2("ACE_bloodIV"),
		LIST_2("ACE_adenosine")
	};
};

class engineer : rm 
{
	displayName = "Engineer";
	backpack[] = 
	{
		"rhs_rk_sht_30_emr_engineer_empty"
	};
	backpackItems[] = 
	{
		"ToolKit",
		"ACE_wirecutter",
		LIST_2("rhs_ec400_sand_mag")
	};
};

class sf : rm 
{
	displayName = "Special Purpose Squad";
	vest[] = 
	{
		"pca_md99_3cd_rifleman_radio",
		LIST_3("pca_md99_3cd_rifleman")
	};
	headgear[] = 
	{
		"wsx_helmet_pasgt_3cd",
		"wsx_helmet_combat_3cd_ess"
	};
	goggles[] +=
	{
		LIST_2("CUP_G_ESS_BLK_Facewrap_Black"),
		"rhsusf_shemagh2_gogg_od",
		"rhsusf_shemagh2_tan"
	};
	primaryWeapon[] = 
	{
		"amf_weap_famas_f1"
	};
	magazines[] = 
	{
		"rhs_mag_rgd5",
		"rhs_mag_rdg2_white",
		LIST_13("amf_25Rnd_556x45_M855A1_F1_Stanag")
	};
};

class vip : ar 
{
	displayName = "Officer";
	headgear[] = 
	{
		"CUP_H_TK_Beret"
	};
	uniform[] =
	{
		"CUP_U_O_TK_Officer"
	};
	vest[] =
	{
		"pca_vest_invisible_kevlar"
	};
	backpack[] = {};
	primaryWeapon[] = 
	{
		"CUP_arifle_AKS_Gold"
	};
};