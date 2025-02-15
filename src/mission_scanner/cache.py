import json
from types import MappingProxyType
from typing import Dict, Set, Optional, Mapping, FrozenSet, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

@dataclass(frozen=True)
class MissionCache:
    """Immutable cache container for mission data."""
    classes: Mapping[str, FrozenSet[str]] = field(default_factory=lambda: MappingProxyType({}))
    equipment: Mapping[str, FrozenSet[str]] = field(default_factory=lambda: MappingProxyType({}))
    last_updated: datetime = field(default_factory=datetime.now)

    @classmethod
    def create_bulk(cls, data: Dict[str, Dict[str, Set[str]]]) -> 'MissionCache':
        """Create a new cache instance with bulk data."""
        immutable_classes = MappingProxyType({
            k: frozenset(v) for k, v in data.get('classes', {}).items()
        })
        immutable_equipment = MappingProxyType({
            k: frozenset(v) for k, v in data.get('equipment', {}).items()
        })
        
        return cls(
            classes=immutable_classes,
            equipment=immutable_equipment,
            last_updated=datetime.now()
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert cache to dictionary for serialization."""
        return {
            'classes': {k: list(v) for k, v in self.classes.items()},
            'equipment': {k: list(v) for k, v in self.equipment.items()},
            'last_updated': self.last_updated.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MissionCache':
        """Create cache from dictionary."""
        return cls(
            classes=MappingProxyType({k: frozenset(v) for k, v in data['classes'].items()}),
            equipment=MappingProxyType({k: frozenset(v) for k, v in data['equipment'].items()}),
            last_updated=datetime.fromisoformat(data['last_updated'])
        )

class MissionCacheManager:
    """Manages caching of scanned mission data with thread-safe access."""
    
    def __init__(self, max_size: int = 1_000_000) -> None:
        self._cache: Optional[MissionCache] = None
        self._max_cache_age = 3600  # 1 hour in seconds
        self._max_size = max_size

    def add_mission_data(self, data: Dict[str, Dict[str, Set[str]]]) -> None:
        """Bulk add or update mission data in cache."""
        if len(data.get('classes', {})) + len(data.get('equipment', {})) > self._max_size:
            raise ValueError(f"Cache size exceeded: {len(data)} > {self._max_size}")
        self._cache = MissionCache.create_bulk(data)

    def get_class(self, name: str) -> Set[str]:
        """Get all file paths where a class is defined."""
        if not self._cache:
            return set()
        return set(self._cache.classes.get(name, set()))

    def get_equipment(self, name: str) -> Set[str]:
        """Get all file paths where equipment is defined."""
        if not self._cache:
            return set()
        return set(self._cache.equipment.get(name, set()))

    def get_all_classes(self) -> Set[str]:
        """Get all cached class names."""
        if not self._cache:
            return set()
        return set(self._cache.classes.keys())

    def get_all_equipment(self) -> Set[str]:
        """Get all cached equipment names."""
        if not self._cache:
            return set()
        return set(self._cache.equipment.keys())

    def find_classes_by_parent(self, parent: str) -> Set[str]:
        """Find all classes that inherit from the given parent class."""
        if not self._cache:
            return set()
        return {name for name in self._cache.classes.keys() if name.startswith(parent)}

    def is_cache_valid(self) -> bool:
        """Check if cache is still valid."""
        if not self._cache:
            return False
        return (datetime.now() - self._cache.last_updated).seconds < self._max_cache_age

    def save_to_disk(self, path: Path) -> None:
        """Save cache to disk."""
        if not self._cache:
            raise ValueError("No cache data to save")
            
        path.parent.mkdir(parents=True, exist_ok=True)
        cache_data = {
            'max_size': self._max_size,
            'max_cache_age': self._max_cache_age,
            'cache': self._cache.to_dict()
        }
        
        with path.open('w') as f:
            json.dump(cache_data, f, indent=2)

    def load_from_disk(self, path: Path) -> None:
        """Load cache from disk."""
        if not path.exists():
            raise FileNotFoundError(f"Cache file not found: {path}")
            
        with path.open('r') as f:
            data = json.load(f)
            
        self._max_size = data['max_size']
        self._max_cache_age = data['max_cache_age']
        self._cache = MissionCache.from_dict(data['cache'])

