"""
Main game engine for text adventure with D20 mechanics
"""
from character import Character
from node import Adventure
from combat import Combat
import spell


class GameEngine:
    """
    Main game engine that manages the adventure flow.
    """
    
    def __init__(self, adventure, character):
        """
        Initialize the game engine.
        
        Args:
            adventure: Adventure instance
            character: Player Character instance
        """
        self.adventure = adventure
        self.character = character
        self.current_node = adventure.get_starting_node()
        self.game_over = False
        self.victory = False
        self.visited_nodes = set()
        self.game_log = []
        
    def start_game(self):
        """Start the game and return initial display"""
        self._log(f"\n{'='*60}")
        self._log(f"  {self.adventure.title}")
        self._log(f"{'='*60}")
        self._log(f"\n{self.adventure.description}\n")
        self._log(f"Character: {self.character.name} (Level {self.character.level} {self.character.char_class})")
        self._log(f"{'='*60}\n")
        
        return self.process_node()
        
    def process_node(self):
        """
        Process the current node and return status.
        
        Returns:
            Dictionary with node information and status
        """
        if self.current_node is None:
            return {
                'status': 'error',
                'message': 'Invalid node!',
                'game_over': True
            }
            
        # Mark as visited
        self.visited_nodes.add(self.current_node.node_id)
        
        # Check victory/defeat
        if self.current_node.is_victory:
            self.victory = True
            self.game_over = True
            return {
                'status': 'victory',
                'message': self.current_node.description,
                'game_over': True
            }
            
        if self.current_node.is_defeat:
            self.game_over = True
            return {
                'status': 'defeat',
                'message': self.current_node.description,
                'game_over': True
            }
            
        # Execute on-enter events
        event_messages = self.current_node.execute_on_enter(self.character)
        
        # Check for traps
        trap_messages = self.current_node.trigger_traps(self.character)
        
        # Check if character died from traps
        if not self.character.is_alive():
            self.game_over = True
            return {
                'status': 'defeat',
                'message': 'You have died!',
                'game_over': True,
                'trap_messages': trap_messages
            }
            
        # Collect treasure
        treasure_messages = self.current_node.collect_treasure(self.character)
        
        # Check for combat
        has_combat = self.current_node.has_combat()
        
        return {
            'status': 'active',
            'node': self.current_node,
            'has_combat': has_combat,
            'event_messages': event_messages,
            'trap_messages': trap_messages,
            'treasure_messages': treasure_messages,
            'game_over': False
        }
        
    def handle_choice(self, choice_index):
        """
        Handle player's choice and move to next node.
        
        Args:
            choice_index: Index of the chosen option (0-based)
            
        Returns:
            Dictionary with result information
        """
        if choice_index < 0 or choice_index >= len(self.current_node.choices):
            return {
                'status': 'error',
                'message': 'Invalid choice!'
            }
            
        # Check requirements
        can_choose, reason = self.current_node.check_requirements(self.character, choice_index)
        if not can_choose:
            return {
                'status': 'blocked',
                'message': f"Cannot choose this option: {reason}"
            }
            
        # Move to next node
        choice = self.current_node.choices[choice_index]
        next_node_id = choice['target']
        self.current_node = self.adventure.get_node(next_node_id)
        
        if self.current_node is None:
            return {
                'status': 'error',
                'message': f'Node {next_node_id} not found!'
            }
            
        # Process the new node
        return self.process_node()
        
    def start_combat(self):
        """
        Start combat encounter at current node.
        
        Returns:
            Combat instance
        """
        return self.current_node.create_combat(self.character, self.adventure)
        
    def handle_combat_result(self, combat_result):
        """
        Handle the result of combat.
        
        Args:
            combat_result: Dictionary from Combat.execute_round()
            
        Returns:
            Game status dictionary
        """
        if combat_result['status'] == 'victory':
            # Award rewards
            rewards = combat_result.get('rewards', {})
            
            messages = ['\n=== VICTORY! ===']
            
            if rewards.get('experience', 0) > 0:
                self.character.gain_experience(rewards['experience'])
                messages.append(f"Gained {rewards['experience']} XP!")
                
            if rewards.get('gold', 0) > 0:
                messages.append(f"Found {rewards['gold']} gold pieces!")
                
            for item in rewards.get('items', []):
                messages.append(f"Found: {item}")
                
            # Clear monsters from node
            self.current_node.monsters = []
            
            return {
                'status': 'combat_complete',
                'victory': True,
                'messages': messages
            }
            
        elif combat_result['status'] == 'defeat':
            self.game_over = True
            return {
                'status': 'game_over',
                'victory': False,
                'message': 'You have been defeated in combat!'
            }
            
        elif combat_result['status'] == 'fled':
            # Player fled - maybe go back to previous node or allow choice
            return {
                'status': 'fled',
                'message': combat_result['message']
            }
            
        else:
            # Combat ongoing
            return {
                'status': 'combat_ongoing',
                'combat_status': combat_result
            }
            
    def _log(self, message):
        """Add message to game log"""
        self.game_log.append(message)
        
    def get_character_status(self):
        """Get formatted character status"""
        return str(self.character)
        
    def save_game(self, filename="savegame.json"):
        """Save game state (basic implementation)"""
        import json
        
        save_data = {
            'character_name': self.character.name,
            'character_class': self.character.char_class,
            'level': self.character.level,
            'current_hp': self.character.current_hp,
            'max_hp': self.character.max_hp,
            'current_node': self.current_node.node_id,
            'visited_nodes': list(self.visited_nodes),
            'abilities': {
                'strength': self.character.strength,
                'dexterity': self.character.dexterity,
                'constitution': self.character.constitution,
                'intelligence': self.character.intelligence,
                'wisdom': self.character.wisdom,
                'charisma': self.character.charisma
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
            
        return f"Game saved to {filename}"
        
    def load_game(self, filename="savegame.json"):
        """Load game state (basic implementation)"""
        import json
        
        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)
                
            # Restore character
            self.character.name = save_data['character_name']
            self.character.char_class = save_data['character_class']
            self.character.level = save_data['level']
            self.character.current_hp = save_data['current_hp']
            self.character.max_hp = save_data['max_hp']
            
            # Restore abilities
            abilities = save_data['abilities']
            self.character.set_abilities(
                abilities['strength'],
                abilities['dexterity'],
                abilities['constitution'],
                abilities['intelligence'],
                abilities['wisdom'],
                abilities['charisma']
            )
            
            # Restore position
            self.current_node = self.adventure.get_node(save_data['current_node'])
            self.visited_nodes = set(save_data['visited_nodes'])
            
            return f"Game loaded from {filename}"
            
        except FileNotFoundError:
            return "Save file not found!"
        except Exception as e:
            return f"Error loading game: {e}"


class GameUI:
    """
    Simple text-based UI for the game.
    """
    
    @staticmethod
    def display_node(node):
        """Display a node's information"""
        print(node.get_display_text())
        
    @staticmethod
    def display_choices(node):
        """Display available choices"""
        print(node.get_choices_text())
        
    @staticmethod
    def display_character(character):
        """Display character information"""
        print("\n" + "="*60)
        print("CHARACTER STATUS")
        print("="*60)
        print(character.get_character_sheet())
        print("="*60 + "\n")
        
    @staticmethod
    def display_combat_status(combat):
        """Display combat status"""
        print(combat.get_combat_summary())
        
    @staticmethod
    def display_messages(messages):
        """Display a list of messages"""
        for msg in messages:
            print(msg)
            
    @staticmethod
    def get_input(prompt="Enter your choice: "):
        """Get input from player"""
        return input(prompt)
        
    @staticmethod
    def display_title(text):
        """Display a title"""
        print("\n" + "="*60)
        print(text.center(60))
        print("="*60 + "\n")
        
    @staticmethod
    def clear_screen():
        """Clear the screen (optional)"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
