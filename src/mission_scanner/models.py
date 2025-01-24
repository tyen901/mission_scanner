from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Set, List, Optional

@dataclass(frozen=True)  # Make class immutable
class Equipment:
    """Equipment found in mission files"""
    name: str
    type: Optional[str] = None
    category: Optional[str] = None  # Add category field
    class_name: Optional[str] = None
    properties: Dict[str, str] = field(default_factory=dict)
    file_path: Optional[Path] = None

    def __hash__(self):
        return hash((self.name, self.type, self.category, self.class_name, str(self.file_path)))

@dataclass(frozen=True)  # Make class immutable
class MissionClass:
    """Class definition found in mission files"""
    name: str
    parent: Optional[str] = None
    file_path: Optional[Path] = None
    properties: Dict[str, str] = field(default_factory=dict)

    def __hash__(self):
        return hash((self.name, self.parent, str(self.file_path)))

@dataclass
class ScanResult:
    """Result of a mission directory scan"""
    classes: Dict[str, MissionClass] = field(default_factory=dict)
    equipment: Dict[str, Equipment] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)

    def merge(self, other: 'ScanResult') -> None:
        """Merge another scan result into this one"""
        self.classes.update(other.classes)
        self.equipment.update(other.equipment)
        self.errors.extend(other.errors)

    @property
    def class_names(self) -> Set[str]:
        """Get set of all class names"""
        return set(self.classes.keys())

    @property
    def equipment_names(self) -> Set[str]:
        """Get set of all equipment names"""
        return set(self.equipment.keys())

    @property
    def has_errors(self) -> bool:
        """Check if scan had any errors"""
        return len(self.errors) > 0
