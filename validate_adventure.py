"""
Validation script for JSON adventures
Checks for common errors and structural issues
"""
import json
import sys
import os


def validate_adventure(filepath):
    """
    Validate a JSON adventure file.
    
    Args:
        filepath: Path to the JSON adventure file
        
    Returns:
        Tuple of (is_valid, errors, warnings)
    """
    errors = []
    warnings = []
    
    # Check file exists
    if not os.path.exists(filepath):
        errors.append(f"File not found: {filepath}")
        return False, errors, warnings
    
    # Try to load JSON
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {e}")
        return False, errors, warnings
    except Exception as e:
        errors.append(f"Error reading file: {e}")
        return False, errors, warnings
    
    # Check required adventure fields
    required_fields = ['title', 'description', 'starting_node_id', 'nodes']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    if 'nodes' not in data or not isinstance(data['nodes'], list):
        errors.append("'nodes' must be a list")
        return False, errors, warnings
    
    if len(data['nodes']) == 0:
        errors.append("Adventure must have at least one node")
        return False, errors, warnings
    
    # Collect all node IDs
    node_ids = set()
    for node in data['nodes']:
        if 'node_id' in node:
            node_ids.add(node['node_id'])
    
    # Check starting node exists
    if 'starting_node_id' in data:
        if data['starting_node_id'] not in node_ids:
            errors.append(f"starting_node_id '{data['starting_node_id']}' not found in nodes")
    
    # Validate each node
    has_victory = False
    has_defeat = False
    
    for i, node in enumerate(data['nodes']):
        node_num = i + 1
        
        # Check required node fields
        if 'node_id' not in node:
            errors.append(f"Node {node_num}: Missing 'node_id'")
            continue
            
        node_id = node['node_id']
        
        if 'title' not in node:
            errors.append(f"Node '{node_id}': Missing 'title'")
        if 'description' not in node:
            errors.append(f"Node '{node_id}': Missing 'description'")
        
        # Check if it's an ending node
        is_ending = node.get('is_victory', False) or node.get('is_defeat', False)
        
        if node.get('is_victory'):
            has_victory = True
        if node.get('is_defeat'):
            has_defeat = True
        
        # Check choices
        if 'choices' in node:
            if not isinstance(node['choices'], list):
                errors.append(f"Node '{node_id}': 'choices' must be a list")
            else:
                for j, choice in enumerate(node['choices']):
                    choice_num = j + 1
                    
                    if 'text' not in choice:
                        errors.append(f"Node '{node_id}', Choice {choice_num}: Missing 'text'")
                    if 'target' not in choice:
                        errors.append(f"Node '{node_id}', Choice {choice_num}: Missing 'target'")
                    elif choice['target'] not in node_ids:
                        errors.append(f"Node '{node_id}', Choice {choice_num}: Target '{choice['target']}' not found")
        elif not is_ending:
            warnings.append(f"Node '{node_id}': No choices (should be an ending node)")
        
        # Validate monsters
        if 'monsters' in node:
            valid_monsters = ['goblin', 'orc', 'skeleton', 'giant_spider', 'zombie', 'ogre', 'troll', 'dragon']
            custom_monsters = data.get('custom_monsters', {}).keys()
            monsters = node['monsters']
            if not isinstance(monsters, list):
                errors.append(f"Node '{node_id}': 'monsters' must be a list")
            else:
                for monster in monsters:
                    if monster not in valid_monsters and monster not in custom_monsters:
                        warnings.append(f"Node '{node_id}': Unknown monster type '{monster}' (not predefined or custom)")
        
        # Validate traps
        if 'traps' in node:
            if not isinstance(node['traps'], list):
                errors.append(f"Node '{node_id}': 'traps' must be a list")
            else:
                for k, trap in enumerate(node['traps']):
                    trap_num = k + 1
                    if 'type' not in trap:
                        errors.append(f"Node '{node_id}', Trap {trap_num}: Missing 'type'")
                    if 'dc' not in trap:
                        errors.append(f"Node '{node_id}', Trap {trap_num}: Missing 'dc'")
                    if 'damage' not in trap:
                        errors.append(f"Node '{node_id}', Trap {trap_num}: Missing 'damage'")
                    if 'save_type' in trap:
                        valid_saves = ['reflex', 'fortitude', 'will']
                        if trap['save_type'] not in valid_saves:
                            warnings.append(f"Node '{node_id}', Trap {trap_num}: Unknown save_type '{trap['save_type']}'")
    
    # Check for endings
    if not has_victory:
        warnings.append("No victory node found (set is_victory: true)")
    if not has_defeat:
        warnings.append("No defeat node found (set is_defeat: true)")
    
    # Check for unreachable nodes
    reachable = {data['starting_node_id']}
    to_check = [data['starting_node_id']]
    
    while to_check:
        current = to_check.pop()
        for node in data['nodes']:
            if node.get('node_id') == current:
                if 'choices' in node:
                    for choice in node['choices']:
                        target = choice.get('target')
                        if target and target not in reachable:
                            reachable.add(target)
                            to_check.append(target)
    
    unreachable = node_ids - reachable
    for node_id in unreachable:
        warnings.append(f"Node '{node_id}' is unreachable from starting node")
    
    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def print_validation_results(filepath, is_valid, errors, warnings):
    """Print validation results in a formatted way"""
    print("="*60)
    print(f"Validating: {filepath}")
    print("="*60)
    
    if errors:
        print("\n❌ ERRORS:")
        for error in errors:
            print(f"  • {error}")
    
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  • {warning}")
    
    if is_valid and not warnings:
        print("\n✓ Validation passed! No errors or warnings.")
    elif is_valid:
        print("\n✓ Validation passed with warnings.")
    else:
        print("\n✗ Validation failed. Please fix errors before using this adventure.")
    
    print("="*60)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python validate_adventure.py <path_to_json>")
        print("\nExample:")
        print("  python validate_adventure.py adventures/my_adventure.json")
        print("\nValidate all adventures:")
        print("  python validate_adventure.py adventures/*.json")
        return
    
    # Validate all provided files
    for filepath in sys.argv[1:]:
        is_valid, errors, warnings = validate_adventure(filepath)
        print_validation_results(filepath, is_valid, errors, warnings)
        print()


if __name__ == "__main__":
    main()
