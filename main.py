"""
Main entry point for the text adventure game
Run this file to start playing!
"""
from character import Character
from game import GameEngine, GameUI
from sample_adventure import create_sample_adventure, create_simple_adventure
from spell import get_spell


def create_character():
    """Interactive character creation"""
    print("\n" + "="*60)
    print("CHARACTER CREATION")
    print("="*60)
    
    name = input("\nEnter your character's name: ")
    
    print("\nChoose your class:")
    print("  1. Fighter - Strong warrior with high HP and combat skills")
    print("  2. Wizard - Spellcaster with powerful magic but lower HP")
    print("  3. Rogue - Agile and skilled, good at avoiding danger")
    print("  4. Cleric - Holy warrior with healing magic and combat ability")
    
    class_choice = input("\nEnter your choice (1-4): ")
    
    class_map = {
        '1': 'Fighter',
        '2': 'Wizard',
        '3': 'Rogue',
        '4': 'Cleric'
    }
    
    char_class = class_map.get(class_choice, 'Fighter')
    
    print("\nChoose ability score generation method:")
    print("  1. Standard (roll 4d6 drop lowest)")
    print("  2. Point buy (set scores manually)")
    
    method = input("\nEnter your choice (1-2): ")
    
    character = Character(name, char_class, level=1)
    
    if method == '1':
        character.roll_abilities()
        print("\nAbility scores rolled!")
    else:
        print("\nEnter ability scores (recommended: 15, 14, 13, 12, 10, 8):")
        str_score = int(input("Strength: "))
        dex = int(input("Dexterity: "))
        con = int(input("Constitution: "))
        int_score = int(input("Intelligence: "))
        wis = int(input("Wisdom: "))
        cha = int(input("Charisma: "))
        character.set_abilities(str_score, dex, con, int_score, wis, cha)
    
    # Give starting spells to spellcasters
    if char_class == 'Wizard':
        character.learn_spell(get_spell('magic_missile'))
        character.learn_spell(get_spell('ray_of_frost'))
        print("\nYou know the spells: Magic Missile, Ray of Frost")
    elif char_class == 'Cleric':
        character.learn_spell(get_spell('cure_light_wounds'))
        character.learn_spell(get_spell('bless'))
        print("\nYou know the spells: Cure Light Wounds, Bless")
    
    print("\n" + "="*60)
    print(character)
    print("="*60)
    
    return character


def play_adventure(game_engine):
    """Main game loop"""
    ui = GameUI()
    
    # Start the game
    result = game_engine.start_game()
    
    while not game_engine.game_over:
        # Display current node
        ui.display_node(game_engine.current_node)
        
        # Display any messages from processing the node
        if result.get('event_messages'):
            ui.display_messages(result['event_messages'])
        if result.get('trap_messages'):
            ui.display_messages(result['trap_messages'])
        if result.get('treasure_messages'):
            ui.display_messages(result['treasure_messages'])
        
        # Check if there's combat
        if result.get('has_combat'):
            print("\n" + "!"*60)
            print("COMBAT BEGINS!".center(60))
            print("!"*60)
            
            combat = game_engine.start_combat()
            combat_result = {'status': 'ongoing'}
            
            while combat_result['status'] == 'ongoing':
                ui.display_combat_status(combat)
                
                print("\nCombat Options:")
                print("  1. Attack")
                print("  2. Cast Spell (if available)")
                print("  3. Use Item")
                print("  4. Attempt to Flee")
                
                action = input("\nWhat do you do? ")
                
                if action == '1':
                    # Attack
                    combat_result = combat.execute_round({'type': 'attack', 'weapon_damage': '1d8'})
                    ui.display_messages(combat_result.get('log', []))
                    
                elif action == '2':
                    # Cast spell
                    if len(game_engine.character.known_spells) == 0:
                        print("You don't know any spells!")
                        continue
                        
                    print("\nKnown Spells:")
                    for i, spell in enumerate(game_engine.character.known_spells):
                        can_cast = game_engine.character.can_cast_spell(spell)
                        status = "✓" if can_cast else "✗"
                        print(f"  {i+1}. {status} {spell.name} (Level {spell.level})")
                    
                    spell_choice = input("\nChoose spell (0 to cancel): ")
                    if spell_choice != '0':
                        spell_idx = int(spell_choice) - 1
                        if 0 <= spell_idx < len(game_engine.character.known_spells):
                            spell = game_engine.character.known_spells[spell_idx]
                            combat_result = combat.execute_round({'type': 'spell', 'spell': spell})
                            ui.display_messages(combat_result.get('log', []))
                        
                elif action == '3':
                    # Use item
                    if not game_engine.character.inventory:
                        print("Your inventory is empty!")
                        continue
                    print("\nInventory:")
                    for i, item in enumerate(game_engine.character.inventory):
                        print(f"  {i+1}. {item.name}")
                    item_choice = input("\nChoose item (0 to cancel): ")
                    if item_choice != '0':
                        item_idx = int(item_choice) - 1
                        if 0 <= item_idx < len(game_engine.character.inventory):
                            item = game_engine.character.inventory[item_idx]
                            combat_result = combat.execute_round({'type': 'item', 'item_name': item.name})
                            ui.display_messages(combat_result.get('log', []))
                    
                elif action == '4':
                    # Flee
                    combat_result = combat.execute_round({'type': 'flee'})
                    ui.display_messages(combat_result.get('log', []))
            
            # Handle combat result
            result = game_engine.handle_combat_result(combat_result)
            
            if result.get('messages'):
                ui.display_messages(result['messages'])
            
            if result['status'] == 'game_over':
                game_engine.game_over = True
                print("\n" + result['message'])
                break
            
            print("\nPress Enter to continue...")
            input()
        
        # Display choices if game is still active
        if not game_engine.game_over:
            ui.display_choices(game_engine.current_node)
            
            # Additional commands
            print("\nOther commands: [S]tatus, [H]elp, [Q]uit")
            
            choice = input("\nYour choice: ").strip().lower()
            
            if choice == 's':
                ui.display_character(game_engine.character)
                print("\nPress Enter to continue...")
                input()
                continue
            elif choice == 'h':
                print("\n=== HELP ===")
                print("Enter the number of your choice to make a decision.")
                print("Combat: Choose actions during combat to defeat enemies.")
                print("Commands: S=Status, H=Help, Q=Quit")
                print("\nPress Enter to continue...")
                input()
                continue
            elif choice == 'q':
                confirm = input("Are you sure you want to quit? (y/n): ")
                if confirm.lower() == 'y':
                    print("Thanks for playing!")
                    return
                continue
            
            # Process normal choice
            try:
                choice_idx = int(choice) - 1
                result = game_engine.handle_choice(choice_idx)
                
                if result['status'] == 'error' or result['status'] == 'blocked':
                    print(f"\n{result['message']}")
                    print("Press Enter to continue...")
                    input()
                elif result['status'] == 'victory':
                    print("\n" + "="*60)
                    print("VICTORY!".center(60))
                    print("="*60)
                    print(f"\n{game_engine.current_node.description}")
                    game_engine.game_over = True
                elif result['status'] == 'defeat':
                    print("\n" + "="*60)
                    print("DEFEAT".center(60))
                    print("="*60)
                    print(f"\n{game_engine.current_node.description}")
                    game_engine.game_over = True
                    
            except (ValueError, IndexError):
                print("\nInvalid choice! Please enter a valid number.")
                print("Press Enter to continue...")
                input()
    
    print("\n" + "="*60)
    print("GAME OVER")
    print("="*60)
    print(f"\nFinal Status:")
    ui.display_character(game_engine.character)


def main():
    """Main function"""
    print("\n" + "="*60)
    print("TEXT ADVENTURE - D20 GAMEBOOK")
    print("="*60)
    print("\nWelcome to the Text Adventure Game!")
    print("This is a gamebook-style adventure using D20 rules.")
    print("\nPrepare yourself for combat, exploration, and decision-making!")
    
    # Choose adventure
    print("\n" + "="*60)
    print("CHOOSE YOUR ADVENTURE")
    print("="*60)
    print("\n1. The Dark Tower (Full adventure with multiple paths)")
    print("2. The Goblin Cave (Shorter, simpler adventure)")
    
    adv_choice = input("\nEnter your choice (1-2): ")
    
    if adv_choice == '2':
        adventure = create_simple_adventure()
    else:
        adventure = create_sample_adventure()
    
    # Create character
    character = create_character()
    
    # Create game engine
    game_engine = GameEngine(adventure, character)
    
    # Start playing
    print("\nPress Enter to begin your adventure...")
    input()
    
    play_adventure(game_engine)
    
    print("\nThank you for playing!")


if __name__ == "__main__":
    main()
