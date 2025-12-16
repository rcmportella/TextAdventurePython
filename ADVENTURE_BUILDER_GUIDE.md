# Adventure Builder Guide

## Quick Start

The **Adventure Builder** is an interactive text interface that guides you through creating JSON adventures without any JSON knowledge.

### Running the Builder

```bash
python adventure_builder.py
```

## Main Features

### 1. Create New Adventure
Guides you step-by-step through:
- Setting title and description
- Defining the starting node
- Creating your first node

### 2. Load Existing Adventure
- Browse and load JSON files from `adventures/` directory
- Edit existing adventures

### 3. Edit Adventure
Full editing capabilities:
- **Add New Node**: Create locations, encounters, choices
- **Edit Existing Node**: Modify any aspect of a node
- **Delete Node**: Remove unwanted nodes
- **Edit Adventure Info**: Change title, description, starting node

### 4. View Adventure Structure
Visual map showing:
- All nodes and their connections
- Starting node marked with ►
- Victory/Defeat endings marked
- Missing node connections (✗)
- Requirements indicators

### 5. Validate Adventure
Automatically checks for:
- Missing nodes referenced in choices
- Unreachable nodes
- Missing endings
- Nodes without choices

### 6. Save Adventure
- Saves to `adventures/` directory
- Suggests filename based on title
- Warns before overwriting

## Creating a Node

When creating a node, you'll be asked for:

1. **Node ID**: Unique identifier (lowercase, underscores)
   - Example: `forest_entrance`, `dragon_lair`

2. **Title**: Short name shown to player
   - Example: "The Dark Forest"

3. **Description**: Full narrative text
   - Type your description
   - Press Enter twice or type END to finish

4. **Monsters** (optional):
   - Choose from list: goblin, orc, skeleton, etc.
   - Add multiple (e.g., "1 1 2" = 2 goblins + 1 orc)

5. **Treasure** (optional):
   - List items line by line
   - Examples: "50 gold pieces", "Potion of Healing"

6. **Traps** (optional):
   - Type: Description (e.g., "spike trap")
   - DC: Difficulty (10-25)
   - Damage: Dice notation (e.g., "2d6")
   - Save Type: Reflex, Fortitude, or Will

7. **Ending Type**:
   - Normal node (has choices)
   - Victory ending
   - Defeat ending

8. **Choices** (for non-ending nodes):
   - Choice text: What player sees
   - Target node: Where it leads
   - Requirements: Optional (ability scores, items, level)

## Workflow Example

### Creating "The Lost Ring" Adventure

1. **Start Builder**
   ```
   python adventure_builder.py
   ```

2. **Choose Option 1**: Create New Adventure
   - Title: "The Lost Ring"
   - Description: "Find the magical ring hidden in the forest."
   - Starting node: "forest_entrance"

3. **Create Starting Node** (forest_entrance)
   - Title: "Forest Entrance"
   - Description: "You stand at the edge of a dark forest."
   - No monsters, treasure, or traps
   - Add choices:
     - "Enter the forest" → deep_forest
     - "Turn back" → defeat

4. **Add Second Node** (deep_forest)
   - Title: "Deep Forest"
   - Description: "You find a chest under an old tree!"
   - Treasure: "Magic Ring", "50 gold pieces"
   - Add choice:
     - "Take the treasure and leave" → victory

5. **Add Victory Node** (victory)
   - Title: "Success!"
   - Description: "You found the magic ring!"
   - Mark as: Victory ending

6. **Add Defeat Node** (defeat)
   - Title: "Gave Up"
   - Description: "You turned back without finding the ring."
   - Mark as: Defeat ending

7. **View Structure** (Option 4)
   - Check all nodes are connected
   - Verify no broken links

8. **Validate** (Option 5)
   - Should pass with no errors

9. **Save** (Option 6)
   - Filename: "lost_ring.json"
   - Saved to `adventures/lost_ring.json`

10. **Play Your Adventure**
    - Run `python main.py`
    - Select option 3
    - Choose your adventure file

## Tips

### Node IDs
✓ Use descriptive names: `goblin_cave`, `throne_room`  
✗ Avoid: `node1`, `n2`, `x`

### Descriptions
✓ Be descriptive and engaging  
✓ Use multiple lines for better formatting  
✗ Don't make them too long (players need to read)

### Choices
✓ Give players meaningful options  
✓ Include at least 2 choices per node  
✓ Use requirements sparingly  
✗ Don't create dead ends (nodes with no choices)

### Structure
✓ Create main path first, then branches  
✓ Always include at least one victory and one defeat  
✓ Test all paths after creating  
✗ Don't leave nodes unreachable

### Validation
- Run validation before saving
- Fix all errors (red ❌)
- Review warnings (yellow ⚠️)
- Test play your adventure

## Common Patterns

### Combat Node
1. Add monsters
2. Add treasure (rewards after combat)
3. Add choices for next location

### Puzzle Node
1. Add multiple choices
2. Use requirements on choices (e.g., Intelligence 14)
3. Wrong choices lead to traps or defeat

### Boss Fight
1. Add powerful monster (ogre, dragon)
2. Maybe add trap too
3. Victory choice leads to end

### Branching Path
1. Create hub node with multiple choices
2. Each choice leads to different area
3. Areas reconnect later or have separate endings

## Keyboard Shortcuts

- **Enter**: Confirm/continue
- **Empty line**: Finish multi-line input
- **END**: Alternative way to finish descriptions
- **y/n**: Quick yes/no responses

## Troubleshooting

### "Node doesn't exist yet"
- This is just a warning
- Create the target node later
- Use View Structure to see missing nodes

### "Unreachable node"
- Node exists but no path leads to it
- Add a choice from another node pointing to it
- Or delete if not needed

### "No victory ending"
- You need at least one node marked as victory
- Edit a node and set it as victory ending

### File won't save
- Check adventures/ directory exists
- Verify you have write permissions
- Try a different filename

## Advanced Features

### Loading and Editing
- Load existing adventures to modify them
- Add new branches to completed adventures
- Fix mistakes in saved adventures

### Requirements
Make choices conditional on:
- **Ability Scores**: "strength": 15
- **Items**: "item": "key" (not fully implemented)
- **Level**: "level": 3

### Multiple Paths
- Create different routes to victory
- Add optional side quests
- Include shortcuts for skilled players

## Next Steps

After creating your adventure:
1. Validate it (Option 5)
2. Save it (Option 6)
3. Play test it (`python main.py`)
4. Get feedback
5. Load and refine (Option 2)
6. Share your JSON file!

## Getting Help

- See full JSON format: `ADVENTURE_JSON_FORMAT.md`
- Quick reference: `QUICK_REFERENCE.md`
- Examples: Browse `adventures/` directory

---

**Happy Adventure Building!** 🎮✨
