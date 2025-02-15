from pathlib import Path

SAMPLE_MISSIONS_FOLDERS = [
    'co32_Seaside_Sweep_2.Altis',
    'co33_cybertruck_at_home_v2.tem_anizay',
    'co33_elephant_of_surprise.tem_kujari',
    'co34_lets_ride_the_mechanism_v2.tem_suursaariv',
    'pre_session.sara'
]

# Base path for sample data
SAMPLE_DATA = Path(__file__).parent / "sample_data"

EXAMPLE_CURATED_ARSENAL = SAMPLE_DATA / "example_curated_arsenal.hpp"
EXAMPLE_CURATED_GEAR = SAMPLE_DATA / "example_curated_gear.hpp"
EXAMPLE_LOADOUT = SAMPLE_DATA / "example_loadout.hpp"
EXAMPLE_MISSION = SAMPLE_DATA / "example_mission.sqm"

SAMPLE_MISSIONS = [
    SAMPLE_DATA / mission for mission in SAMPLE_MISSIONS_FOLDERS
]

