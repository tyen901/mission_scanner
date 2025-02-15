import pytest
from mission_scanner.cache import MissionCache, MissionCacheManager
from dataclasses import FrozenInstanceError

@pytest.fixture
def sample_data():
    return {
        'classes': {
            'baseMan': {'/path/to/file1.hpp', '/path/to/file2.hpp'},
            'rifleman': {'/path/to/file1.hpp'}
        },
        'equipment': {
            'rifle_m4': {'/path/to/file1.hpp'},
            'pistol_glock': {'/path/to/file2.hpp'}
        }
    }

@pytest.fixture
def cache_manager():
    return MissionCacheManager(max_size=1000)

def test_mission_cache_creation(sample_data):
    """Test MissionCache creation and immutability"""
    cache = MissionCache.create_bulk(sample_data)
    
    # Test immutability by attempting to modify the frozen dataclass
    with pytest.raises(FrozenInstanceError):
        cache.classes = {'new_class': frozenset()} # type: ignore
    
    # Test immutability of the internal mappings
    with pytest.raises(TypeError):
        cache.classes['new_equipment'] = frozenset()  # type: ignore
    
    # Test immutability of the sets within mappings
    some_class = next(iter(cache.classes))
    files = cache.classes[some_class]
    # Verify we can't modify the frozen set
    with pytest.raises(AttributeError):
        files.add('/new/path') # type: ignore

def test_cache_manager_add_data(cache_manager, sample_data):
    """Test adding data to cache manager"""
    cache_manager.add_mission_data(sample_data)
    
    assert 'baseMan' in cache_manager.get_all_classes()
    assert 'rifle_m4' in cache_manager.get_all_equipment()

def test_cache_manager_get_class(cache_manager, sample_data):
    """Test retrieving class information"""
    cache_manager.add_mission_data(sample_data)
    
    base_man_files = cache_manager.get_class('baseMan')
    assert len(base_man_files) == 2
    assert '/path/to/file1.hpp' in base_man_files
    assert '/path/to/file2.hpp' in base_man_files

def test_cache_manager_get_equipment(cache_manager, sample_data):
    """Test retrieving equipment information"""
    cache_manager.add_mission_data(sample_data)
    
    rifle_files = cache_manager.get_equipment('rifle_m4')
    assert len(rifle_files) == 1
    assert '/path/to/file1.hpp' in rifle_files

def test_cache_manager_max_size(cache_manager):
    """Test cache size limits"""
    large_data = {
        'classes': {f'class_{i}': {f'/path/{i}'} for i in range(2000)}
    }
    
    with pytest.raises(ValueError, match="Cache size exceeded"):
        cache_manager.add_mission_data(large_data)

def test_cache_manager_empty_cache(cache_manager):
    """Test behavior with empty cache"""
    assert cache_manager.get_class('nonexistent') == set()
    assert cache_manager.get_equipment('nonexistent') == set()
    assert cache_manager.get_all_classes() == set()
    assert cache_manager.get_all_equipment() == set()

def test_cache_validity(cache_manager, sample_data):
    """Test cache validity checking"""
    cache_manager.add_mission_data(sample_data)
    assert cache_manager.is_cache_valid()

def test_find_classes_by_parent(cache_manager):
    """Test finding classes by parent prefix"""
    data = {
        'classes': {
            'base_soldier': {'file1'},
            'base_soldier_rifleman': {'file1'},
            'base_soldier_medic': {'file1'},
            'vehicle_tank': {'file2'}
        }
    }
    
    cache_manager.add_mission_data(data)
    soldier_classes = cache_manager.find_classes_by_parent('base_soldier')
    
    assert len(soldier_classes) == 3
    assert 'base_soldier' in soldier_classes
    assert 'base_soldier_rifleman' in soldier_classes
    assert 'base_soldier_medic' in soldier_classes
    assert 'vehicle_tank' not in soldier_classes

def test_cache_manager_multiple_updates(cache_manager):
    """Test multiple cache updates"""
    initial_data = {
        'classes': {'class1': {'file1'}},
        'equipment': {'eq1': {'file1'}}
    }
    
    updated_data = {
        'classes': {'class2': {'file2'}},
        'equipment': {'eq2': {'file2'}}
    }
    
    cache_manager.add_mission_data(initial_data)
    first_classes = cache_manager.get_all_classes()
    
    cache_manager.add_mission_data(updated_data)
    second_classes = cache_manager.get_all_classes()
    
    assert 'class1' in first_classes
    assert 'class2' in second_classes
    assert 'class1' not in second_classes

def test_cache_save_load(tmp_path, cache_manager, sample_data):
    """Test saving and loading cache to/from disk"""
    cache_manager.add_mission_data(sample_data)
    cache_file = tmp_path / "cache.json"
    
    # Test saving
    cache_manager.save_to_disk(cache_file)
    assert cache_file.exists()
    
    # Create new cache manager and load saved data
    new_manager = MissionCacheManager()
    new_manager.load_from_disk(cache_file)
    
    # Verify loaded data matches original
    assert new_manager.get_all_classes() == cache_manager.get_all_classes()
    assert new_manager.get_all_equipment() == cache_manager.get_all_equipment()
    assert new_manager._max_size == cache_manager._max_size
    assert new_manager._max_cache_age == cache_manager._max_cache_age

def test_save_empty_cache(cache_manager, tmp_path):
    """Test attempting to save empty cache"""
    cache_file = tmp_path / "empty_cache.json"
    with pytest.raises(ValueError, match="No cache data to save"):
        cache_manager.save_to_disk(cache_file)

def test_load_nonexistent_cache(cache_manager, tmp_path):
    """Test loading from nonexistent cache file"""
    cache_file = tmp_path / "nonexistent.json"
    with pytest.raises(FileNotFoundError):
        cache_manager.load_from_disk(cache_file)

def test_cache_serialization_round_trip(sample_data):
    """Test cache serialization/deserialization"""
    # Create cache with sample data
    cache = MissionCache.create_bulk(sample_data)
    
    # Convert to dict and back
    cache_dict = cache.to_dict()
    restored_cache = MissionCache.from_dict(cache_dict)
    
    # Compare original and restored cache
    assert restored_cache.classes == cache.classes
    assert restored_cache.equipment == cache.equipment
    assert restored_cache.last_updated == cache.last_updated
