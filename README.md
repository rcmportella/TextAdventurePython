# Text Adventure Game Framework - D20 OGL System

A comprehensive Python framework for creating gamebook-style text adventures using D20/OGL (Open Game License) mechanics.

## Features

### Core Systems
- **D20 Combat System**: Full implementation of D20 combat mechanics including attack rolls, saving throws, and damage
- **Character System**: Complete character creation with 6 ability scores (STR, DEX, CON, INT, WIS, CHA), class selection, and level progression
- **Spell System**: OGL-based spellcasting with spell levels, spell slots, and various spell effects
- **Monster System**: Diverse monster types with hit dice, armor class, attack bonuses, and special abilities
- **Node-based Adventure**: Gamebook paragraph system where each node has descriptions, choices, and encounters

### Game Elements
- **Combat**: Turn-based combat with initiative rolls, attack rolls, and damage calculation
- **Exploration**: Navigate through interconnected story nodes with multiple choice paths
- **Encounters**: Monsters, treasures, and traps at various locations
- **Character Progression**: Experience points and level-up system
- **Inventory**: Item collection and usage system
- **Saving/Loading**: Basic game state persistence

## File Structure

```
TextAdventurePython/
├── dice.py                # Dice rolling utilities (d4, d6, d8, d10, d12, d20, d100)
├── character.py           # Character class with D20 attributes and mechanics
├── spell.py               # Spell system with various spells (Magic Missile, Fireball, etc.)
├── monster.py             # Monster classes (Goblin, Orc, Dragon, etc.)
├── combat.py              # Combat system and item classes
├── node.py                # GameNode and Adventure classes for gamebook structure
├── game.py                # Main game engine and UI
├── sample_adventure.py    # Example adventures (The Dark Tower, The Goblin Cave)
├── adventure_loader.py    # JSON adventure loading and exporting system
├── export_adventures.py   # Utility to export Python adventures to JSON
├── main.py                # Entry point to run the game
├── adventures/            # Directory for JSON adventure files
│   ├── dark_tower.json    # The Dark Tower adventure in JSON format
│   ├── goblin_cave.json   # The Goblin Cave adventure in JSON format
│   └── template.json      # Template for creating new adventures
├── ADVENTURE_JSON_FORMAT.md  # Documentation for JSON adventure format
├── QUICKSTART.md          # Quick start guide
└── README.md              # This file
```

## Quick Start

### Running the Game

```bash
python main.py
```

### Character Classes

1. **Fighter**: High HP, strong melee combat, best BAB (Base Attack Bonus)
2. **Wizard**: Spellcaster with powerful magic, lower HP
3. **Rogue**: Agile with good reflexes, moderate combat ability
4. **Cleric**: Holy warrior with healing spells and combat skills

### Sample Adventures

- **The Dark Tower**: Full-featured adventure with multiple paths, secrets, and a boss fight
- **The Goblin Cave**: Shorter adventure perfect for testing the system

## Creating Your Own Adventure

### Option 1: Interactive Builder (Easiest!) 🎯

Use the **Adventure Builder** - a guided text interface that creates JSON files for you. No JSON or coding knowledge needed!

```bash
python adventure_builder.py
```

The builder provides:
- ✓ Step-by-step guidance
- ✓ Interactive menus
- ✓ Automatic validation
- ✓ Visual structure viewer
- ✓ Easy node creation and editing

See [ADVENTURE_BUILDER_GUIDE.md](ADVENTURE_BUILDER_GUIDE.md) for detailed instructions.

### Option 2: JSON File Format (Manual)

Create adventures by editing JSON files directly.

#### Quick Start with JSON

1. **Copy the template**:
   ```bash
   cp adventures/template.json adventures/my_adventure.json
   ```

2. **Edit the JSON file** with any text editor:
   ```json
   {
     "title": "My Adventure",
     "description": "Your adventure description",
     "starting_node_id": "start",
     "nodes": [
       {
         "node_id": "start",
         "title": "Starting Point",
         "description": "The adventure begins...",
         "choices": [
           {"text": "Go forward", "target": "next_node"}
         ]
       }
     ]
   }
   ```

3. **Run the game** and select option 3 to load your custom adventure

#### JSON Format Details

See [ADVENTURE_JSON_FORMAT.md](ADVENTURE_JSON_FORMAT.md) for complete documentation including:
- Full JSON schema
- Field descriptions
- Requirements system (ability scores, items, levels)
- Monsters, treasure, and traps
- Example adventures

#### Benefits of JSON Format
- ✓ No Python knowledge needed
- ✓ Easy to edit and share
- ✓ Version control friendly
- ✓ Visual editor compatible
- ✓ Rapid prototyping

### Option 3: Python Code (Advanced)

For adventures requiring custom logic or events, use Python:

```python
from node import Adventure, GameNode
from character import Character
from game import GameEngine

# Create adventure
adventure = Adventure(
    title="My Adventure",
    description="An epic quest...",
    starting_node_id="start"
)

# Create a node
node = GameNode(
    node_id="start",
    title="The Beginning",
    description="You stand at the entrance..."
)

# Add encounters
node.add_monster_encounter(['goblin', 'goblin'])

# Add treasure
node.add_treasure(["50 gold pieces", "Potion of Healing"])

# Add traps
node.add_trap("spike trap", dc=15, damage="2d6", save_type='reflex')

# Add choices
node.add_choice("Go north", "north_room")
node.add_choice("Go east", "east_room", requirements={'strength': 14})

# Add custom events
def special_event(character, node):
    character.gain_xp(100)
    return "You feel more experienced!"

node.add_on_enter_event(special_event)

# Mark endings
node.set_victory()  # or node.set_defeat()

# Add to adventure
adventure.add_node(node)

# Export to JSON (optional)
from adventure_loader import AdventureExporter
AdventureExporter.export_to_file(adventure, 'adventures/my_adventure.json')
```

### Converting Python Adventures to JSON

Use the export utility to convert existing Python adventures:

```bash
python export_adventures.py
```

This will create JSON files for all built-in adventures in the `adventures/` directory.

### Validating JSON Adventures

Before playing a custom adventure, validate it to check for errors:

```bash
python validate_adventure.py adventures/my_adventure.json
```

The validator checks for:
- ✓ Valid JSON syntax
- ✓ Required fields present
- ✓ All target nodes exist
- ✓ Node reachability
- ✓ Valid monster types
- ✓ Proper trap structure
- ✓ Victory/defeat endings

### Available Example Adventures

The `adventures/` directory includes:
- **dark_tower.json** - Complex adventure with 14 nodes, multiple paths, secrets
- **goblin_cave.json** - Simple 5-node adventure, good for learning
- **haunted_manor.json** - Medium 8-node ghost story
- **template.json** - Blank template for creating new adventures
```

### Monster Types

Available monsters:
- `goblin`: Weak humanoid (CR 1/2)
- `orc`: Medium warrior (CR 1)
- `skeleton`: Undead (CR 1)
- `giant_spider`: Venomous (CR 1)
- `zombie`: Slow undead (CR 1/2)
- `ogre`: Large giant (CR 3)
- `troll`: Regenerating (CR 5)
- `dragon`: Boss-level threat (CR 10+)

### Spells

Available spells by level:

**Cantrips (Level 0):**
- Detect Magic
- Ray of Frost

**Level 1:**
- Magic Missile
- Cure Light Wounds
- Shield
- Burning Hands
- Bless

**Level 3:**
- Fireball
- Lightning Bolt

### Adding Custom Spells

```python
from spell import Spell
import dice

class CustomSpell(Spell):
    def __init__(self):
        super().__init__(
            name="My Spell",
            level=1,
            school="Evocation",
            description="Does something cool"
        )
    
    def cast(self, caster, target=None):
        # Implement spell effect
        damage = dice.d6(3)
        target.take_damage(damage)
        return f"Spell hits for {damage} damage!"
```

### Adding Custom Monsters

```python
from monster import Monster

class CustomMonster(Monster):
    def __init__(self):
        super().__init__(
            name="My Monster",
            hit_dice="3d8+3",
            armor_class=15,
            attack_bonus=4,
            damage="1d8+2",
            treasure=["30 gold pieces"]
        )
```

## D20 Mechanics

### Ability Scores
- Range: 3-18 (10-11 is average)
- Modifier: (Score - 10) / 2 (rounded down)
- Used for: Attack rolls, saving throws, skill checks

### Combat
- **Attack Roll**: d20 + BAB + ability modifier vs. AC
- **Damage**: Weapon dice + strength modifier
- **Critical Hit**: Natural 20 (automatic hit)
- **Critical Miss**: Natural 1 (automatic miss)

### Saving Throws
- **Fortitude**: CON-based (resist poison, disease)
- **Reflex**: DEX-based (dodge, avoid traps)
- **Will**: WIS-based (resist mind effects)

### Spell Slots
Characters have limited spell slots per day based on level and class.

## Game Commands

During gameplay:
- Enter **number** to make a choice
- **S** - View character status
- **H** - Help
- **Q** - Quit game

During combat:
1. Attack (basic melee/ranged attack)
2. Cast Spell (if available)
3. Use Item (potions, etc.)
4. Attempt to Flee

## Advanced Features

### Choice Requirements

You can require specific conditions for choices:

```python
# Requires item
node.add_choice("Use the key", "locked_room", requirements={'item': 'Ancient Key'})

# Requires ability score
node.add_choice("Break down the door", "inside", requirements={'strength': 16})

# Requires level
node.add_choice("Cast ritual", "ritual_room", requirements={'level': 5})
```

### On-Enter Events

Execute custom code when entering a node:

```python
def heal_player(character, node):
    character.heal(10)
    return "You feel refreshed! (+10 HP)"

node.add_on_enter_event(heal_player)
```

### Victory and Defeat Conditions

```python
victory_node.set_victory()  # Player wins
defeat_node.set_defeat()    # Player loses
```

## Tips for Adventure Design

1. **Start Simple**: Create a linear path first, then add branches
2. **Balance Combat**: Mix easy and challenging encounters
3. **Reward Exploration**: Hide treasure in optional paths
4. **Multiple Solutions**: Offer different approaches (combat, stealth, diplomacy)
5. **Clear Descriptions**: Make locations vivid and choices clear
6. **Test Difficulty**: Ensure encounters are appropriate for character level

## System Requirements

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

## License

This framework follows the Open Game License (OGL) for D20 game mechanics.

## Contributing

To extend the framework:

1. Add new monster types in [monster.py](monster.py)
2. Create new spells in [spell.py](spell.py)
3. Design new adventures in a new file like [sample_adventure.py](sample_adventure.py)
4. Extend character classes in [character.py](character.py)

## Credits

Created as a complete D20/OGL text adventure framework demonstrating:
- Object-oriented game design
- Node-based narrative structure
- D20 combat mechanics
- Spell system implementation
- Turn-based combat
- State management

Enjoy creating your own adventures!
"# TextAdventurePython" 
