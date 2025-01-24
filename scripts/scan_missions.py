import os
import sys
import json
from pathlib import Path
import tempfile
from datetime import datetime
import logging
from tqdm import tqdm

# Add the src directory to Python path
src_path = str(Path(__file__).parent.parent / 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from mission_scanner import MissionScannerAPI

PROJECT_ROOT = Path(__file__).parent.parent
SAMPLE_DATA = PROJECT_ROOT / 'sample_data'

def generate_report(api: MissionScannerAPI, output_path: Path) -> None:
    """Generate a detailed report of mission classes and equipment"""
    stats = api.get_stats()
    
    report = {
        "scan_time": datetime.now().isoformat(),
        "summary": {
            "total_scans": stats['total_scans'],
            "failed_scans": stats['failed_scans'],
            "total_classes": stats['total_classes'],
            "total_equipment": stats['total_equipment']
        },
        "classes": {},
        "equipment": {}
    }

    # Get result from last scan
    result = api.scan_directory(SAMPLE_DATA)
    
    # Add classes and equipment to report
    for name, cls in result.classes.items():
        report["classes"][name] = {
            "parent": cls.parent,
            "properties": dict(cls.properties),
            "defined_in": [str(cls.file_path)]
        }
        
    for name, equip in result.equipment.items():
        report["equipment"][name] = {
            "type": equip.type,
            "properties": dict(equip.properties),
            "defined_in": [str(equip.file_path)]
        }

    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, sort_keys=True)

def _build_class_hierarchy(classes):
    """Build class hierarchy dictionary"""
    # Initialize hierarchy
    hierarchy = {}
    root_classes = []
    
    # Group classes by their parent
    for cls in classes:
        if not cls.parent:
            root_classes.append(cls)
        else:
            if cls.parent not in hierarchy:
                hierarchy[cls.parent] = []
            hierarchy[cls.parent].append(cls)
    
    return root_classes, hierarchy

def _write_class_tree(f, cls, hierarchy, level=0):
    """Write class tree recursively with proper indentation"""
    indent = "  " * level
    extension_info = f" (extends {cls.parent})" if cls.parent else ""
    f.write(f"{indent}- {cls.name}{extension_info}\n")
    
    # Process children
    if cls.name in hierarchy:
        for child in sorted(hierarchy[cls.name], key=lambda x: x.name):
            _write_class_tree(f, child, hierarchy, level + 1)

def generate_text_report(api: MissionScannerAPI, output_path: Path) -> None:
    """Generate a human-readable text report of mission classes and equipment"""
    stats = api.get_stats()
    result = api.scan_directory(SAMPLE_DATA)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Write header
        f.write("Mission Scanner Report\n")
        f.write("=" * 50 + "\n\n")
        
        # Write summary
        f.write("Summary\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total scans: {stats['total_scans']}\n")
        f.write(f"Failed scans: {stats['failed_scans']}\n")
        f.write(f"Total classes: {stats['total_classes']}\n")
        f.write(f"Total equipment: {stats['total_equipment']}\n\n")
        
        # Group items by file
        items_by_file = {}
        for cls in result.classes.values():
            file_path = str(cls.file_path)
            if file_path not in items_by_file:
                items_by_file[file_path] = {'classes': [], 'equipment': []}
            # Store full class information
            items_by_file[file_path]['classes'].append(cls)
            
        for eq in result.equipment.values():
            file_path = str(eq.file_path)
            if file_path not in items_by_file:
                items_by_file[file_path] = {'classes': [], 'equipment': []}
            items_by_file[file_path]['equipment'].append(eq)
        
        # Write items grouped by file
        f.write("Found Items By File\n")
        f.write("=" * 50 + "\n\n")
        
        for file_path, items in sorted(items_by_file.items()):
            f.write(f"\nFile: {file_path}\n")
            f.write("-" * len(f"File: {file_path}") + "\n")
            
            if items['classes']:
                f.write("\nClasses:\n")
                # Build class hierarchy
                root_classes, hierarchy = _build_class_hierarchy(items['classes'])
                # Write class tree starting from root classes
                for cls in sorted(root_classes, key=lambda x: x.name):
                    _write_class_tree(f, cls, hierarchy)
            
            if items['equipment']:
                f.write("\nEquipment:\n")
                for eq in sorted(items['equipment'], key=lambda x: x.name):
                    f.write(f"  - {eq.name}")
                    if eq.type:
                        f.write(f" (type: {eq.type})")
                    f.write("\n")
            f.write("\n")

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(PROJECT_ROOT / 'scan_missions.log')
        ]
    )
    logger = logging.getLogger()

    try:
        # Initialize API with cache in temp directory
        temp_dir = PROJECT_ROOT / 'temp'
        temp_dir.mkdir(exist_ok=True)
        api = MissionScannerAPI(temp_dir / 'cache')

        # Set up progress tracking
        pbar = tqdm(desc="Scanning", unit=" files")
        def progress_callback(path: str):
            pbar.update(1)
            pbar.set_description(f"Scanning: {Path(path).name[:30]}")
        api._scanner.progress_callback = progress_callback

        if not SAMPLE_DATA.exists():
            logger.error(f"Sample data directory not found: {SAMPLE_DATA}")
            sys.exit(1)
            
        # Scan sample data directory
        logger.info(f"Scanning missions in: {SAMPLE_DATA}")
        result = api.scan_directory(SAMPLE_DATA)
        
        # Generate text report instead of JSON
        output_file = temp_dir / f"mission_scan_{datetime.now():%Y%m%d_%H%M%S}.txt"
        generate_text_report(api, output_file)
        logger.info(f"Report written to: {output_file}")
        
        # Print summary
        print("\nScan Summary:")
        stats = api.get_stats()
        print(f"Total scans: {stats['total_scans']}")
        print(f"Total classes found: {stats['total_classes']}")
        print(f"Total equipment found: {stats['total_equipment']}")
        
    except Exception as e:
        logger.exception(f"\nError during scan: {e}")
        sys.exit(1)
    finally:
        if 'api' in locals():
            api.cleanup()
        if 'pbar' in locals():
            pbar.close()

if __name__ == "__main__":
    main()
