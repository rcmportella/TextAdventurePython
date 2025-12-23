"""
Adventure Loader - Load adventures from JSON files
"""
import json
from node import Adventure, GameNode


class AdventureLoader:
    """Load adventures from JSON format"""
    
    @staticmethod
    def load_from_file(filepath):
        """
        Load an adventure from a JSON file.
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            Adventure instance
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return AdventureLoader.load_from_dict(data)
    
    @staticmethod
    def load_from_dict(data):
        """
        Load an adventure from a dictionary (parsed JSON).
        
        Args:
            data: Dictionary containing adventure data
            
        Returns:
            Adventure instance
        """
        # Create adventure
        adventure = Adventure(
            title=data['title'],
            description=data['description'],
            starting_node_id=data['starting_node_id']
        )
        
        # Load custom monsters if present
        if 'custom_monsters' in data:
            for monster_name, monster_stats in data['custom_monsters'].items():
                adventure.add_custom_monster(monster_name, monster_stats)
        
        # Add all nodes
        for node_data in data['nodes']:
            node = AdventureLoader._create_node(node_data)
            adventure.add_node(node)
        
        return adventure
    
    @staticmethod
    def _create_node(node_data):
        """
        Create a GameNode from node data dictionary.
        
        Args:
            node_data: Dictionary containing node data
            
        Returns:
            GameNode instance
        """
        node = GameNode(
            node_id=node_data['node_id'],
            title=node_data['title'],
            description=node_data['description']
        )
        
        # Add monsters
        if 'monsters' in node_data:
            node.add_monster_encounter(node_data['monsters'])
        
        # Add treasure
        if 'treasure' in node_data:
            node.add_treasure(node_data['treasure'])
        
        # Add traps
        if 'traps' in node_data:
            for trap_data in node_data['traps']:
                node.add_trap(
                    trap_type=trap_data['type'],
                    dc=trap_data['dc'],
                    damage=trap_data['damage'],
                    save_type=trap_data.get('save_type', 'reflex')
                )
        
        # Add choices
        if 'choices' in node_data:
            for choice_data in node_data['choices']:
                node.add_choice(
                    choice_text=choice_data['text'],
                    target_node_id=choice_data['target'],
                    requirements=choice_data.get('requirements')
                )
        
        # Set victory/defeat flags
        if node_data.get('is_victory', False):
            node.set_victory()
        if node_data.get('is_defeat', False):
            node.set_defeat()
        
        # Add on_enter events for gold cost
        if 'gold_cost' in node_data:
            node.set_gold_cost(node_data['gold_cost'])
        
        # Add on_enter events for item costs
        if 'item_cost' in node_data:
            for item_name, quantity in node_data['item_cost'].items():
                node.set_item_cost(item_name, quantity)
        
        return node


class AdventureExporter:
    """Export adventures to JSON format"""
    
    @staticmethod
    def export_to_file(adventure, filepath):
        """
        Export an adventure to a JSON file.
        
        Args:
            adventure: Adventure instance to export
            filepath: Path where to save the JSON file
        """
        data = AdventureExporter.adventure_to_dict(adventure)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def adventure_to_dict(adventure):
        """
        Convert an adventure to a dictionary.
        
        Args:
            adventure: Adventure instance
            
        Returns:
            Dictionary representation
        """
        result = {
            'title': adventure.title,
            'description': adventure.description,
            'starting_node_id': adventure.starting_node_id,
            'nodes': [AdventureExporter._node_to_dict(node) 
                     for node in adventure.nodes.values()]
        }
        
        # Add custom monsters if present
        if adventure.custom_monsters:
            result['custom_monsters'] = adventure.custom_monsters
        
        return result
    
    @staticmethod
    def _node_to_dict(node):
        """
        Convert a GameNode to a dictionary.
        
        Args:
            node: GameNode instance
            
        Returns:
            Dictionary representation
        """
        node_dict = {
            'node_id': node.node_id,
            'title': node.title,
            'description': node.description
        }
        
        if node.monsters:
            node_dict['monsters'] = node.monsters
        
        if node.treasure:
            node_dict['treasure'] = node.treasure
        
        if node.traps:
            node_dict['traps'] = [
                {
                    'type': trap['type'],
                    'dc': trap['dc'],
                    'damage': trap['damage'],
                    'save_type': trap['save_type']
                }
                for trap in node.traps
            ]
        
        if node.choices:
            node_dict['choices'] = [
                {
                    'text': choice['text'],
                    'target': choice['target'],
                    'requirements': choice['requirements']
                }
                if choice['requirements'] else {
                    'text': choice['text'],
                    'target': choice['target']
                }
                for choice in node.choices
            ]
        
        if node.is_victory:
            node_dict['is_victory'] = True
        
        if node.is_defeat:
            node_dict['is_defeat'] = True
        
        if node.gold_cost > 0:
            node_dict['gold_cost'] = node.gold_cost
        
        if node.item_cost:
            node_dict['item_cost'] = node.item_cost
        
        return node_dict
