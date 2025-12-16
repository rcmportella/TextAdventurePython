# Quick Start Guide

## Running the Game

1. **Play the full interactive game:**
   ```bash
   python main.py
   ```
   or
   ```bash
   py main.py
   ```

2. **Run the simple example:**
   ```bash
   python example.py
   ```

## Creating Your First Adventure

### Step 1: Import Required Classes

```python
from node import Adventure, GameNode
from character import Character
from game import GameEngine, GameUI
```

### Step 2: Create an Adventure

```python
adventure = Adventure(
    title="My First Adventure",
    description="A brave hero's journey begins...",
    starting_node_id="start"
)
```

### Step 3: Create Nodes

```python
# Starting node
start_node = GameNode(
    node_id="start",
    title="The Village",
    description="You are in a peaceful village. An old man approaches you."
)

# Add a choice
start_node.add_choice("Listen to the old man", "quest_given")

# Add to adventure
adventure.add_node(start_node)

# Create more nodes...
quest_node = GameNode(
    node_id="quest_given",
    title="The Quest",
    description="The old man tells you about a monster in the forest..."
)

quest_node.add_choice("Go to the forest", "forest")
quest_node.add_choice("Refuse the quest", "defeat")
adventure.add_node(quest_node)
```

### Step 4: Add Combat Encounters

```python
forest = GameNode(
    node_id="forest",
    title="Dark Forest",
    description="You enter the forest and encounter a goblin!"
)

# Add monsters
forest.add_monster_encounter('goblin')

# Add treasure for after combat
forest.add_treasure(["30 gold pieces", "Potion of Healing"])

forest.add_choice("Return to village victorious", "victory")
adventure.add_node(forest)
```

### Step 5: Create Endings

```python
# Victory
victory = GameNode(
    node_id="victory",
    title="Victory!",
    description="You have saved the village! The people celebrate your bravery!"
)
victory.set_victory()
adventure.add_node(victory)

# Defeat
defeat = GameNode(
    node_id="defeat",
    title="The End",
    description="You refused the quest and returned home. The monster continues to terrorize the village."
)
defeat.set_defeat()
adventure.add_node(defeat)
```

### Step 6: Create Character and Play

```python
# Create character
hero = Character("Hero", "Fighter", level=1)
hero.roll_abilities()

# Start game
game = GameEngine(adventure, hero)
ui = GameUI()

# Simple game loop
result = game.start_game()
ui.display_node(game.current_node)
ui.display_choices(game.current_node)

# Player makes choices...
choice = int(input("Your choice: ")) - 1
result = game.handle_choice(choice)
```

## Advanced Features

### Adding Traps

```python
dungeon = GameNode(node_id="dungeon", title="Dungeon", description="...")
dungeon.add_trap(
    trap_type="poison dart trap",
    dc=15,                      # Difficulty Class
    damage="2d6",               # Damage dice
    save_type='reflex'          # Type of saving throw
)
```

### Choice Requirements

```python
# Requires high strength
door.add_choice(
    "Break down the door",
    "inside",
    requirements={'strength': 16}
)

# Requires an item
gate.add_choice(
    "Use the key",
    "treasury",
    requirements={'item': 'Golden Key'}
)

# Requires character level
ritual.add_choice(
    "Perform the ritual",
    "summoning",
    requirements={'level': 5}
)
```

### On-Enter Events

```python
def heal_fountain(character, node):
    character.heal(20)
    return "The magical fountain restores your health! (+20 HP)"

healing_room = GameNode(node_id="fountain", title="...", description="...")
healing_room.add_on_enter_event(heal_fountain)
```

### Combat Actions

Players can:
1. **Attack** - Basic weapon attack
2. **Cast Spell** - Use magic (if spellcaster)
3. **Use Item** - Consume potions, etc.
4. **Flee** - Attempt to escape combat

### Character Classes

- **Fighter**: High HP (d10), high BAB, strong in combat
- **Wizard**: Low HP (d4), powerful spells, intelligence-based
- **Rogue**: Medium HP (d6), good reflexes, agile
- **Cleric**: Medium HP (d8), healing spells, wisdom-based

### Available Monsters

| Monster | Difficulty | Special |
|---------|-----------|---------|
| Goblin | Easy | Quick and sneaky |
| Skeleton | Easy | Undead |
| Giant Spider | Easy | Poison |
| Zombie | Easy | Undead, slow |
| Orc | Medium | Strong warrior |
| Troll | Hard | Regeneration |
| Ogre | Hard | Large giant |
| Dragon | Boss | Breath weapon |

### Spell Examples

```python
from spell import get_spell

# Get a spell
fireball = get_spell('fireball')
magic_missile = get_spell('magic_missile')
cure_wounds = get_spell('cure_light_wounds')

# Learn spell
wizard.learn_spell(fireball)

# Cast spell in combat
success, result = wizard.cast_spell(fireball, target=monster)
```

## Testing Your Adventure

1. Create a small test adventure with 3-5 nodes
2. Include at least one combat encounter
3. Add one treasure and one trap
4. Test all paths (victory and defeat)
5. Verify choices work correctly

## Tips

1. **Balance**: Start with easy monsters (goblins) and escalate difficulty
2. **Rewards**: Give treasure for exploration and combat
3. **Choices**: Provide meaningful alternatives, not just linear paths
4. **Description**: Make locations vivid and engaging
5. **Testing**: Play through your adventure multiple times

## Common Patterns

### Linear Quest
```
Start → Challenge → Boss → Victory
```

### Branching Paths
```
Start → {Path A, Path B} → Merge → End
```

### Hub and Spokes
```
Central Hub → {Quest 1, Quest 2, Quest 3} → Return to Hub → Final
```

### Multiple Endings
```
Start → Choices → {Victory A, Victory B, Defeat A, Defeat B}
```

## Need Help?

- Check [README.md](README.md) for detailed documentation
- Look at [sample_adventure.py](sample_adventure.py) for examples
- Run [example.py](example.py) to see the framework in action

Happy adventuring!
