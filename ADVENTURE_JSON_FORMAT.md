# Adventure JSON Format Documentation

## Overview

Adventures can now be stored in JSON files and loaded dynamically. This makes it easy to create, edit, and share adventures without modifying Python code.

## JSON Structure

```json
{
  "title": "Adventure Title",
  "description": "Brief description of the adventure",
  "starting_node_id": "node_id_where_adventure_begins",
  "nodes": [
    // Array of node objects
  ]
}
```

## Node Structure

Each node in the `nodes` array has the following structure:

```json
{
  "node_id": "unique_identifier",
  "title": "Node Title",
  "description": "Full description of the location/scene",
  "monsters": ["monster_type1", "monster_type2"],  // Optional
  "treasure": ["item1", "item2", "X gold pieces"],  // Optional
  "traps": [  // Optional
    {
      "type": "trap_name",
      "dc": 15,
      "damage": "2d6",
      "save_type": "reflex"
    }
  ],
  "choices": [  // Optional (required unless it's an ending)
    {
      "text": "Choice text shown to player",
      "target": "target_node_id",
      "requirements": {  // Optional
        "dexterity": 14,
        "item": "key",
        "level": 3
      }
    }
  ],
  "is_victory": true,  // Optional, marks victory ending
  "is_defeat": true    // Optional, marks defeat ending
}
```

## Field Descriptions

### Adventure Level
- **title**: Name of the adventure
- **description**: Introduction/background story
- **starting_node_id**: ID of the first node players will see

### Node Level
- **node_id**: Unique string identifier (use underscores, e.g., "goblin_cave")
- **title**: Short title displayed to the player
- **description**: Full narrative text describing the scene

### Optional Node Fields

#### Monsters
Array of monster type strings. Available types:
- `"goblin"`
- `"orc"`
- `"ogre"`
- `"giant_spider"`

Example:
```json
"monsters": ["goblin", "goblin", "orc"]
```

#### Treasure
Array of item names/descriptions. Special handling for:
- Gold: Include "gold" in string with amount (e.g., "50 gold pieces")
- Potions: Include "potion" in string (e.g., "Potion of Healing")
- Other items: Descriptive strings

Example:
```json
"treasure": ["100 gold pieces", "Potion of Healing", "Magic sword +1"]
```

#### Traps
Array of trap objects:
- **type**: Description of the trap
- **dc**: Difficulty Class (target number to beat)
- **damage**: Dice notation (e.g., "2d6", "1d8+2")
- **save_type**: "reflex", "fortitude", or "will"

Example:
```json
"traps": [
  {
    "type": "poison dart trap",
    "dc": 15,
    "damage": "2d4",
    "save_type": "reflex"
  }
]
```

#### Choices
Array of choice objects that define player options:
- **text**: What the player sees
- **target**: node_id to navigate to
- **requirements**: (Optional) Dictionary of requirements

Requirements can include:
- Ability scores: `"strength": 15`, `"dexterity": 14`, etc.
- Items: `"item": "key"`
- Level: `"level": 3`

Example:
```json
"choices": [
  {
    "text": "Enter through the door",
    "target": "hallway"
  },
  {
    "text": "Pick the lock",
    "target": "hallway",
    "requirements": {
      "dexterity": 14
    }
  }
]
```

#### Ending Flags
- **is_victory**: Set to `true` for winning endings
- **is_defeat**: Set to `true` for losing endings

Ending nodes typically have no choices.

## Loading Adventures

### From Main Menu
Run the game and select option 3 to load a custom JSON adventure.

### Programmatically
```python
from adventure_loader import AdventureLoader

# Load from file
adventure = AdventureLoader.load_from_file('adventures/my_adventure.json')

# Load from dictionary
data = {...}  # JSON data as dict
adventure = AdventureLoader.load_from_dict(data)
```

## Creating New Adventures

1. Create a new `.json` file in the `adventures/` directory
2. Follow the JSON structure above
3. Ensure all `target` node_ids reference valid nodes
4. Test by running the game and selecting option 3

## Example: Simple Adventure

```json
{
  "title": "The Lost Ring",
  "description": "Find the magical ring hidden in the forest.",
  "starting_node_id": "forest_entrance",
  "nodes": [
    {
      "node_id": "forest_entrance",
      "title": "Forest Entrance",
      "description": "You stand at the edge of a dark forest.",
      "choices": [
        {
          "text": "Enter the forest",
          "target": "deep_forest"
        },
        {
          "text": "Turn back",
          "target": "defeat"
        }
      ]
    },
    {
      "node_id": "deep_forest",
      "title": "Deep Forest",
      "description": "You find a chest under an old tree!",
      "treasure": ["Magic Ring", "50 gold pieces"],
      "choices": [
        {
          "text": "Take the treasure and leave",
          "target": "victory"
        }
      ]
    },
    {
      "node_id": "victory",
      "title": "Success!",
      "description": "You found the magic ring!",
      "is_victory": true
    },
    {
      "node_id": "defeat",
      "title": "Gave Up",
      "description": "You turned back without finding the ring.",
      "is_defeat": true
    }
  ]
}
```

## Limitations

- **Custom Events**: On-enter events (Python functions) cannot be stored in JSON. These must be added programmatically if needed.
- **Monster Types**: Only predefined monster types can be used. New monsters must be added to `monster.py`.
- **Complex Logic**: Advanced branching logic requires Python code.

## Tips

- Use descriptive node_ids (e.g., "goblin_cave" not "node1")
- Test all choice paths to ensure no broken links
- Keep descriptions engaging but concise
- Balance combat, exploration, and story
- Provide multiple paths when possible for replayability
- Use requirements sparingly to avoid blocking players
- Include at least one victory and one defeat node

## Exporting Existing Adventures

To convert Python-based adventures to JSON:

```python
from sample_adventure import create_sample_adventure
from adventure_loader import AdventureExporter

adventure = create_sample_adventure()
AdventureExporter.export_to_file(adventure, 'my_adventure.json')
```

Or use the provided utility script:
```bash
python export_adventures.py
```
