# Text Adventure Python - Project Structure

## Complete File Listing

```
TextAdventurePython/
│
├── README.md              # Complete documentation
├── QUICKSTART.md          # Quick start guide for beginners
├── requirements.txt       # Python dependencies (none required)
│
├── Core System Files:
│   ├── dice.py           # Dice rolling utilities (d4-d100, ability scores, modifiers)
│   ├── character.py      # Character class with D20 mechanics
│   ├── spell.py          # Spell system with multiple spells
│   ├── monster.py        # Monster classes and factory
│   ├── combat.py         # Combat system and items
│   ├── node.py           # GameNode and Adventure classes
│   └── game.py           # Game engine and UI
│
├── Adventure Files:
│   └── sample_adventure.py   # Two sample adventures included
│
└── Entry Points:
    ├── main.py           # Interactive game launcher
    └── example.py        # Programmatic example

## Module Overview

### dice.py (80 lines)
- Dice rolling functions (d4, d6, d8, d10, d12, d20, d100)
- Ability score generation (4d6 drop lowest)
- Modifier calculation

### character.py (280 lines)
- Character class with 6 ability scores
- 4 character classes (Fighter, Wizard, Rogue, Cleric)
- Combat mechanics (attack rolls, saving throws)
- Spell casting system
- Inventory management
- Experience and leveling

### spell.py (280 lines)
- Base Spell class
- 10 implemented spells across 3 levels
- Spell effects (damage, healing, buffs)
- Spell library and lookup functions

### monster.py (260 lines)
- Base Monster class
- 8 predefined monster types
- Monster factory function
- Special abilities support

### combat.py (260 lines)
- Turn-based combat system
- Initiative rolling
- Combat actions (attack, spell, item, flee)
- Item classes (potions, weapons, armor)
- Combat log and rewards

### node.py (300 lines)
- GameNode class for locations
- Adventure container class
- Choice system with requirements
- Trap system
- Treasure collection
- On-enter events

### game.py (280 lines)
- GameEngine for managing game flow
- Node processing
- Combat handling
- Save/load system
- GameUI for display

### sample_adventure.py (360 lines)
- "The Dark Tower" - full adventure with 14 nodes
- "The Goblin Cave" - simple 5-node adventure
- Demonstrates all framework features

### main.py (280 lines)
- Interactive game launcher
- Character creation wizard
- Full game loop with combat
- Menu system

### example.py (110 lines)
- Programmatic usage example
- Mini 3-node adventure
- Automated combat demo

## Total Stats

- **12 Python files**
- **~2,500 lines of code**
- **0 external dependencies**
- **2 complete sample adventures**
- **8 monster types**
- **10 spells**
- **4 character classes**

## Features Implemented

### D20/OGL Systems
✅ 6 ability scores (STR, DEX, CON, INT, WIS, CHA)
✅ Ability modifiers
✅ Attack rolls (d20 + BAB + modifiers)
✅ Armor Class (AC)
✅ Hit Points and Hit Dice
✅ Saving throws (Fortitude, Reflex, Will)
✅ Base Attack Bonus (BAB)
✅ Experience points and leveling
✅ Spell slots and spell levels
✅ Monster Challenge Ratings

### Game Systems
✅ Node-based adventure structure
✅ Multiple choice navigation
✅ Combat encounters
✅ Treasure collection
✅ Trap system with saving throws
✅ Inventory management
✅ Spell casting
✅ Item usage
✅ Victory/defeat conditions
✅ Save/load functionality
✅ Character creation
✅ Initiative system
✅ Turn-based combat

### Content
✅ 2 complete adventures
✅ 8 monster types
✅ 10 spells (cantrips to level 3)
✅ 4 character classes
✅ Multiple combat actions
✅ Various items (potions, weapons, armor)

## Usage Patterns

### For Players
```bash
python main.py  # Start interactive game
```

### For Developers
```python
# Import framework
from character import Character
from node import Adventure, GameNode
from game import GameEngine

# Create content
adventure = Adventure(...)
character = Character(...)
game = GameEngine(adventure, character)

# Run game
result = game.start_game()
```

### For Learning
```bash
python example.py  # See framework in action
```

## Extension Points

Want to extend the framework? Here's what you can add:

1. **New Monster Types**: Add classes in `monster.py`
2. **New Spells**: Add classes in `spell.py`
3. **New Items**: Add classes in `combat.py`
4. **New Adventures**: Create files like `sample_adventure.py`
5. **New Classes**: Extend `Character` in `character.py`
6. **New Node Types**: Extend `GameNode` in `node.py`

## Architecture

```
┌─────────────┐
│   main.py   │  ← Entry point
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   game.py   │  ← Game engine
└──────┬──────┘
       │
       ├→ node.py (Adventure, GameNode)
       ├→ character.py (Character)
       ├→ combat.py (Combat, Items)
       ├→ spell.py (Spells)
       ├→ monster.py (Monsters)
       └→ dice.py (Dice rolls)
```

## Design Principles

1. **Modular**: Each system is independent
2. **Extensible**: Easy to add new content
3. **OOP**: Proper object-oriented design
4. **D20 Compliant**: Follows OGL rules
5. **No Dependencies**: Pure Python
6. **Well Documented**: Comments and docstrings
7. **Example-Driven**: Multiple working examples

## Testing Checklist

- [x] Character creation works
- [x] Ability score generation
- [x] Combat system functional
- [x] Spell casting works
- [x] Monster encounters
- [x] Node navigation
- [x] Treasure collection
- [x] Trap system
- [x] Victory/defeat conditions
- [x] Save/load (basic)
- [x] Multiple adventures
- [x] All spells tested
- [x] All monsters tested
- [x] Choice requirements work
- [x] On-enter events work

Everything is fully functional and ready to use!
