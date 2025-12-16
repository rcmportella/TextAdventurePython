# Adventure Builder - Interface Preview

This document shows what using the Adventure Builder looks like.

## Main Menu

```
======================================================================
ADVENTURE BUILDER - Interactive JSON Adventure Creator
======================================================================

Create text adventures easily with this guided interface!
No JSON knowledge required - we'll build it together.

----------------------------------------------------------------------
MAIN MENU
----------------------------------------------------------------------
1. Create New Adventure
2. Load Existing Adventure
3. Edit Current Adventure
4. View Adventure Structure
5. Validate Adventure
6. Save Adventure
7. Exit

Choice: _
```

## Creating a New Adventure

```
======================================================================
CREATE NEW ADVENTURE
======================================================================

Adventure Title: The Mysterious Cave

Enter a brief description/introduction for your adventure:
(This sets the scene for players)
> A strange cave has been discovered near your village. Local legends
speak of treasure within, but also of terrible dangers. Will you dare
to explore its depths?

What should be the starting node ID?
(Suggestion: 'start', 'beginning', or 'intro')
Starting node ID: cave_entrance

✓ Adventure 'The Mysterious Cave' created!
✓ Starting node will be: 'cave_entrance'

Create the starting node now? (y/n): y
```

## Creating a Node

```
======================================================================
CREATE NEW NODE
======================================================================

Node ID (lowercase, no spaces, e.g., 'forest_entrance'):
> cave_entrance

Node Title (shown to player):
> Cave Entrance

Node Description (what the player sees/experiences):
(Press Enter twice to finish, or type END on a new line)
> You stand before the mouth of a dark cave. Strange sounds echo
> from within, and a chill wind blows from the darkness. Moss covers
> the entrance, and you can see torchlight flickering deep inside.
> 
END

----------------------------------------------------------------------
Optional Elements (you can add these now or later)
----------------------------------------------------------------------

Add monsters? (y/n): n

Add treasure? (y/n): y

Add treasure items (one per line, empty line to finish):
Examples: '50 gold pieces', 'Potion of Healing', 'Magic sword +1'
> Torch
✓ Added: Torch
> 10 gold pieces
✓ Added: 10 gold pieces
> 

Add traps? (y/n): n

Is this an ending node?
1. No (has choices)
2. Victory ending
3. Defeat ending
Choice: 1

----------------------------------------------------------------------
ADD CHOICES
----------------------------------------------------------------------
Choices lead to other nodes. You'll need to create those nodes later.
(Empty text to finish adding choices)

--- New Choice ---
Choice text (what player sees): Enter the cave boldly
Existing nodes:
  - cave_entrance
Target node ID: cave_interior
Add requirements? (y/n): n
✓ Choice added → cave_interior
⚠️  Note: Node 'cave_interior' doesn't exist yet. Create it later.

--- New Choice ---
Choice text (what player sees): Turn back to the village
Existing nodes:
  - cave_entrance
Target node ID: retreat
Add requirements? (y/n): n
✓ Choice added → retreat
⚠️  Note: Node 'retreat' doesn't exist yet. Create it later.

--- New Choice ---
Choice text (what player sees): 

✓ Node 'cave_entrance' created successfully!
```

## Adding Monsters

```
Available monster types:
  1. goblin
  2. orc
  3. skeleton
  4. giant_spider
  5. zombie
  6. ogre
  7. troll
  8. dragon

Enter monster numbers separated by spaces (e.g., '1 1 2' for 2 goblins and 1 orc):
> 1 1 4
✓ Added 3 monster(s)
```

## Viewing Structure

```
======================================================================
ADVENTURE STRUCTURE: The Mysterious Cave
======================================================================

Description: A strange cave has been discovered near your village...
Starting Node: cave_entrance
Total Nodes: 5

----------------------------------------------------------------------
NODE MAP
----------------------------------------------------------------------

► cave_entrance
  Title: Cave Entrance
  💰 Treasure: 2 item(s)
  Choices:
    ✓ → cave_interior: Enter the cave boldly
    ✗ → deep_chamber: Venture deeper
    ✓ → retreat: Turn back to the village

  cave_interior
  Title: Inside the Cave
  ⚔️  Monsters: goblin, goblin, giant_spider
  Choices:
    ✗ → deep_chamber: Continue forward

  deep_chamber
  Title: The Deep Chamber
  ⚠️  Traps: 1
  Choices:
    ✓ → treasure_room: Open the chest
    ✓ → victory: Escape with treasure

  retreat [DEFEAT]
  Title: Too Scared
  
  victory [VICTORY]
  Title: Treasure Found!

Press Enter to continue...
```

## Validation

```
======================================================================
VALIDATING ADVENTURE
======================================================================

⚠️  WARNINGS:
  • Node 'deep_chamber' is unreachable

✓ No critical errors, but there are warnings to review.

Press Enter to continue...
```

## Edit Node Menu

```
----------------------------------------------------------------------
EDITING NODE: cave_interior
----------------------------------------------------------------------
Title: Inside the Cave
Description: You step into the cave. The air is cold and damp...
Monsters: 2
Treasure: 0
Traps: 0
Choices: 1
Victory: False, Defeat: False

What to edit?
1. Title
2. Description
3. Monsters
4. Treasure
5. Traps
6. Choices
7. Ending flags
8. Back

Choice: _
```

## Saving

```
======================================================================
SAVE ADVENTURE
======================================================================

Suggested filename: the_mysterious_cave.json
Filename (or Enter for suggested): 

⚠️  File exists. Overwrite? (y/n): y

✓ Adventure saved to: adventures/the_mysterious_cave.json
✓ 5 nodes saved
```

## Adding a Trap

```
--- Add Trap ---
Trap description (e.g., 'spike trap', 'poison dart'): falling rocks
Difficulty Class (DC) [10-25]: 15
Damage (e.g., '2d6', '1d8+2'): 3d6

Save type:
1. Reflex (dodge)
2. Fortitude (endurance)
3. Will (mental)
Choice [1]: 1

✓ Trap added: falling rocks (DC 15, 3d6 reflex)

Add another trap? (y/n): n
```

## Adding Requirements to a Choice

```
Add requirements? (y/n): y

Requirement type:
1. Ability score (e.g., Strength 15)
2. Item (e.g., needs 'key')
3. Level (e.g., level 3+)
4. No requirements

Choice: 1

Ability: str, dex, con, int, wis, cha
Ability: dex
Required dexterity score: 14

✓ Choice added with requirement: dexterity 14
```

## Multi-line Description Entry

```
Node Description (what the player sees/experiences):
(Press Enter twice to finish, or type END on a new line)
> You enter a grand chamber with high vaulted ceilings.
> Torches line the walls, casting flickering shadows.
> 
> At the far end, you see a massive throne made of bones.
> Sitting upon it is a skeletal figure wearing a crown.
> As you step forward, its eyes begin to glow red!
> 
END
```

## Features in Action

### Smart Formatting
- Node IDs automatically converted to lowercase with underscores
- Filenames auto-suggested from titles
- Empty inputs use sensible defaults

### Visual Indicators
- ► = Starting node
- ✓ = Valid/exists
- ✗ = Invalid/missing
- ⚔️  = Has monsters
- 💰 = Has treasure
- ⚠️  = Has traps
- [VICTORY] = Victory ending
- [DEFEAT] = Defeat ending

### User-Friendly
- Examples provided for every input
- Lists of available options shown
- Existing nodes displayed when creating choices
- Confirmation for destructive operations
- Clear error and success messages

---

This interface makes adventure creation intuitive and error-free!
