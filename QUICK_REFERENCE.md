# Quick Reference - JSON Adventures

## File Locations
- **Adventure files**: `adventures/*.json`
- **Template**: `adventures/template.json`
- **Documentation**: `ADVENTURE_JSON_FORMAT.md`

## Minimum Required Fields

```json
{
  "title": "Adventure Name",
  "description": "Introduction text",
  "starting_node_id": "start",
  "nodes": [
    {
      "node_id": "start",
      "title": "Location Name",
      "description": "What happens here",
      "choices": [
        {"text": "Option 1", "target": "node2"}
      ]
    },
    {
      "node_id": "node2",
      "title": "Victory!",
      "description": "You win!",
      "is_victory": true
    }
  ]
}
```

## Common Node Patterns

### Combat Node
```json
{
  "node_id": "battle",
  "title": "Combat!",
  "description": "Enemies attack!",
  "monsters": ["goblin", "goblin"],
  "treasure": ["50 gold pieces", "Potion of Healing"],
  "choices": [
    {"text": "Continue", "target": "next"}
  ]
}
```

### Trap Node
```json
{
  "node_id": "corridor",
  "title": "Trapped Hall",
  "description": "You see suspicious tiles...",
  "traps": [
    {
      "type": "spike trap",
      "dc": 15,
      "damage": "2d6",
      "save_type": "reflex"
    }
  ],
  "choices": [
    {"text": "Proceed carefully", "target": "next"}
  ]
}
```

### Locked Choice (Requires Ability)
```json
{
  "choices": [
    {
      "text": "Force the door open",
      "target": "locked_room",
      "requirements": {"strength": 15}
    },
    {
      "text": "Pick the lock",
      "target": "locked_room",
      "requirements": {"dexterity": 14}
    }
  ]
}
```

### Victory/Defeat Nodes
```json
{
  "node_id": "win",
  "title": "Victory!",
  "description": "You succeeded!",
  "is_victory": true
}
```

```json
{
  "node_id": "lose",
  "title": "Defeat",
  "description": "You failed...",
  "is_defeat": true
}
```

## Available Monster Types
- `goblin` (CR 1/2)
- `orc` (CR 1)
- `skeleton` (CR 1)
- `giant_spider` (CR 1)
- `zombie` (CR 1/2)
- `ogre` (CR 3)
- `troll` (CR 5)
- `dragon` (CR 10+)

## Treasure Format
- Gold: `"50 gold pieces"` (must include "gold")
- Potions: `"Potion of Healing"` (must include "potion")
- Other: Any descriptive string

## Requirements
- **Abilities**: `strength`, `dexterity`, `constitution`, `intelligence`, `wisdom`, `charisma`
- **Items**: `{"item": "key"}` (not fully implemented yet)
- **Level**: `{"level": 3}`

## Save Types for Traps
- `reflex` - Dodge/agility
- `fortitude` - Endurance/health
- `will` - Mental resistance

## Damage Dice Notation
- `1d4` - 1 die, 4 sides
- `2d6` - 2 dice, 6 sides each
- `3d8+5` - 3d8 plus 5

## Testing Your Adventure

```bash
# Quick test
python -c "from adventure_loader import AdventureLoader; adv = AdventureLoader.load_from_file('adventures/your_file.json'); print(f'Loaded: {adv.title}, Nodes: {len(adv.nodes)}')"

# Play it
python main.py
# Select option 3 and choose your file
```

## Common Mistakes

❌ Missing comma between nodes
❌ Forgetting closing brackets `]` or braces `}`
❌ Wrong node_id in target (typo)
❌ No victory or defeat node (infinite loop)
❌ starting_node_id doesn't match any node

## Tips

✓ Start with template.json
✓ Use descriptive node_ids (e.g., "goblin_cave" not "node1")
✓ Test each path thoroughly
✓ Provide multiple routes when possible
✓ Balance combat and exploration
✓ Include at least one victory and one defeat
✓ Use proper JSON formatting (online validators help)

## Example Workflow

1. **Copy template**
   ```bash
   cp adventures/template.json adventures/my_quest.json
   ```

2. **Edit in text editor**
   - Change title, description
   - Add/modify nodes
   - Connect choices to targets

3. **Validate JSON** (optional)
   - Use online JSON validator
   - Or: `python -c "import json; json.load(open('adventures/my_quest.json'))"`

4. **Test in game**
   - Run main.py
   - Select option 3
   - Choose your file

5. **Iterate**
   - Play through
   - Fix issues
   - Add content
   - Repeat

## Getting Help

- Full documentation: `ADVENTURE_JSON_FORMAT.md`
- System overview: `JSON_ADVENTURE_SYSTEM.md`
- Examples: `adventures/` directory
  - `goblin_cave.json` - Simple
  - `haunted_manor.json` - Medium
  - `dark_tower.json` - Complex
