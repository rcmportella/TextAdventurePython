"""
Node/Paragraph system for gamebook-style adventures
"""
from combat import Combat, HealingPotion
from monster import create_monster
import dice


class GameNode:
    """
    Represents a paragraph/location in the gamebook.
    Each node has a description and can contain encounters, choices, etc.
    """
    
    def __init__(self, node_id, title, description):
        """
        Initialize a game node.
        
        Args:
            node_id: Unique identifier for this node
            title: Short title for the node
            description: Full text description of the location/scene
        """
        self.node_id = node_id
        self.title = title
        self.description = description
        
        # Encounters and events
        self.monsters = []  # List of monster types to encounter
        self.treasure = []  # Items/gold found here
        self.traps = []     # Trap definitions
        
        # Choices that lead to other nodes
        self.choices = []   # List of (choice_text, target_node_id, requirements)
        
        # Node type
        self.is_victory = False
        self.is_defeat = False
        
        # Events that trigger when entering node
        self.on_enter_events = []
        
    def add_monster_encounter(self, monster_types):
        """
        Add monsters to encounter at this node.
        
        Args:
            monster_types: List of monster type strings or single string
        """
        if isinstance(monster_types, str):
            self.monsters.append(monster_types)
        else:
            self.monsters.extend(monster_types)
            
    def add_treasure(self, items):
        """
        Add treasure to this node.
        
        Args:
            items: List of item names/descriptions
        """
        if isinstance(items, str):
            self.treasure.append(items)
        else:
            self.treasure.extend(items)
            
    def add_trap(self, trap_type, dc, damage, save_type='reflex'):
        """
        Add a trap to this node.
        
        Args:
            trap_type: Description of the trap
            dc: Difficulty Class to avoid
            damage: Damage dice string (e.g., "2d6")
            save_type: Type of saving throw to avoid
        """
        self.traps.append({
            'type': trap_type,
            'dc': dc,
            'damage': damage,
            'save_type': save_type
        })
        
    def add_choice(self, choice_text, target_node_id, requirements=None):
        """
        Add a choice that leads to another node.
        
        Args:
            choice_text: Text displayed for this choice
            target_node_id: ID of the node this choice leads to
            requirements: Optional dict of requirements (e.g., {'item': 'key'})
        """
        self.choices.append({
            'text': choice_text,
            'target': target_node_id,
            'requirements': requirements or {}
        })
        
    def set_victory(self):
        """Mark this node as a victory condition"""
        self.is_victory = True
        
    def set_defeat(self):
        """Mark this node as a defeat condition"""
        self.is_defeat = True
        
    def add_on_enter_event(self, event_func):
        """
        Add a function to execute when entering this node.
        
        Args:
            event_func: Function that takes (character, node) and returns message
        """
        self.on_enter_events.append(event_func)
        
    def execute_on_enter(self, character):
        """Execute all on-enter events"""
        messages = []
        for event in self.on_enter_events:
            msg = event(character, self)
            if msg:
                messages.append(msg)
        return messages
        
    def check_requirements(self, character, choice_index):
        """
        Check if character meets requirements for a choice.
        
        Args:
            character: Player character
            choice_index: Index of the choice to check
            
        Returns:
            Tuple of (can_choose: bool, reason: str)
        """
        if choice_index >= len(self.choices):
            return False, "Invalid choice"
            
        choice = self.choices[choice_index]
        requirements = choice['requirements']
        
        # Check item requirements
        if 'item' in requirements:
            required_item = requirements['item']
            has_item = any(item.name == required_item for item in character.inventory)
            if not has_item:
                return False, f"Requires {required_item}"
                
        # Check ability score requirements
        for ability in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']:
            if ability in requirements:
                required_score = requirements[ability]
                actual_score = getattr(character, ability)
                if actual_score < required_score:
                    return False, f"Requires {ability.upper()} {required_score}+"
                    
        # Check level requirement
        if 'level' in requirements:
            if character.level < requirements['level']:
                return False, f"Requires level {requirements['level']}+"
                
        return True, ""
        
    def trigger_traps(self, character):
        """
        Trigger any traps at this node.
        
        Args:
            character: Player character
            
        Returns:
            List of trap result messages
        """
        messages = []
        
        for trap in self.traps:
            save_roll = character.saving_throw(trap['save_type'])
            
            if save_roll >= trap['dc']:
                messages.append(f"You avoid the {trap['type']}! (Save: {save_roll} vs DC {trap['dc']})")
            else:
                # Take damage from trap
                damage = self._roll_trap_damage(trap['damage'])
                character.take_damage(damage)
                messages.append(f"You trigger a {trap['type']}! (Save: {save_roll} vs DC {trap['dc']})")
                messages.append(f"You take {damage} damage! HP: {character.current_hp}/{character.max_hp}")
                
        return messages
        
    def _roll_trap_damage(self, damage_dice):
        """Roll trap damage"""
        if '+' in damage_dice:
            dice_part, mod = damage_dice.split('+')
            mod = int(mod)
        else:
            dice_part = damage_dice
            mod = 0
            
        count, sides = dice_part.split('d')
        count = int(count)
        sides = int(sides)
        
        return dice.roll(sides, count, mod)
        
    def has_combat(self):
        """Check if this node has combat encounters"""
        return len(self.monsters) > 0
        
    def create_combat(self, character):
        """
        Create a combat encounter from this node's monsters.
        
        Args:
            character: Player character
            
        Returns:
            Combat instance
        """
        monster_instances = [create_monster(m_type) for m_type in self.monsters]
        return Combat(character, monster_instances)
        
    def collect_treasure(self, character):
        """
        Collect all treasure at this node.
        
        Args:
            character: Player character
            
        Returns:
            List of treasure messages
        """
        messages = []
        
        for item in self.treasure:
            if 'gold' in item.lower():
                # Extract gold amount
                amount = int(''.join(filter(str.isdigit, item)))
                messages.append(f"You found {amount} gold pieces!")
            elif 'potion' in item.lower():
                character.add_item(HealingPotion())
                messages.append(f"You found a {item}!")
            else:
                messages.append(f"You found: {item}")
                
        # Clear treasure after collecting
        self.treasure = []
        
        return messages
        
    def get_display_text(self):
        """Get formatted display text for this node"""
        text = f"\n{'='*60}\n"
        text += f"{self.title}\n"
        text += f"{'='*60}\n\n"
        text += f"{self.description}\n"
        
        return text
        
    def get_choices_text(self):
        """Get formatted text for available choices"""
        if not self.choices:
            return "\n[No choices available - this is an ending]"
            
        text = "\nWhat do you do?\n"
        for i, choice in enumerate(self.choices):
            text += f"  [{i+1}] {choice['text']}\n"
            
        return text
        
    def __str__(self):
        return f"Node {self.node_id}: {self.title}"


class Adventure:
    """
    Container for a complete gamebook adventure.
    Manages all nodes and the flow between them.
    """
    
    def __init__(self, title, description, starting_node_id):
        """
        Initialize an adventure.
        
        Args:
            title: Adventure title
            description: Adventure description
            starting_node_id: ID of the first node
        """
        self.title = title
        self.description = description
        self.starting_node_id = starting_node_id
        self.nodes = {}  # Dictionary of node_id -> GameNode
        
    def add_node(self, node):
        """Add a node to the adventure"""
        self.nodes[node.node_id] = node
        
    def get_node(self, node_id):
        """Get a node by ID"""
        return self.nodes.get(node_id)
        
    def get_starting_node(self):
        """Get the starting node"""
        return self.nodes.get(self.starting_node_id)
        
    def __str__(self):
        return f"{self.title}: {len(self.nodes)} locations"
