import logging
import re
from pathlib import Path
from typing import Set, Dict, Any, List, Optional, cast

from mission_scanner.parser import BaseParser, ParseResult
from mission_scanner.models import Equipment, MissionClass
from mission_scanner.parser import read_file_content
from class_scanner import ClassParser, PropertyValue, ClassObject

logger = logging.getLogger(__name__)

class SqmParser(BaseParser):
    """Parser for SQM mission files"""
    
    def __init__(self):
        self.class_parser = ClassParser()  # Use single ClassParser

    def parse(self, file_path: Path) -> ParseResult:
        """Parse SQM file and return classes and equipment"""
        classes: Dict[str, MissionClass] = {}
        equipment: Set[Equipment] = set()
        
        try:
            content, _ = read_file_content(file_path)
            if content is None:
                return ParseResult(classes, equipment)

            # Parse entire class hierarchy
            class_objects = self.class_parser.parse_hierarchical(content)
            logger.debug(f"Parsed {len(class_objects)} top level objects")

            # Find mission class
            for mission_class in class_objects:
                if mission_class.name == "Mission":
                    # Process mission structure
                    self._process_mission_class(mission_class, equipment, file_path)
                    break

        except Exception as e:
            logger.error(f"Error parsing SQM file {file_path}: {e}", exc_info=True)
            
        return ParseResult(classes, equipment)

    def _process_mission_class(self, mission: ClassObject, equipment: Set[Equipment], file_path: Path) -> None:
        """Process Mission class and all its nested entities"""
        # Find Entities class
        entities_class = mission.find_nested_class("Entities")
        if not entities_class:
            return

        # Process all Item classes recursively
        self._process_entities(entities_class, equipment, file_path)

    def _process_entities(self, entities: ClassObject, equipment: Set[Equipment], file_path: Path) -> None:
        """Recursively process all entities looking for inventory"""
        for cls in entities.nested_classes:
            # Process current class if it's an Item with Object dataType
            if (cls.name.startswith("Item") and 
                "dataType" in cls.properties and
                cls.properties["dataType"] == "Object"):
                
                # Look for nested Attributes class
                if attributes := cls.find_nested_class("Attributes"):
                    # Look for Inventory in Attributes
                    if inventory := attributes.find_nested_class("Inventory"):
                        self._process_inventory_object(inventory, equipment, file_path)

            # Recursively process any nested Entities
            if nested_entities := cls.find_nested_class("Entities"):
                self._process_entities(nested_entities, equipment, file_path)

    def _find_entities_with_inventory(self, classes: List[ClassObject]) -> List[ClassObject]:
        """Find all entity objects that have inventory"""
        entities = []
        
        for cls in classes:
            # Check if this is an entity with inventory using ClassObject methods
            if (cls.name.startswith("Item") and 
                "dataType" in cls.properties and
                cls.properties["dataType"] == "Object" and
                cls.find_nested_class("Inventory")):
                entities.append(cls)
                
            # Recursively check nested classes
            entities.extend(self._find_entities_with_inventory(cls.nested_classes))
                
        return entities

    def _process_inventory_object(self, inventory: ClassObject, equipment: Set[Equipment], file_path: Path) -> None:
        """Process an inventory class object and its contents"""
        # First process direct equipment properties - use exact case as in SQM
        equipment_types = {
            'map': 'ItemMap',
            'compass': 'ItemCompass', 
            'watch': 'ItemWatch',
            'headgear': 'headgear',
            'binocular': 'binocular'
        }

        for prop_name, item_name in equipment_types.items():
            if prop_name in inventory.properties:
                equipment.add(Equipment(
                    name=item_name,  # Use standard item name
                    type='item',
                    category=prop_name,
                    file_path=file_path
                ))
                logger.debug(f"Added {prop_name}: {item_name}")

        # Process weapon classes
        for weapon_type in ['primaryWeapon', 'handgun', 'secondaryWeapon']:
            if weapon := inventory.find_nested_class(weapon_type):
                self._process_weapon(weapon, equipment, file_path)

        # Process container classes
        for container in ['uniform', 'vest', 'backpack']:
            if container_obj := inventory.find_nested_class(container):
                self._process_container(container_obj, equipment, file_path)

    def _process_weapon(self, weapon: ClassObject, equipment: Set[Equipment], file_path: Path) -> None:
        """Process a weapon class and its attachments"""
        if 'name' not in weapon.properties:
            return

        name = cast(PropertyValue, weapon.properties['name']).raw_value
        equipment.add(Equipment(
            name=name,
            type='weapon',
            category=weapon.name,  # primaryWeapon, handgun, or secondaryWeapon
            file_path=file_path
        ))
        logger.debug(f"Added weapon: {name}")

        # Process weapon attachments if present
        for attachment_type in ['optics', 'muzzle', 'pointer']:
            if value := weapon.properties.get(attachment_type):
                if isinstance(value, PropertyValue):
                    equipment.add(Equipment(
                        name=value.raw_value,
                        type='attachment',
                        category=attachment_type,
                        file_path=file_path
                    ))
                    logger.debug(f"Added {attachment_type}: {value.raw_value}")

        # Process weapon magazines
        if mag_class := weapon.find_nested_class('primaryMuzzleMag'):
            if 'name' in mag_class.properties:
                mag_name = cast(PropertyValue, mag_class.properties['name']).raw_value
                equipment.add(Equipment(
                    name=mag_name,
                    type='magazine',
                    category=weapon.name,
                    file_path=file_path
                ))
                logger.debug(f"Added magazine: {mag_name}")

    def _process_container(self, container: ClassObject, equipment: Set[Equipment], file_path: Path) -> None:
        """Process a container (uniform/vest/backpack) and its cargo"""
        # Add the container itself
        if typename := container.properties.get('typeName'):
            if isinstance(typename, PropertyValue):
                equipment.add(Equipment(
                    name=typename.raw_value,
                    type='container',
                    category=container.name,
                    file_path=file_path
                ))
                logger.debug(f"Added container: {typename.raw_value}")

        # Process ItemCargo
        if item_cargo := container.find_nested_class('ItemCargo'):
            self._process_cargo_items(item_cargo, 'item', equipment, file_path)

        # Process MagazineCargo
        if mag_cargo := container.find_nested_class('MagazineCargo'):
            self._process_cargo_items(mag_cargo, 'magazine', equipment, file_path)

    def _process_cargo_items(self, cargo: ClassObject, cargo_type: str, equipment: Set[Equipment], file_path: Path) -> None:
        """Process cargo items from a container"""
        if 'items' not in cargo.properties:
            return

        items_count = int(cast(PropertyValue, cargo.properties['items']).raw_value)
        
        for i in range(items_count):
            item_key = f'Item{i}'
            if item := cargo.find_nested_class(item_key):
                if 'name' in item.properties:
                    name = cast(PropertyValue, item.properties['name']).raw_value
                    count = 1
                    if 'count' in item.properties:
                        count = int(cast(PropertyValue, item.properties['count']).raw_value)
                    
                    # Add each item
                    equipment.add(Equipment(
                        name=name,
                        type=cargo_type,
                        category=cargo.name.lower().replace('cargo', ''),
                        file_path=file_path,
                        count=count
                    ))
                    logger.debug(f"Added cargo {cargo_type}: {name} x{count}")
