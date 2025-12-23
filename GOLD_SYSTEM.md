# Gold System and Node Events

## Overview

The Text Adventure system now supports a comprehensive gold/currency system that allows you to:
- Track player gold
- Add gold as treasure
- Deduct gold when entering specific nodes (tolls, fees, purchases, etc.)
- Create custom on-enter events for nodes

## Gold Tracking

### Character Gold Attribute

All characters now have a `gold` attribute that tracks their current wealth:

```python
character = Character("Hero", "Fighter", 1)
print(character.gold)  # Starts at 0

character.add_gold(100)  # Add 100 gold
print(character.gold)  # Now 100

character.remove_gold(30)  # Remove 30 gold (returns True if successful)
print(character.gold)  # Now 70
```

The `remove_gold()` method returns `True` if the character has enough gold, or `False` if they don't have enough.

## Using Gold in Adventures

### Adding Gold as Treasure

Gold can be added as treasure in any node. The system automatically detects items containing "gold" in their description:

**In JSON:**
```json
{
  "node_id": "treasure_room",
  "title": "Treasure Room",
  "description": "A room filled with treasure!",
  "treasure": ["100 gold pieces", "Potion of Healing"]
}
```

**In Python:**
```python
node = GameNode("treasure_room", "Treasure Room", "A room filled with treasure!")
node.add_treasure(["100 gold pieces", "Potion of Healing"])
```

When the player collects this treasure, the gold is automatically added to their `character.gold` attribute.

### Gold Costs (Entry Fees)

You can set a gold cost for entering a node. This is useful for:
- Toll bridges
- Shop purchases
- Bribes
- Entry fees to locations
- Any situation where the player must pay gold

**In JSON:**
```json
{
  "node_id": "toll_bridge",
  "title": "The Toll Bridge",
  "description": "A troll demands payment to cross.",
  "gold_cost": 30,
  "choices": [
    {
      "text": "Cross the bridge",
      "target": "other_side"
    }
  ]
}
```

**In Python:**
```python
node = GameNode("toll_bridge", "The Toll Bridge", "A troll demands payment to cross.")
node.set_gold_cost(30)
node.add_choice("Cross the bridge", "other_side")
```

### How Gold Costs Work

When a player enters a node with a gold cost:
1. The system automatically attempts to deduct the gold from the player
2. If successful, a message displays: "You pay 30 gold to enter. (Remaining: 70 gp)"
3. If the player doesn't have enough gold, a warning displays: "WARNING: You don't have enough gold! (20/30 gp needed)"
4. The player can still proceed even without enough gold (you can add requirements to prevent this if needed)

## Example Adventure

See [toll_bridge_example.json](adventures/toll_bridge_example.json) for a complete working example that demonstrates:
- Finding gold as treasure
- Paying a toll to cross a bridge
- Tracking gold throughout the adventure

To play this example:
1. Run the game
2. Select "Load Custom Adventure"
3. Choose `adventures/toll_bridge_example.json`

## Advanced: Custom On-Enter Events

For more complex scenarios, you can create custom on-enter events in Python:

```python
def custom_gold_event(character, node):
    """Custom event that gives bonus gold to high-level characters"""
    if character.level >= 5:
        bonus = 50
        character.add_gold(bonus)
        return f"As a renowned hero, you receive a bonus of {bonus} gold!"
    return None

node = GameNode("guild_hall", "Guild Hall", "The adventurer's guild greets you.")
node.add_on_enter_event(custom_gold_event)
```

On-enter events can:
- Modify character stats
- Add/remove items or gold
- Check conditions and provide different outcomes
- Return a message to display to the player (or None for no message)

## Character Sheet Display

Gold is now displayed in both compact and detailed character sheets:

**Compact:**
```
Hero - Level 1 Fighter
HP: 12/12 | AC: 13 | Gold: 150
STR: 16 DEX: 13 CON: 14
INT: 10 WIS: 12 CHA: 8
```

**Detailed:**
```
COMBAT STATS:
  Hit Points:        12/12
  Armor Class:       13
  Base Attack Bonus: +1
  Experience:        0 XP
  Gold:              150 gp
```

## Integration with Existing Systems

The gold system integrates seamlessly with:
- **Treasure collection**: Gold found in treasure is automatically added
- **Character sheets**: Gold is displayed in status screens
- **JSON adventures**: Gold costs can be defined in JSON files
- **Save/load**: Gold is tracked with all other character stats

## Tips for Adventure Design

1. **Balance gold rewards**: Make sure players can earn enough gold to pay for costs
2. **Optional expenses**: Use gold costs for optional paths or bonuses, not required progression (unless you give enough gold)
3. **Visual feedback**: The system always shows remaining gold after transactions
4. **Strategic choices**: Create interesting decisions where players must choose between spending gold or saving it

## Example Usage Patterns

### Pattern 1: Shop/Merchant
```json
{
  "node_id": "shop",
  "title": "Merchant's Shop",
  "description": "A merchant offers to sell you a magic sword for 100 gold.",
  "choices": [
    {
      "text": "Buy the magic sword (100 gold)",
      "target": "buy_sword"
    },
    {
      "text": "Leave the shop",
      "target": "town_square"
    }
  ]
},
{
  "node_id": "buy_sword",
  "title": "Purchase Complete",
  "description": "You purchase the magic sword!",
  "gold_cost": 100,
  "treasure": ["Magic Sword +1"],
  "choices": [
    {
      "text": "Return to town",
      "target": "town_square"
    }
  ]
}
```

### Pattern 2: Multiple Toll Options
```json
{
  "node_id": "guard_post",
  "title": "Guard Post",
  "description": "Guards block the gate. You can pay a fee or try to sneak past.",
  "choices": [
    {
      "text": "Pay the guards (50 gold)",
      "target": "gate_paid"
    },
    {
      "text": "Try to sneak past (DEX 15)",
      "target": "gate_sneak",
      "requirements": {"dexterity": 15}
    }
  ]
},
{
  "node_id": "gate_paid",
  "title": "Through the Gate",
  "description": "The guards let you pass.",
  "gold_cost": 50,
  "choices": [...]
}
```

### Pattern 3: Risk vs Reward
```json
{
  "node_id": "gambling_den",
  "title": "Gambling Den",
  "description": "You can gamble 20 gold for a chance at a bigger reward.",
  "choices": [
    {
      "text": "Gamble 20 gold",
      "target": "gamble_result"
    },
    {
      "text": "Leave",
      "target": "exit"
    }
  ]
},
{
  "node_id": "gamble_result",
  "title": "Gambling Results",
  "description": "You roll the dice...",
  "gold_cost": 20,
  "treasure": ["100 gold pieces"],
  "choices": [...]
}
```

## Summary

The gold system adds economic gameplay to your text adventures:
- ✅ Automatic tracking of player wealth
- ✅ Easy-to-use JSON format for gold costs
- ✅ Visual feedback for all transactions
- ✅ Flexible event system for custom behaviors
- ✅ Full integration with character and adventure systems

Start using it in your adventures today!
