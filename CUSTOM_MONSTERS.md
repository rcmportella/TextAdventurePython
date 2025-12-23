# Custom Monster Support - Implementation Guide

## Overview
The adventure system now supports creating custom monsters with full stats, both through the adventure builder interface and in JSON files.

## What Was Changed

### 1. **Adventure Class** ([node.py](node.py#L282-L301))
- Added `custom_monsters` dictionary to store custom monster definitions
- Added `add_custom_monster()` method to register custom monsters
- Added `get_custom_monster()` method to retrieve custom monster stats

### 2. **Adventure Builder** ([adventure_builder.py](adventure_builder.py#L255-L330))
- Updated `add_monsters_to_node()` to include option 9 for custom monsters
- Added new `create_custom_monster()` method that collects:
  - Monster name
  - Hit dice (e.g., "2d8")
  - Armor Class (e.g., 12)
  - Attack bonus (e.g., +2)
  - Damage dice (e.g., "1d6")
  - Special abilities (list)
  - Treasure carried (list)

### 3. **Adventure Loader/Exporter** ([adventure_loader.py](adventure_loader.py#L28-L45, L127-L149))
- Updated to load `custom_monsters` from JSON
- Updated to export `custom_monsters` to JSON

### 4. **Game Engine** ([game.py](game.py#L147-L154), [node.py](node.py#L209-L240))
- Updated `create_combat()` to use custom monster stats when available
- Falls back to predefined monsters for standard types

### 5. **Validation** ([validate_adventure.py](validate_adventure.py#L109-L119))
- Updated to recognize custom monsters in validation

## JSON Format for Custom Monsters

Add a `custom_monsters` section at the adventure level:

```json
{
  "title": "Adventure Title",
  "description": "Adventure description",
  "starting_node_id": "start",
  "custom_monsters": {
    "monster_name": {
      "hit_dice": "2d8",
      "armor_class": 12,
      "attack_bonus": 2,
      "damage": "1d6",
      "special_abilities": ["Ability 1", "Ability 2"],
      "treasure": ["Item 1", "Item 2"]
    }
  },
  "nodes": [...]
}
```

Then use the monster name in any node's `monsters` array:

```json
{
  "node_id": "encounter",
  "title": "Boss Fight",
  "description": "The monster attacks!",
  "monsters": ["monster_name"],
  "choices": [...]
}
```

## Using the Adventure Builder

When adding monsters to a node:
1. Select option 9 "Custom monster (create your own)"
2. Enter monster name
3. Provide stats (hit dice, AC, attack bonus, damage)
4. Add special abilities (optional, one per line)
5. Add treasure carried (optional, one per line)

The custom monster definition is saved with the adventure and reused if you add the same monster to other nodes.

## Example

See [custom_monster_example.json](adventures/custom_monster_example.json) for a complete working example featuring:
- **Ice Troll**: A powerful regenerating boss monster
- **Frost Sprite**: A quick flying creature with ranged attacks

Both monsters have custom stats, special abilities, and treasure that wouldn't be possible with the predefined monster types.

## Benefits

- Create unique monsters specific to your adventure
- Define exact stats for balanced encounters
- Add custom special abilities and treasure
- No need to modify Python code to add new monster types
- Full compatibility with existing predefined monsters
