# JSON Adventure System - Summary

## What Was Implemented

The project now supports **storing adventures in JSON files** that can be loaded at runtime. This provides a data-driven approach to creating adventures without modifying Python code.

## New Files Created

1. **adventure_loader.py** - Core loader and exporter classes
   - `AdventureLoader`: Loads adventures from JSON files
   - `AdventureExporter`: Exports Python adventures to JSON format

2. **adventures/** - Directory containing adventure JSON files
   - `goblin_cave.json` - The Goblin Cave adventure
   - `dark_tower.json` - The Dark Tower adventure  
   - `template.json` - Template for creating new adventures

3. **ADVENTURE_JSON_FORMAT.md** - Complete documentation of the JSON format

4. **export_adventures.py** - Utility script to export Python adventures to JSON

## How It Works

### Loading Adventures from JSON

The system can load adventures in three ways:

1. **Automatic loading** (options 1 & 2 in main menu)
   - Tries to load from JSON first
   - Falls back to Python code if JSON not found

2. **Custom JSON loading** (option 3 in main menu)
   - Lists all JSON files in `adventures/` directory
   - Allows selection or direct path input

3. **Programmatic loading**:
   ```python
   from adventure_loader import AdventureLoader
   adventure = AdventureLoader.load_from_file('path/to/adventure.json')
   ```

### JSON Structure

The JSON format supports all key features:

```json
{
  "title": "Adventure Name",
  "description": "Adventure intro",
  "starting_node_id": "start",
  "nodes": [
    {
      "node_id": "start",
      "title": "Node Title",
      "description": "Full description...",
      "monsters": ["goblin", "orc"],
      "treasure": ["50 gold pieces", "Potion of Healing"],
      "traps": [{
        "type": "spike trap",
        "dc": 15,
        "damage": "2d6",
        "save_type": "reflex"
      }],
      "choices": [{
        "text": "Choice text",
        "target": "target_node_id",
        "requirements": {
          "dexterity": 14,
          "item": "key",
          "level": 3
        }
      }],
      "is_victory": false,
      "is_defeat": false
    }
  ]
}
```

## Features Supported

### ✅ Fully Supported in JSON
- Node structure (id, title, description)
- Monster encounters (list of monster types)
- Treasure (items and gold)
- Traps (type, DC, damage, save type)
- Choices with targets
- Requirements (ability scores, items, level)
- Victory/defeat nodes

### ⚠️ Limitations
- **Custom events**: Python functions can't be stored in JSON
  - Solution: Add programmatically after loading if needed
- **Complex logic**: Advanced branching requires Python code
- **Monster types**: Limited to predefined types in monster.py

## Benefits

### For Game Designers
- Create adventures without coding
- Edit in any text editor
- Quick iteration and testing
- Share adventures easily

### For Developers  
- Separate data from code
- Version control friendly
- Easy to extend with custom loaders
- Potential for visual editors

### For Players
- Community-created content
- Easy to download and try new adventures
- Mod-friendly

## Usage Examples

### Creating a New Adventure

1. Copy template:
   ```bash
   cp adventures/template.json adventures/my_quest.json
   ```

2. Edit JSON file with your content

3. Run game and select option 3 to load it

### Converting Python to JSON

```bash
python export_adventures.py
```

This exports all Python adventures to JSON format.

### Loading in Code

```python
from adventure_loader import AdventureLoader
from character import Character
from game import GameEngine

# Load adventure
adventure = AdventureLoader.load_from_file('adventures/my_quest.json')

# Create character and play
character = Character("Hero", "Fighter", level=1)
character.roll_abilities()

game = GameEngine(adventure, character)
game.start_game()
```

## Testing

Both adventures have been tested and confirmed working:
- ✓ The Goblin Cave: 5 nodes loaded successfully
- ✓ The Dark Tower: 14 nodes loaded successfully
- ✓ All node properties (monsters, treasure, traps, choices) preserved
- ✓ Requirements system functional
- ✓ Victory/defeat flags working

## Next Steps (Optional Enhancements)

1. **Visual Adventure Editor** - GUI for creating adventures
2. **YAML Support** - Alternative format (more human-readable)
3. **Adventure Validation** - Check for broken links, missing nodes
4. **Dynamic Monster Creation** - Define monsters in JSON
5. **Conditional Events** - Simple event system in JSON
6. **Variable System** - Track game state beyond character
7. **Import/Export Save Games** - Include adventure reference

## Documentation

- **ADVENTURE_JSON_FORMAT.md** - Complete JSON format reference
- **README.md** - Updated with JSON instructions
- **template.json** - Starting point for new adventures

## Backward Compatibility

The system maintains full backward compatibility:
- Python-based adventures still work
- sample_adventure.py functions unchanged
- Can mix JSON and Python approaches
- Existing saves should work (node IDs preserved)

---

**Ready to use!** You can now create adventures by simply editing JSON files.
