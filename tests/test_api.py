import pytest
from pathlib import Path
import re
from mission_scanner.api import MissionScannerAPI, MissionScannerAPIConfig
from mission_scanner.models import ScanResult

from tests.conftest import SAMPLE_DATA_FOLDER

@pytest.fixture
def temp_cache_dir(tmp_path):
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    return cache_dir

@pytest.fixture
def api(temp_cache_dir):
    config = MissionScannerAPIConfig(
        cache_max_age=3600,
        cache_max_size=1000000,
        max_workers=2
    )
    api = MissionScannerAPI(temp_cache_dir, config)
    yield api
    api.cleanup()

def test_api_initialization(temp_cache_dir):
    """Test API initialization with config"""
    def error_handler(e):
        return None
    def progress_callback(msg, progress):
        return None
    
    config = MissionScannerAPIConfig(
        cache_max_age=1800,
        cache_max_size=500000,
        max_workers=4,
        error_handler=error_handler,
        progress_callback=progress_callback
    )
    
    api = MissionScannerAPI(temp_cache_dir, config)
    assert api.config.cache_max_age == 1800
    assert api.config.cache_max_size == 500000
    assert api.config.max_workers == 4
    assert api.config.error_handler == error_handler
    assert api.config.progress_callback == progress_callback

def test_scan_directory(api):  # Removed sample_loadout parameter
    """Test scanning a directory"""
    result = api.scan_directory(
        SAMPLE_DATA_FOLDER,
        patterns=[re.compile(r'.*\.hpp$')]
    )
    
    assert isinstance(result, ScanResult)
    assert len(result.classes) > 0
    assert len(result.equipment) > 0
    assert not result.errors

def test_scan_nonexistent_directory(api):
    """Test scanning a non-existent directory"""
    with pytest.raises(FileNotFoundError):
        api.scan_directory(Path('nonexistent'))

def test_scan_with_patterns(api):
    """Test scanning with file patterns"""
    # Only scan .hpp files
    hpp_pattern = [re.compile(r'.*\.hpp$')]
    result = api.scan_directory(SAMPLE_DATA_FOLDER, patterns=hpp_pattern)
    
    # Verify only .hpp files were processed
    for class_def in result.classes.values():
        assert str(class_def.file_path).endswith('.hpp')

def test_api_stats(api):
    """Test API statistics tracking"""
    # Initial stats
    stats = api.get_stats()
    assert stats['total_scans'] == 0
    assert stats['failed_scans'] == 0
    
    # After successful scan
    api.scan_directory(SAMPLE_DATA_FOLDER)
    stats = api.get_stats()
    assert stats['total_scans'] == 1
    assert stats['failed_scans'] == 0
    assert stats['total_classes'] > 0
    assert stats['total_equipment'] > 0

def test_error_handling(temp_cache_dir):
    """Test error handling with custom handler"""
    error_caught = []
    
    def error_handler(e):
        error_caught.append(e)
    
    config = MissionScannerAPIConfig(error_handler=error_handler)
    api = MissionScannerAPI(temp_cache_dir, config)
    
    # Trigger an error
    with pytest.raises(FileNotFoundError):
        api.scan_directory(Path('nonexistent'))
    
    assert len(error_caught) == 1
    assert isinstance(error_caught[0], FileNotFoundError)

def test_api_cleanup(api):
    """Test API cleanup"""
    # Perform some operations
    api.scan_directory(SAMPLE_DATA_FOLDER)
    
    # Cleanup
    api.cleanup()
    
    # Verify executor is shut down
    assert api._executor._shutdown
