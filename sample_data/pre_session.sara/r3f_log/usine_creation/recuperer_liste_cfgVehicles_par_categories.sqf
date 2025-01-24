/**
 * Récupère les liste des catégories (CfgVehicleClasses) et pour chacune d'elles les véhicules associés (CfgVehicles)
 * 
 * @param 0 (optionnel) l'éventuelle usine pour laquelle récupérer les catégories autorisées (en fonction de la white ou black list)
 * @param 1 (optionnel) true pour conserver les catégories vides (càd sans entrée dans le CfgVehicles) (défaut : false)
 * 
 * @return tableau au format [tableau des catégories, tableau 2D des véhicules associés à chaque catégorie]
 * 
 * Copyright (C) 2014 Team ~R3F~
 * 
 * This program is free software under the terms of the GNU General Public License version 3.
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
//categories// input
//_cars = ["B_G_Van_01_transport_F","B_Quadbike_01_F"];

//private _classes = ([] apply {[_x] append ([_x] call BIS_fnc_objectType)}) select {(_x select 1) isEqualTo "Vehicle"};

_cars = [];
_air = [];
_armour = [];

_cccc = 0 spawn {
	uiSleep 15;
	if ([] call BIS_fnc_isLoading) then {
		endLoadingScreen;
	};
};
startLoadingScreen ["Generating Vehicle Lists"];

private _cars_u = ("( 
    (getNumber (_x >> 'scope') >= 2) &&
    {(tolower getText (_x >> 'simulation')) in ['car', 'carx', 'motorcycle']} &&
	{!((configName _x) isKindOf 'rhs_9k79_B')}
)" configClasses (configFile >> "CfgVehicles")) apply {[(toLower (getText (_x >> 'displayName'))), configName _x]};

{
	private _first = _cars_u select 0;
	private _test = [];
	{
		_test = [_first select 0, _x select 0];
		_test sort true;
		if !((_test select 0) isEqualTo (_first select 0)) then { 
			_first = _x;
		};
	} forEach _cars_u;
	_cars pushBack (_first select 1);
	_cars_u = _cars_u - [_first];
} forEach _cars_u;

progressLoadingScreen 0.33;

private _air_u = ("( 
    (getNumber (_x >> 'scope') >= 2) &&
    {(tolower getText (_x >> 'simulation')) in ['airplane', 'airplanex', 'helicopter', 'helicopterrtd', 'helicopterx']} &&
	{!((configName _x) isKindOf 'RHS_C130J_Base' || (configName _x) isKindOf 'RHS_TU95MS_base')}
)" configClasses (configFile >> "CfgVehicles")) apply {[(toLower (getText (_x >> 'displayName'))), configName _x]};

{
	private _first = _air_u select 0;
	private _test = [];
	{
		_test = [_first select 0, _x select 0];
		_test sort true;
		if !((_test select 0) isEqualTo (_first select 0)) then { 
			_first = _x;
		};
	} forEach _air_u;
	_air pushBack (_first select 1);
	_air_u = _air_u - [_first];
} forEach _air_u;

progressLoadingScreen 0.67;

private _armour_u = ("( 
    (getNumber (_x >> 'scope') >= 2) &&
    {(tolower getText (_x >> 'simulation')) in ['tank', 'tankx']} &&
	{!((configName _x) iskindof 'StaticWeapon')}
)" configClasses (configFile >> "CfgVehicles")) apply {[(toLower (getText (_x >> 'displayName'))), configName _x]};

{
	private _first = _armour_u select 0;
	private _test = [];
	{
		_test = [_first select 0, _x select 0];
		_test sort true;
		if !((_test select 0) isEqualTo (_first select 0)) then { 
			_first = _x;
		};
	} forEach _armour_u;
	_armour pushBack (_first select 1);
	_armour_u = _armour_u - [_first];
} forEach _armour_u;

progressLoadingScreen 1;
endLoadingScreen;

/*{
	switch (_x select 2) do {
		case "WheeledAPC";
		case "Car": {
			_cars pushBack (_x select 0);
		};
		case "Helicopter";
		case "Plane": {
			_air pushBack (_x select 0);
		};
	};
} forEach _classes;*/

//_cars = ["bear_tka_uaz","bear_tka_uaz_ags30","bear_tka_uaz_dshkm","bear_tka_uaz_open","bear_tka_uaz_spg9","bear_aaf_m1025_od_m2","bear_aaf_m1025_od_mk19","B_G_Van_01_transport_F","CAF_AG_afr_p_van_01","CAF_AG_afr_p_Offroad","CAF_AG_afr_p_Offroad_armed_01","CAF_AG_eeur_r_van_01","CAF_AG_eeur_r_Offroad","CAF_AG_eeur_r_Offroad_armed_01","CAF_AG_ME_T_van_01","CAF_AG_ME_T_Offroad","CAF_AG_ME_T_Offroad_armed_01","B_MRAP_01_F","B_MRAP_01_gmg_F","B_MRAP_01_hmg_F","O_MRAP_02_F","O_MRAP_02_hmg_F","O_MRAP_02_gmg_F","C_Offroad_01_F","B_G_Offroad_01_F","B_G_Offroad_01_armed_F","B_Quadbike_01_F","O_Quadbike_01_F","C_Quadbike_01_F","I_Quadbike_01_F","B_G_Quadbike_01_F","I_MRAP_03_F","I_MRAP_03_hmg_F","I_MRAP_03_gmg_F","B_Truck_01_transport_F","B_Truck_01_covered_F","O_Truck_02_covered_F","O_Truck_02_transport_F","I_Truck_02_covered_F","I_Truck_02_transport_F","O_Truck_03_transport_F","O_Truck_03_covered_F","O_Truck_03_device_F","C_Hatchback_01_F","C_Hatchback_01_sport_F","C_SUV_01_F","B_Truck_01_mover_F","B_Truck_01_box_F","C_Van_01_transport_F","C_Van_01_box_F","C_Kart_01_F","C_Kart_01_Fuel_F","C_Kart_01_Blu_F","C_Kart_01_Red_F","C_Kart_01_Vrana_F","BAF_Offroad_D","BAF_Offroad_W","LandRover_CZ_EP1","LandRover_ACR","LandRover_TK_CIV_EP1","LandRover_MG_TK_EP1","BAF_Offroad_W_HMG","BAF_Offroad_D_HMG","ACR_Offroad_HMG","rhs_tigr_vdv","rhs_tigr_vmf","rhs_tigr_msv","rhs_tigr_vv","rhsusf_m998_w_2dr","rhsusf_m998_d_2dr","rhsusf_m998_w_s_2dr","rhsusf_m998_d_s_2dr","rhsusf_m998_w_2dr_halftop","rhsusf_m998_d_2dr_halftop","rhsusf_m998_w_s_2dr_halftop","rhsusf_m998_d_s_2dr_halftop","rhsusf_m998_w_2dr_fulltop","rhsusf_m998_d_2dr_fulltop","rhsusf_m998_w_s_2dr_fulltop","rhsusf_m998_d_s_2dr_fulltop","rhsusf_m998_w_4dr","rhsusf_m998_d_4dr","rhsusf_m998_w_s_4dr","rhsusf_m998_d_s_4dr","rhsusf_m998_w_4dr_halftop","rhsusf_m998_d_4dr_halftop","rhsusf_m998_w_s_4dr_halftop","rhsusf_m998_d_s_4dr_halftop","rhsusf_m998_w_4dr_fulltop","rhsusf_m998_d_4dr_fulltop","rhsusf_m998_w_s_4dr_fulltop","rhsusf_m998_d_s_4dr_fulltop","rhsusf_m1025_w","rhsusf_m1025_d","rhsusf_m1025_w_s","rhsusf_m1025_d_s","rhsusf_m1025_w_m2","rhsusf_m1025_d_m2","rhsusf_m1025_w_s_m2","rhsusf_m1025_d_s_m2","rhsusf_m1025_w_mk19","rhsusf_m1025_d_Mk19","rhsusf_m1025_w_s_Mk19","rhsusf_m1025_d_s_Mk19","UK3CB_BAF_Jackal2_L2A1_D","UK3CB_BAF_Jackal2_GMG_D","UK3CB_BAF_Jackal2_GMG_W","UK3CB_BAF_Jackal2_L2A1_W","RDS_Ikarus_Civ_01","RDS_Ikarus_Civ_02","RDS_Lada_Civ_01","RDS_Lada_Civ_02","RDS_Lada_Civ_03","RDS_Lada_Civ_04","RDS_Lada_Civ_05","RDS_S1203_Civ_01","RDS_S1203_Civ_02","RDS_S1203_Civ_03","RDS_Gaz24_Civ_01","RDS_Gaz24_Civ_02","RDS_Gaz24_Civ_03","RDS_Golf4_Civ_01","RDS_Octavia_Civ_01","RDS_Hatchback_01_F","RDS_SUV_01_F","RDS_Van_01_transport_F","RDS_Van_01_box_F","RHS_UAZ_MSV_01","rhs_uaz_vdv","rhs_uaz_vmf","rhs_uaz_vv","rhs_uaz_open_MSV_01","rhs_uaz_open_vdv","rhs_uaz_open_vmf","rhs_uaz_open_vv","RHS_Ural_MSV_01","RHS_Ural_VDV_01","RHS_Ural_VMF_01","RHS_Ural_VV_01","RHS_Ural_Open_MSV_01","RHS_Ural_Open_VDV_01","RHS_Ural_Open_VMF_01","RHS_Ural_Open_VV_01","RHS_Ural_Fuel_MSV_01","RHS_Ural_Fuel_VDV_01","RHS_Ural_Fuel_VMF_01","RHS_Ural_Fuel_VV_01","RHS_BM21_MSV_01","RHS_BM21_VDV_01","RHS_BM21_VMF_01","RHS_BM21_VV_01","RHS_Civ_Truck_02_covered_F","RHS_Civ_Truck_02_transport_F","rhs_typhoon_vdv","rhs_gaz66_vmf","rhs_gaz66o_vmf","rhs_gaz66_vdv","rhs_gaz66o_vdv","rhs_gaz66_vv","rhs_gaz66o_vv","rhs_gaz66_msv","rhs_gaz66o_msv","rhs_gaz66_r142_vmf","rhs_gaz66_r142_vdv","rhs_gaz66_r142_msv","rhs_gaz66_r142_vv","rhs_gaz66_repair_vmf","rhs_gaz66_repair_vdv","rhs_gaz66_repair_vv","rhs_gaz66_repair_msv","rhs_gaz66_ap2_vmf","rhs_gaz66_ap2_vdv","rhs_gaz66_ap2_vv","rhs_gaz66_ap2_msv","rhs_gaz66_ammo_vmf","rhs_gaz66_ammo_vdv","rhs_gaz66_ammo_vv","rhs_gaz66_ammo_msv","rhs_tigr_3camo_vdv","rhs_tigr_sts_vdv","rhs_tigr_sts_vdv","rhs_tigr_sts_3camo_vdv","rhs_tigr_m_vdv","rhs_tigr_m_vdv","rhs_gaz66_zu23_msv","RHS_Ural_Zu23_MSV_01","rhsusf_M1078A1P2_wd_fmtv_usarmy","rhsusf_M1078A1P2_wd_open_fmtv_usarmy","rhsusf_M1078A1P2_B_wd_fmtv_usarmy","rhsusf_M1078A1P2_B_M2_wd_fmtv_usarmy","rhsusf_M1078A1P2_B_M2_wd_open_fmtv_usarmy","rhsusf_M1083A1P2_wd_fmtv_usarmy","rhsusf_M1083A1P2_wd_open_fmtv_usarmy","rhsusf_M1083A1P2_B_wd_fmtv_usarmy","rhsusf_M1083A1P2_B_M2_wd_fmtv_usarmy","rhsusf_M1083A1P2_B_M2_wd_open_fmtv_usarmy","rhsusf_M1083A1P2_B_wd_open_fmtv_usarmy","rhsusf_M977A4_usarmy_wd","rhsusf_M977A4_AMMO_usarmy_wd","rhsusf_M977A4_REPAIR_usarmy_wd","rhsusf_M977A4_BKIT_usarmy_wd","rhsusf_M977A4_AMMO_BKIT_usarmy_wd","rhsusf_M977A4_BKIT_M2_usarmy_wd","rhsusf_M977A4_AMMO_BKIT_M2_usarmy_wd","rhsusf_M977A4_REPAIR_BKIT_M2_usarmy_wd","rhsusf_M977A4_REPAIR_BKIT_usarmy_wd","rhsusf_M978A4_usarmy_wd","rhsusf_M978A4_BKIT_usarmy_wd","rhsusf_M1117_W","rhsusf_M978A4_usarmy_d","rhsusf_M978A4_BKIT_usarmy_d","rhsusf_M977A4_usarmy_d","rhsusf_M977A4_BKIT_usarmy_d","rhsusf_M977A4_REPAIR_BKIT_usarmy_d","rhsusf_M977A4_REPAIR_BKIT_M2_usarmy_d","rhsusf_M977A4_AMMO_BKIT_M2_usarmy_d","rhsusf_M977A4_BKIT_M2_usarmy_d","rhsusf_M977A4_AMMO_BKIT_usarmy_d","rhsusf_M977A4_REPAIR_usarmy_d","rhsusf_M977A4_AMMO_usarmy_d","rhsusf_M1083A1P2_B_d_open_fmtv_usarmy","rhsusf_M1083A1P2_B_M2_d_open_fmtv_usarmy","rhsusf_M1083A1P2_B_M2_d_fmtv_usarmy","rhsusf_M1083A1P2_B_d_fmtv_usarmy","rhsusf_M1083A1P2_d_open_fmtv_usarmy","rhsusf_M1083A1P2_B_M2_d_MHQ_fmtv_usarmy","rhsusf_M1083A1P2_B_M2_d_Medical_fmtv_usarmy","rhsusf_M1083A1P2_d_fmtv_usarmy","rhsusf_M1078A1P2_B_d_open_fmtv_usarmy","rhsusf_M1078A1P2_B_M2_d_open_fmtv_usarmy","rhsusf_M1078A1P2_B_M2_d_fmtv_usarmy","rhsusf_M1078A1P2_B_d_fmtv_usarmy","rhsusf_M1078A1P2_d_open_fmtv_usarmy","rhsusf_M1078A1P2_d_fmtv_usarmy","rhsusf_M1117_O","rhsusf_M1117_D"];
//_air = ["bear_tka_Mi24P_CAS","bear_tka_Mi24P","bear_tka_Mi8AMT","bear_tka_Mi8AMTSh","bear_tka_Mi8AMTSh_FAB","bear_tka_Mi8mt","bear_tka_Mi8mt_Cargo","bear_tka_l159_CAS","bear_tka_l39","bear_tka_Su25SM","bear_tka_Su25SM_CAS","bear_ka60_c_pla","bear_ka60_grey_pla","bear_mi24g_CAS_pla","bear_mi24g_UPK23_pla","bear_mi24g_FAB_pla","bear_Mi8mt_pla","bear_Mi8mt_Cargo_pla","bear_Mi8MTV3_pla","bear_Mi8AMT_pla","bear_Su25SM_pla","bear_Su25SM_KH29_pla","bear_Su25SM_CAS_pla","Cha_AV8B2","Cha_AV8B","Cha_AV8B3","Cha_GR7","Cha_GR9","FIR_F16C","FIR_F16C_ROKAF","FIR_F16C_Polish","FIR_F16C_TWAS","B_Heli_Light_01_F","B_Heli_Light_01_armed_F","C_Heli_Light_01_civil_F","O_Heli_Light_02_F","O_Heli_Light_02_unarmed_F","O_Heli_Light_02_v2_F","B_Heli_Attack_01_F","O_Heli_Attack_02_F","O_Heli_Attack_02_black_F","B_Heli_Transport_01_F","B_Heli_Transport_01_camo_F","I_Heli_Transport_02_F","I_Heli_light_03_F","I_Heli_light_03_unarmed_F","B_Plane_CAS_01_F","O_Plane_CAS_02_F","I_Plane_Fighter_03_CAS_F","I_Plane_Fighter_03_AA_F","B_Heli_Transport_03_F","B_Heli_Transport_03_unarmed_F","O_Heli_Transport_04_F","O_Heli_Transport_04_ammo_F","O_Heli_Transport_04_bench_F","O_Heli_Transport_04_box_F","O_Heli_Transport_04_covered_F","O_Heli_Transport_04_fuel_F","O_Heli_Transport_04_medevac_F","O_Heli_Transport_04_repair_F","CHO_F35B_AA","CHO_F35B_CAS","CHO_F35B_LGB","UK3CB_BAF_Vehicles_Merlin_RAF_ZJ124","UK3CB_BAF_Wildcat_Transport_RN_ZZ396","UK3CB_BAF_Wildcat_Armed_Army_ZZ400","RHS_Mi24P_vvs","RHS_Mi24P_vvsc","RHS_Mi24P_vdv","RHS_Mi24V_vvs","RHS_Mi24V_vvsc","RHS_Mi24Vt_vvs","RHS_Mi24V_vdv","RHS_Mi8mt_vvs","RHS_Mi8mt_vvsc","RHS_Mi8mt_vdv","RHS_Mi8mt_vv","RHS_Mi8MTV3_vvs","RHS_Mi8MTV3_vvsc","RHS_Mi8MTV3_vdv","RHS_Mi8AMT_vvs","RHS_Mi8AMT_vvsc","RHS_Mi8AMT_vdv","RHS_Mi8AMTSh_vvs","RHS_Mi8AMTSh_vvsc","RHS_Mi8amt_civilian","RHS_Su25SM_vvs","RHS_Su25SM_vvsc","RHS_Ka52_vvsc","RHS_Ka52_vvs","rhs_ka60_grey","rhs_ka60_c","RHS_AH64D","RHS_CH_47F","RHS_CH_47F_light","RHS_UH60M","RHS_UH60M_MEV","RHS_A10","RHS_Ka52_UPK23_vvs","RHS_Ka52_UPK23_vvsc","RHS_Mi24P_AT_vvs","RHS_Mi24P_CAS_vvs","RHS_Mi24V_AT_vvs","RHS_Mi24V_FAB_vvs","RHS_Mi24V_UPK23_vvs","RHS_Mi24V_UPK23_vvsc","RHS_Mi24V_FAB_vvsc","RHS_Mi24V_AT_vvsc","RHS_Mi24P_CAS_vvsc","RHS_Mi24P_AT_vvsc","RHS_Mi8AMTSh_FAB_vvsc","RHS_Mi8AMTSh_UPK23_vvsc","RHS_Mi8MTV3_FAB_vvsc","RHS_Mi8MTV3_UPK23_vvsc","RHS_Mi24Vt_vvsc","RHS_T50_vvs_blueonblue","RHS_T50_vvs_054","RHS_T50_vvs_053","RHS_T50_vvs_052","RHS_T50_vvs_051","RHS_T50_vvs_generic","RHS_Su25SM_KH29_vvs","RHS_Su25SM_CAS_vvs","RHS_Su25SM_KH29_vvsc","RHS_Su25SM_CAS_vvsc","RHS_AH64D_AA","RHS_AH64D_CS","RHS_AH64D_GS","RHS_AH64DGrey","RHS_UH60M_MEV2_d","RHS_MELB_AH6M_H","RHS_MELB_AH6M_L","RHS_MELB_AH6M_M","RHS_MELB_MH6M","RHS_MELB_H6M","RHS_A10_AT","RHS_C130J","rhsusf_f22","RHS_AH1Z_CS","RHS_AH1Z_GS","RHS_AH1Z","rhsusf_CH53E_USMC_D","RHS_UH1Y_FFAR_d","RHS_UH1Y_d","RHS_UH1Y_d_GS","RHS_UH1Y_UNARMED_d"];
//_armour = ["bear_tka_zsu234","bear_tka_btr60","bear_tka_bmp1","bear_tka_bmp1d","bear_tka_bmp1k","bear_tka_bmp1p","bear_tka_bmp2","bear_tka_bmp2e","bear_tka_bmp2d","bear_tka_bmp2k","bear_tka_prp3","bear_tka_BRDM2","bear_tka_BRDM2_ATGM","bear_tka_BRDM2UM","bear_tka_BRDM2_HQ","bear_tka_t72bb","bear_tka_t72ba","bear_aaf_m113","AAVB","Burnes_aav_des","Cha_LAV25","Cha_LAV25A2","Cha_LAV25_HQ","B_APC_Tracked_01_rcws_F","B_APC_Tracked_01_AA_F","O_APC_Tracked_02_cannon_F","O_APC_Tracked_02_AA_F","I_APC_tracked_03_cannon_F","I_MBT_03_cannon_F","B_MBT_01_cannon_F","B_MBT_01_arty_F","B_MBT_01_mlrs_F","O_MBT_02_cannon_F","O_MBT_02_arty_F","Burnes_M1A2_MEU_01_Public","Burnes_M1A2_MEU_02_Public","Burnes_M1A2_MEU_03_Public","Burnes_M1A2_MEU_04_Public","B_APC_Wheeled_01_cannon_F","RHS_M2A2","RHS_M2A2_BUSKI","RHS_M2A3","RHS_M2A3_BUSKI","RHS_M2A3_BUSKIII","RHS_M2A3_BUSKIII_wd","RHS_M6","RHS_M2A2_wd","RHS_M2A2_BUSKI_WD","RHS_M2A3_BUSKI_wd","RHS_M2A3_wd","RHS_M6_wd","rhsusf_m109_usarmy","rhsusf_m109d_usarmy","rhsusf_m1a1aimwd_usarmy","rhsusf_m1a1aimd_usarmy","rhsusf_m1a1aim_tuski_wd","rhsusf_m1a1aim_tuski_d","rhsusf_m1a1fep_d","rhsusf_m1a1fep_wd","rhsusf_m1a2sep1d_usarmy","rhsusf_m1a2sep1wd_usarmy","rhsusf_m1a2sep1tuskid_usarmy","rhsusf_m1a2sep1tuskiwd_usarmy","O_APC_Wheeled_02_rcws_F","B_MBT_01_TUSK_F","I_APC_Wheeled_03_cannon_F","Burnes_FV4034_01","Burnes_FV4034_02","Burnes_FV4034_03","Burnes_FV4034_05","rhs_2s3_tv","rhs_bmd1","rhs_bmd1k","rhs_bmd1p","rhs_bmd1pk","rhs_bmd1r","rhs_bmd2","rhs_bmd2m","rhs_bmd2k","rhs_bmp1_vdv","rhs_bmp1_tv","rhs_bmp1_msv","rhs_bmp1_vmf","rhs_bmp1_vv","rhs_bmp1p_vdv","rhs_bmp1p_tv","rhs_bmp1p_msv","rhs_bmp1p_vmf","rhs_bmp1p_vv","rhs_bmp1k_vdv","rhs_bmp1k_tv","rhs_bmp1k_msv","rhs_bmp1k_vmf","rhs_bmp1k_vv","rhs_bmp1d_vdv","rhs_bmp1d_tv","rhs_bmp1d_msv","rhs_bmp1d_vmf","rhs_bmp1d_vv","rhs_prp3_vdv","rhs_prp3_tv","rhs_prp3_msv","rhs_prp3_vmf","rhs_prp3_vv","rhs_bmp2e_vdv","rhs_bmp2e_tv","rhs_bmp2e_msv","rhs_bmp2e_vmf","rhs_bmp2e_vv","rhs_bmp2_vdv","rhs_bmp2_tv","rhs_bmp2_msv","rhs_bmp2_vmf","rhs_bmp2_vv","rhs_bmp2k_vdv","rhs_bmp2k_tv","rhs_bmp2k_msv","rhs_bmp2k_vmf","rhs_bmp2k_vv","rhs_bmp2d_vdv","rhs_bmp2d_tv","rhs_bmp2d_msv","rhs_bmp2d_vmf","rhs_bmp2d_vv","rhs_brm1k_vdv","rhs_brm1k_tv","rhs_brm1k_msv","rhs_brm1k_vmf","rhs_brm1k_vv","rhs_btr70_vmf","rhs_btr70_vdv","rhs_btr70_vv","rhs_btr70_msv","rhs_btr80_msv","rhs_btr80_vdv","rhs_btr80_vv","rhs_btr80_vmf","rhs_btr80a_msv","rhs_btr80a_vdv","rhs_btr80a_vv","rhs_btr80a_vmf","rhs_sprut_vdv","rhs_bmd4_vdv","rhs_bmd4m_vdv","rhs_bmd4ma_vdv","rhs_t72ba_tv","rhs_t72bb_tv","rhs_t72bc_tv","rhs_t72bd_tv","rhs_t80b","rhs_t80bk","rhs_t80bv","rhs_t80bvk","rhs_t80","rhs_t80a","rhs_t80u","rhsusf_m113_usarmy","rhsusf_m113d_usarmy","rhs_btr60_vmf","rhs_btr60_vdv","rhs_btr60_vv","rhs_btr60_msv","rhs_zsu234_aa","rhs_zsu234_chdkz","rhs_bmd2_chdkz","rhs_btr70_chdkz","rhs_t72bb_chdkz","rhs_t90_tv","rhs_t90a_tv","rhs_t80u45m","rhs_t80ue1","rhs_Ob_681_2"];

[["Car","Air","Armored"],[_cars,_air,_armour]]