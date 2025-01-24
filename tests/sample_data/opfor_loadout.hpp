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
	displayName = "Rifleman";
	uniform[] = 
	{
		"U_I_CombatUniform",
		"U_I_CombatUniform_shortsleeve"
	};
	vest[] = 
	{
		LIST_4("V_PlateCarrierIA1_dgtl"),
		"V_PlateCarrierIA2_dgtl"
	};
	headgear[] = 
	{
		"H_HelmetIA"
	};
	backpack[] = 
	{
		"B_Kitbag_rgr"
	};
	primaryWeapon[] = 
	{
		"arifle_Mk20_F"
	};
	scope[] = 
	{
		"optic_ACO_grn"
	};
	magazines[] = 
	{
		"HandGrenade",
		"SmokeShell",
		LIST_7("30Rnd_556x45_Stanag_red")
	};
};

class ar : rm 
{
	displayName = "Automatic Rifleman";
	primaryWeapon[] = 
	{
		"LMG_Mk200_F"
	};
	magazines[] = 
	{
		"HandGrenade",
		"SmokeShell",
		LIST_5("ACE_200Rnd_65x39_cased_Box_red")
	};
};

class mg : rm 
{
	displayName = "Machine Gunner";
	primaryWeapon[] = 
	{
		"rhs_weap_fnmag"
	};
	magazines[] = 
	{
		"HandGrenade",
		"SmokeShell",
		LIST_3("rhsusf_100Rnd_762x51_m62_tracer")
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

class rm_mat : rm 
{
	displayName = "Rifleman (MAT)";
	secondaryWeapon[] = 
	{
		"fwa_weap_m2_carlgustaf"
	};
	backpackItems[] = 
	{
		LIST_3("fwa_1rnd_m2_carlgustaf_HEAT"),
		"fwa_1rnd_m2_carlgustaf_WP"
	};
};