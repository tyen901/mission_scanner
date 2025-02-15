from pathlib import Path
from mission_scanner.parsers.sqf_parser import SqfParser
from .conftest import SAMPLE_DATA

def test_parse_real_curated_gear():
    parser = SqfParser()
    sample_file = SAMPLE_DATA / "example_curatedgear.sqf"
    
    result = parser.parse(sample_file)
    found_items = {eq.name for eq in result.equipment}
    
    # Expected equipment from example_curatedgear.sqf
    expected_items = {
        "rhs_tsh4",  # Crew helmet
        "rhs_rpg_empty",  # RPG backpack
        "rhs_weap_rpg7",  # RPG weapon
        "rhs_rpg7_PG7VL_mag",  # RPG ammo
        "ACE_fieldDressing",
        "ACE_packingBandage", 
        "ACE_epinephrine",
        "ACE_morphine",
        "ACE_tourniquet",
        "ACE_splint",
        "rhs_mag_rgd5",  # Grenade
        "rhs_mag_rdg2_white"  # Smoke grenade
    }
    
    # Verify all expected items are found
    assert expected_items.issubset(found_items), \
        f"Missing items: {expected_items - found_items}"

    # Verify no face/head references are included
    head_items = {item for item in found_items if item.startswith('WhiteHead_')}
    assert not head_items, f"Found face references that should be filtered: {head_items}"

def test_parse_mission_inventory():
    """Test parsing equipment from mission.sqm inventory blocks"""
    parser = SqfParser()
    sample_file = SAMPLE_DATA / "example_mission.sqm"
    
    result = parser.parse(sample_file)
    found_items = {eq.name for eq in result.equipment}
    
    # Expected items from example_mission.sqm inventory blocks
    expected_items = {
        "CUP_srifle_LeeEnfield",
        "CUP_optic_no23mk2",
        "CUP_10x_303_M",
        "rhssaf_zrak_rd7j",
        "TC_U_aegis_guerilla_garb_m81_sudan",
        "ACRE_BF888S",
        "ACE_fieldDressing",
        "ACE_packingBandage",
        "ACE_tourniquet",
        "ACE_epinephrine",
        "ACE_morphine",
        "ACE_splint",
        "simc_vest_pasgt_lc2_alt_od3",
        "SmokeShell",
        "rhs_mag_m67",
        "pca_eagle_a3_od",
        "simc_pasgt_m81",
        # MG kit items
        "rhs_weap_mg42",
        "rhsgref_50Rnd_792x57_SmE_drum",
        "rhsusf_weap_glock17g4",
        "rhsusf_mag_17Rnd_9x19_JHP",
        "rhsusf_spcs_ocp_saw"
    }
    
    # Verify all expected items are found
    assert expected_items.issubset(found_items), \
        f"Missing items: {expected_items - found_items}"

def test_parse_curated_arsenal():
    """Test parsing equipment from curated arsenal definitions"""
    parser = SqfParser()
    sample_file = SAMPLE_DATA / "example_curatedarsenal.sqf"
    
    result = parser.parse(sample_file)
    found_items = {eq.name for eq in result.equipment}
    
    # Test sampling of expected equipment categories from arsenal
    expected_items = {
        "11Rnd_45ACP_Mag",
        "1Rnd_Smoke_Grenade_shell",
        "1Rnd_SmokeBlue_Grenade_shell",
        "1Rnd_SmokeGreen_Grenade_shell",
        "1Rnd_SmokeOrange_Grenade_shell",
        "1Rnd_SmokePurple_Grenade_shell",
        "1Rnd_SmokeRed_Grenade_shell",
        "1Rnd_SmokeYellow_Grenade_shell",
        "ACE_40mm_Flare_green",
        "ACE_40mm_Flare_red",
        "ACE_40mm_Flare_white",
        "ACE_adenosine",
        "ACE_bloodIV_250",
        "ACE_bloodIV_500",
        "ACE_bloodIV",
        "ACE_Clacker",
        "ACE_DefusalKit",
        "ACE_elasticBandage",
        "ACE_EntrenchingTool",
        "ACE_epinephrine",
        "ACE_fieldDressing",
        "ACE_M26_Clacker",
        "ACE_MapTools",
        "ACE_morphine",
        "ace_optic_arco_2d",
        "ace_optic_hamr_2d",
        "ace_optic_mrco_2d",
        "ACE_packingBandage",
        "ACE_plasmaIV_250",
        "ACE_plasmaIV_500",
        "ACE_plasmaIV",
        "ACE_quikclot",
        "ACE_RangeCard",
        "ACE_salineIV_250",
        "ACE_salineIV_500",
        "ACE_salineIV",
        "ACE_splint",
        "ACE_surgicalKit",
        "ACE_tourniquet",
        "ACE_wirecutter",
        "ACRE_PRC117F",
        "ACRE_PRC148",
        "ACRE_PRC152",
        "ACRE_PRC343",
        "aegis_bandanna_kawaii",
        "aegis_boonie_blk",
        "aegis_guerilla_garb_m81",
        "aegis_guerilla_jacket_m81",
        "aegis_guerilla_tshirt_m81_alt",
        "aegis_guerilla_tshirt_m81",
        "aegis_merc_polo_blu",
        "aegis_merc_polo_camo",
        "aegis_merc_polo_m81",
        "aegis_merc_tshirt_blk",
        "aegis_shemag_cbr",
        "aegis_shemag_khk",
        "aegis_shemag_oli",
        "aegis_shemag_red",
        "aegis_shemag_shades_cbr",
        "aegis_shemag_shades_khk",
        "aegis_shemag_shades_oli",
        "aegis_shemag_shades_red",
        "aegis_shemag_shades_tan",
        "aegis_shemag_shades_white",
        "aegis_shemag_tactical_cbr",
        "aegis_shemag_tactical_khk",
        "aegis_shemag_tactical_oli",
        "aegis_shemag_tactical_red",
        "aegis_shemag_tactical_tan",
        "aegis_shemag_tactical_white",
        "aegis_shemag_tan",
        "aegis_shemag_white",
        "aegis_sweater_grn",
        "aegis_tacticalpack_cbr",
        "aegis_tacticalpack_khk",
        "aegis_weap_fnx45_blk",
        "B_Carryall_cbr",
        "B_Carryall_khk",
        "B_Carryall_oli",
        "B_Kitbag_cbr",
        "B_Kitbag_rgr",
        "bear_balaclava1_black",
        "bear_bandana_m81",
        "Binocular",
        "CUP_bipod_VLTOR_Modpod_black",
        "CUP_G_TK_RoundGlasses_blk",
        "CUP_G_TK_RoundGlasses_gold",
        "CUP_G_TK_RoundGlasses",
        "CUP_H_FR_BandanaGreen",
        "cup_optic_acog_ta01b_black",
        "cup_optic_acog_ta01b_coyote",
        "cup_optic_elcan_specterdr_black",
        "cup_optic_sb_3_12x50_pmii_pip",
        "fwa_1rnd_m2_carlgustaf_HE",
        "fwa_1rnd_m2_carlgustaf_HEAT",
        "fwa_1rnd_m2_carlgustaf_WP",
        "fwa_weap_m2_carlgustaf_no78",
        "G_Aviator",
        "G_Balaclava_blk",
        "G_Balaclava_BlueStrips",
        "G_Bandanna_aviator",
        "G_Bandanna_beast",
        "G_Bandanna_blk",
        "G_Bandanna_BlueFlame1",
        "G_Bandanna_CandySkull",
        "G_Bandanna_khk",
        "G_Bandanna_oli",
        "G_Bandanna_RedFlame1",
        "G_Bandanna_shades",
        "G_Bandanna_sport",
        "G_Bandanna_Vampire_01",
        "G_Combat",
        "G_Shades_Black",
        "G_Shades_Blue",
        "G_Shades_Green",
        "G_Shades_Red",
        "G_Spectacles_Tinted",
        "G_Spectacles",
        "G_Sport_Blackred",
        "G_Sport_BlackWhite",
        "G_Sport_Blackyellow",
        "G_Sport_Checkered",
        "G_Sport_Greenblack",
        "G_Sport_Red",
        "G_Squares_Tinted",
        "G_Squares",
        "H_Bandanna_blu",
        "H_Bandanna_cbr",
        "H_Bandanna_gry",
        "H_Bandanna_khk_hs",
        "H_Bandanna_khk",
        "H_Beret_blk",
        "H_Booniehat_khk",
        "H_Booniehat_oli",
        "H_Booniehat_tan",
        "H_Shemag_olive",
        "H_ShemagOpen_khk",
        "H_ShemagOpen_tan",
        "ItemCompass",
        "ItemMap",
        "ItemWatch",
        "milgp_f_face_shield_blk",
        "milgp_f_face_shield_cb",
        "milgp_f_face_shield_khk",
        "milgp_f_face_shield_rgr",
        "milgp_f_face_shield_shades_blk",
        "milgp_f_face_shield_shades_cb",
        "milgp_f_face_shield_shades_khk",
        "milgp_f_face_shield_shades_rgr",
        "milgp_f_face_shield_shades_shemagh_blk",
        "milgp_f_face_shield_shades_shemagh_cb",
        "milgp_f_face_shield_shades_shemagh_khk",
        "milgp_f_face_shield_shades_shemagh_rgr",
        "milgp_f_face_shield_shades_shemagh_tan",
        "milgp_f_face_shield_shades_tan",
        "milgp_f_face_shield_shemagh_blk",
        "milgp_f_face_shield_shemagh_cb",
        "milgp_f_face_shield_shemagh_khk",
        "milgp_f_face_shield_shemagh_rgr",
        "milgp_f_face_shield_shemagh_tan",
        "milgp_f_face_shield_tan",
        "milgp_h_cap_01_cb",
        "milgp_h_cap_01_gry",
        "milgp_h_cap_01_khk",
        "milgp_h_cap_01_tan",
        "milgp_h_cap_backwards_01_cb",
        "milgp_h_cap_backwards_01_gry",
        "milgp_h_cap_backwards_01_khk",
        "milgp_h_cap_backwards_01_tan",
        "milgp_v_mmac_assaulter_belt_cb",
        "milgp_v_mmac_assaulter_belt_khk",
        "milgp_v_mmac_assaulter_belt_mc",
        "milgp_v_mmac_assaulter_belt_rgr",
        "milgp_v_mmac_hgunner_belt_cb",
        "milgp_v_mmac_hgunner_belt_khk",
        "milgp_v_mmac_hgunner_belt_mc",
        "milgp_v_mmac_hgunner_belt_rgr",
        "milgp_v_mmac_medic_belt_cb",
        "milgp_v_mmac_medic_belt_khk",
        "milgp_v_mmac_medic_belt_mc",
        "milgp_v_mmac_medic_belt_rgr",
        "milgp_v_mmac_teamleader_belt_cb",
        "milgp_v_mmac_teamleader_belt_khk",
        "milgp_v_mmac_teamleader_belt_mc",
        "milgp_v_mmac_teamleader_belt_rgr",
        "MineDetector",
        "murshun_cigs_cigpack",
        "murshun_cigs_lighter",
        "optic_arco_ak_blk_f",
        "optic_arco",
        "optic_hamr",
        "optic_mrco",
        "pca_backpack_invisible_large",
        "pca_backpack_invisible",
        "pca_headband_blk",
        "pca_headband_red",
        "pca_headband_tan",
        "pca_headband",
        "pca_mag_30Rnd_556x45_M855A1_PMAG_Blk",
        "pca_mag_30Rnd_556x45_M856A1_PMAG_Blk",
        "pca_mag_30Rnd_556x45_M856A1_PMAG_Blk",
        "pca_nvg_face_shield_blk",
        "pca_nvg_face_shield_cb",
        "pca_nvg_face_shield_khk",
        "pca_nvg_face_shield_rgr",
        "pca_nvg_face_shield_shemagh_blk",
        "pca_nvg_face_shield_shemagh_cb",
        "pca_nvg_face_shield_shemagh_khk",
        "pca_nvg_face_shield_shemagh_rgr",
        "pca_nvg_face_shield_shemagh_tan",
        "pca_nvg_face_shield_tan",
        "pca_nvg_shemagh_lowered_oli",
        "pca_nvg_shemagh_lowered_red",
        "pca_nvg_shemagh_lowered_tan",
        "pca_nvg_shemagh_lowered_white",
        "pca_weap_svd_wood_npz",
        "rhs_10Rnd_762x54mmR_7N14",
        "rhs_fieldcap_m88_back",
        "rhs_fieldcap_m88",
        "rhs_mag_M397_HET",
        "rhs_mag_M433_HEDP",
        "rhs_mag_M441_HE",
        "rhs_mag_m67",
        "rhs_mag_m713_Red",
        "rhs_mag_m714_White",
        "rhs_mag_m715_Green",
        "rhs_mag_m716_yellow",
        "rhs_rk_sht_30_olive",
        "rhsgref_uniform_TLA_1",
        "rhsgref_uniform_TLA_2",
        "rhssaf_kitbag_md2camo",
        "rhsusf_acc_acog",
        "rhsusf_m112_mag",
        "rhsusf_m112_mag",
        "rhsusf_m112x4_mag",
        "sfp_weap_ak5c_blk",
        "sfp_weap_ak5c_m203_blk",
        "sfp_weap_ak5c_vfg_blk",
        "SmokeShell",
        "SmokeShellBlue",
        "SmokeShellGreen",
        "SmokeShellOrange",
        "SmokeShellPurple",
        "SmokeShellRed",
        "SmokeShellYellow",
        "sps_100Rnd_762x51_M62_Tracer_Red_KAC_Box",
        "sps_100Rnd_762x51_M80A1_Mixed_KAC_Box",
        "sps_200Rnd_556x45_M855A1_Mixed_KAC_Box",
        "sps_200Rnd_556x45_M856A1_Tracer_Red_KAC_Box",
        "sps_weap_kac_amg_blk",
        "sps_weap_kac_lamg_blk",
        "sps_weap_kac_lamg_hg_blk",
        "ToolKit",
        "U_BG_Guerilla1_1",
        "U_BG_Guerilla2_1",
        "U_BG_Guerilla2_2",
        "U_BG_Guerilla2_3",
        "U_BG_Guerrilla_6_1",
        "U_BG_leader",
        "wsx_eagle_a3_khk",
        "wsx_eagle_a3_rgr",
        "wsx_tacticalpack_oli",
    }
    
    # Verify all expected items are found
    assert expected_items.issubset(found_items), \
        f"Missing items: {expected_items - found_items}"

    # Verify filtered items
    filtered_items = {
        'WhiteHead_01', 'WhiteHead_02', # Face textures should be filtered
        '$', # Macro references should be filtered
        '' # Empty strings should be filtered
    }
    
    assert not (filtered_items & found_items), \
        f"Found items that should be filtered: {filtered_items & found_items}"

    # Verify array parsing
    array_items = {
        "ACE_Clacker",
        "ACE_DefusalKit",
        "ACE_EntrenchingTool",
        "rhsusf_m112_mag",
        "MineDetector"
    }
    
    assert array_items.issubset(found_items), \
        f"Missing array items: {array_items - found_items}"

# Keep basic test for regression testing
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
    
    path.unlink()  # Cleanup

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
    
    path.unlink()  # Cleanup

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
    
    path.unlink()  # Cleanup
