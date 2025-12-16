"""
Utility script to export Python-based adventures to JSON format
"""
from sample_adventure import create_sample_adventure, create_simple_adventure
from adventure_loader import AdventureExporter
import os


def export_all_adventures():
    """Export all built-in adventures to JSON files"""
    
    # Create adventures directory if it doesn't exist
    os.makedirs('adventures', exist_ok=True)
    
    print("Exporting adventures to JSON format...\n")
    
    # Export Dark Tower
    print("1. Exporting 'The Dark Tower'...")
    dark_tower = create_sample_adventure()
    AdventureExporter.export_to_file(dark_tower, 'adventures/dark_tower.json')
    print(f"   ✓ Saved to adventures/dark_tower.json")
    print(f"   {len(dark_tower.nodes)} nodes exported\n")
    
    # Export Goblin Cave
    print("2. Exporting 'The Goblin Cave'...")
    goblin_cave = create_simple_adventure()
    AdventureExporter.export_to_file(goblin_cave, 'adventures/goblin_cave.json')
    print(f"   ✓ Saved to adventures/goblin_cave.json")
    print(f"   {len(goblin_cave.nodes)} nodes exported\n")
    
    print("="*60)
    print("Export complete!")
    print("="*60)
    print("\nJSON files are ready to use and can be edited in any text editor.")
    print("See ADVENTURE_JSON_FORMAT.md for documentation on the format.")


if __name__ == "__main__":
    export_all_adventures()
