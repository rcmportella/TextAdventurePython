"""
Example of using the framework programmatically
This shows how to create a simple custom adventure and run it without the interactive UI
"""
from character import Character
from node import Adventure, GameNode
from game import GameEngine
from combat import Combat


def create_mini_adventure():
    """Create a very simple 3-node adventure"""
    adventure = Adventure(
        title="The Lost Sword",
        description="Find the legendary sword!",
        starting_node_id="forest"
    )
    
    # Node 1: Forest
    forest = GameNode(
        node_id="forest",
        title="Dark Forest",
        description="You are in a dark forest. A path leads to an old shrine."
    )
    forest.add_treasure(["20 gold pieces"])
    forest.add_choice("Follow the path to the shrine", "shrine")
    adventure.add_node(forest)
    
    # Node 2: Shrine
    shrine = GameNode(
        node_id="shrine",
        title="Ancient Shrine",
        description="An ancient shrine with a guardian skeleton!"
    )
    shrine.add_monster_encounter('skeleton')
    shrine.add_choice("Take the sword", "victory")
    adventure.add_node(shrine)
    
    # Node 3: Victory
    victory = GameNode(
        node_id="victory",
        title="Success!",
        description="You have claimed the legendary sword! Victory is yours!"
    )
    victory.set_victory()
    adventure.add_node(victory)
    
    return adventure


def run_example():
    """Run a programmatic example"""
    print("="*60)
    print("FRAMEWORK EXAMPLE - Programmatic Adventure")
    print("="*60)
    
    # Create character
    print("\n1. Creating character...")
    hero = Character("Brave Hero", "Fighter", level=2)
    hero.set_abilities(16, 14, 15, 10, 12, 8)
    print(f"   Created: {hero.name} (Fighter Level {hero.level})")
    print(f"   HP: {hero.current_hp}, AC: {hero.armor_class}")
    
    # Create adventure
    print("\n2. Loading adventure...")
    adventure = create_mini_adventure()
    print(f"   Loaded: {adventure.title}")
    print(f"   Nodes: {len(adventure.nodes)}")
    
    # Create game engine
    print("\n3. Starting game engine...")
    game = GameEngine(adventure, hero)
    
    # Start game
    result = game.start_game()
    print(f"   Status: {result['status']}")
    
    # Display first node
    print("\n" + "="*60)
    print(game.current_node.get_display_text())
    print("="*60)
    
    # Collect treasure
    if result.get('treasure_messages'):
        for msg in result['treasure_messages']:
            print(f"   {msg}")
    
    # Make first choice
    print("\n4. Making choice: Go to shrine")
    result = game.handle_choice(0)
    
    print("\n" + "="*60)
    print(game.current_node.get_display_text())
    print("="*60)
    
    # Combat
    if result['has_combat']:
        print("\n5. Engaging in combat!")
        combat = game.start_combat()
        
        # Fight automatically for 3 rounds
        for round_num in range(1, 4):
            print(f"\n   Round {round_num}:")
            combat_result = combat.execute_round({'type': 'attack', 'weapon_damage': '1d8+3'})
            
            for log_msg in combat_result['log'][-3:]:  # Show last 3 messages
                print(f"     {log_msg}")
            
            if combat_result['status'] != 'ongoing':
                print(f"   Combat ended: {combat_result['status']}")
                game.handle_combat_result(combat_result)
                break
    
    # Final choice
    print("\n6. Taking the sword...")
    result = game.handle_choice(0)
    
    if result['status'] == 'victory':
        print("\n" + "="*60)
        print("VICTORY!")
        print("="*60)
        print(game.current_node.description)
    
    print(f"\n7. Final character state:")
    print(f"   HP: {hero.current_hp}/{hero.max_hp}")
    print(f"   Level: {hero.level}")
    print(f"   XP: {hero.experience}")
    
    print("\n" + "="*60)
    print("Example completed!")
    print("="*60)


if __name__ == "__main__":
    run_example()
