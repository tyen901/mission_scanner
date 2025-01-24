from pathlib import Path
from typing import Dict, Set, Optional, Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from datetime import datetime
from .models import MissionClass, Equipment

@dataclass(frozen=True)
class MissionCache:
    """Immutable cache container for mission data."""
    classes: Mapping[str, Set[str]] = field(default_factory=dict)
    equipment: Mapping[str, Set[str]] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Convert mutable collections to immutable ones after initialization."""
        object.__setattr__(self, 'classes', MappingProxyType(dict(self.classes)))
        object.__setattr__(self, 'equipment', MappingProxyType(dict(self.equipment)))

    @classmethod
    def create_bulk(cls, data: Dict[str, Dict[str, Set[str]]]) -> 'MissionCache':
        """Create a new cache instance with bulk data."""
        classes = data.get('classes', {})
        equipment = data.get('equipment', {})

        return cls(
            classes={k: frozenset(v) for k, v in classes.items()},
            equipment={k: frozenset(v) for k, v in equipment.items()},
            last_updated=datetime.now()
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

