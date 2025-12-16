"""
Sample adventure demonstrating the gamebook framework
"""
from node import Adventure, GameNode


def create_sample_adventure():
    """
    Create a sample adventure: "The Dark Tower"
    
    Returns:
        Adventure instance
    """
    adventure = Adventure(
        title="The Dark Tower",
        description="A mysterious tower has appeared on the outskirts of town. Strange creatures have been seen emerging from it at night. You have been hired to investigate and stop whatever evil lurks within.",
        starting_node_id="start"
    )
    
    # === NODE 1: Starting point ===
    start = GameNode(
        node_id="start",
        title="The Tower Entrance",
        description="""You stand before a tall, ominous tower built of black stone. 
The entrance is a massive wooden door, slightly ajar. Strange sounds echo from within.
A worn path leads around the side of the tower, and you notice a small window high up on the wall."""
    )
    start.add_choice("Enter through the main door", "main_hall")
    start.add_choice("Investigate the side path", "side_path")
    start.add_choice("Try to climb to the window", "window_climb", requirements={'dexterity': 14})
    adventure.add_node(start)
    
    # === NODE 2: Main Hall ===
    main_hall = GameNode(
        node_id="main_hall",
        title="The Main Hall",
        description="""You push open the heavy door and step into a vast hall. Torches flicker on the walls,
casting dancing shadows. At the far end, a grand staircase leads upward. You hear the shuffling
of feet and see two goblins turning to face you with crude weapons drawn!"""
    )
    main_hall.add_monster_encounter(['goblin', 'goblin'])
    main_hall.add_choice("Ascend the stairs", "upper_chamber")
    main_hall.add_choice("Search the hall for secrets", "secret_room")
    adventure.add_node(main_hall)
    
    # === NODE 3: Side Path ===
    side_path = GameNode(
        node_id="side_path",
        title="The Side Path",
        description="""You follow a narrow path around the tower. Overgrown with weeds and brambles,
it seems rarely used. You discover a small cellar entrance, partially hidden by vegetation.
The door is old and rusty but appears unlocked."""
    )
    side_path.add_treasure(["Potion of Healing", "25 gold pieces"])
    side_path.add_choice("Enter the cellar", "cellar")
    side_path.add_choice("Return to the main entrance", "start")
    adventure.add_node(side_path)
    
    # === NODE 4: Window Climb ===
    window_climb = GameNode(
        node_id="window_climb",
        title="The Tower Window",
        description="""With agility and skill, you scale the tower wall and slip through the window.
You find yourself in a small study. Ancient books line the shelves, and a desk holds various
arcane instruments. This appears to be a wizard's workshop. You notice a journal on the desk
and a trapdoor in the floor."""
    )
    window_climb.add_treasure(["Spell scroll: Magic Missile", "Wizard's journal"])
    window_climb.add_choice("Read the journal", "read_journal")
    window_climb.add_choice("Open the trapdoor", "main_hall")
    window_climb.add_choice("Continue through the door", "upper_chamber")
    adventure.add_node(window_climb)
    
    # === NODE 5: Read Journal ===
    read_journal = GameNode(
        node_id="read_journal",
        title="The Wizard's Secret",
        description="""You read the journal and learn that a wizard named Malachar once lived here.
He attempted to summon a demon but lost control. The demon now commands the tower and its
creatures. The journal mentions that the demon can only be defeated by destroying its binding
crystal, located in the tower's highest chamber. You also find a note about a secret passage."""
    )
    read_journal.add_choice("Look for the secret passage", "secret_passage")
    read_journal.add_choice("Continue exploring", "upper_chamber")
    adventure.add_node(read_journal)
    
    # === NODE 6: Cellar ===
    cellar = GameNode(
        node_id="cellar",
        title="The Dark Cellar",
        description="""The cellar is damp and cold. Crates and barrels are stacked haphazardly.
You hear a skittering sound and see several giant spiders crawling down from their webs!"""
    )
    cellar.add_monster_encounter(['giant_spider', 'giant_spider'])
    cellar.add_treasure(["50 gold pieces", "Potion of Healing"])
    cellar.add_choice("Climb the stairs to the main tower", "main_hall")
    adventure.add_node(cellar)
    
    # === NODE 7: Secret Room ===
    secret_room = GameNode(
        node_id="secret_room",
        title="Hidden Chamber",
        description="""You discover a hidden door behind a tapestry! Inside is a small armory
with various weapons and a suit of armor. Among the treasures, you also find a healing potion."""
    )
    secret_room.add_treasure(["Longsword +1", "Chain Mail", "2x Potion of Healing", "30 gold pieces"])
    secret_room.add_choice("Continue up the stairs", "upper_chamber")
    secret_room.add_choice("Return to the hall", "main_hall")
    adventure.add_node(secret_room)
    
    # === NODE 8: Upper Chamber ===
    upper_chamber = GameNode(
        node_id="upper_chamber",
        title="The Upper Chamber",
        description="""You ascend the stairs to a circular chamber. The walls are covered in arcane
symbols that glow with an eerie light. In the center of the room, an orc warrior stands guard,
wielding a massive battle axe. Beyond him, another staircase leads even higher."""
    )
    upper_chamber.add_monster_encounter('orc')
    upper_chamber.add_choice("Continue upward", "trap_corridor")
    upper_chamber.add_choice("Search the chamber", "search_upper")
    adventure.add_node(upper_chamber)
    
    # === NODE 9: Search Upper Chamber ===
    search_upper = GameNode(
        node_id="search_upper",
        title="Arcane Discoveries",
        description="""You examine the arcane symbols and discover they form a protective ward.
With some study, you understand that dispelling it would weaken the demon above. You also
find a hidden alcove containing treasure."""
    )
    search_upper.add_treasure(["Spell scroll: Fireball", "Magic amulet", "40 gold pieces"])
    
    def dispel_ward(character, node):
        """Event: Dispel the protective ward"""
        return "You dispel the protective ward! The demon's power is weakened."
    
    search_upper.add_on_enter_event(dispel_ward)
    search_upper.add_choice("Continue to the top of the tower", "trap_corridor")
    adventure.add_node(search_upper)
    
    # === NODE 10: Trap Corridor ===
    trap_corridor = GameNode(
        node_id="trap_corridor",
        title="The Trapped Corridor",
        description="""You enter a long corridor leading to the tower's peak. The floor is made of
stone tiles, and you notice some appear slightly different from others. This looks like a trapped
hallway!"""
    )
    trap_corridor.add_trap("poison dart trap", 15, "2d4", "reflex")
    trap_corridor.add_choice("Proceed to the summit", "demon_chamber")
    adventure.add_node(trap_corridor)
    
    # === NODE 11: Secret Passage ===
    secret_passage = GameNode(
        node_id="secret_passage",
        title="Hidden Passage",
        description="""You find a secret passage behind a bookshelf! It leads through the tower walls,
bypassing the trapped corridor entirely. You emerge near the summit chamber."""
    )
    secret_passage.add_treasure(["Ancient spellbook", "Potion of Healing"])
    secret_passage.add_choice("Enter the demon's chamber", "demon_chamber")
    adventure.add_node(secret_passage)
    
    # === NODE 12: Demon Chamber (Boss Fight) ===
    demon_chamber = GameNode(
        node_id="demon_chamber",
        title="The Demon's Lair",
        description="""You enter the highest chamber of the tower. A massive pentagram is drawn on the
floor in what appears to be blood. In the center stands a terrible demon, its eyes burning with
hellfire. A glowing crystal hovers above an altar - the binding crystal! The demon roars and
attacks!"""
    )
    demon_chamber.add_monster_encounter('ogre')  # Using ogre as demon stand-in
    demon_chamber.add_choice("Destroy the binding crystal", "victory")
    demon_chamber.add_choice("Flee the tower", "defeat_fled")
    adventure.add_node(demon_chamber)
    
    # === NODE 13: Victory ===
    victory = GameNode(
        node_id="victory",
        title="Victory!",
        description="""With the demon defeated, you approach the binding crystal. You raise your weapon
and strike it with all your might. The crystal shatters into a thousand pieces, and the demon
lets out a final scream before dissolving into smoke. The tower begins to crumble around you,
but you manage to escape just in time.

The townsfolk celebrate your heroism, and you are rewarded handsomely. The threat has been
vanquished, and peace returns to the land!

*** YOU WIN! ***"""
    )
    victory.set_victory()
    adventure.add_node(victory)
    
    # === NODE 14: Defeat by Fleeing ===
    defeat_fled = GameNode(
        node_id="defeat_fled",
        title="Defeat",
        description="""You flee from the demon's chamber, running down the tower stairs as fast as you can.
The demon's laughter echoes behind you. You escape the tower with your life, but the demon
remains, and the threat continues to grow.

You have failed in your quest.

*** GAME OVER ***"""
    )
    defeat_fled.set_defeat()
    adventure.add_node(defeat_fled)
    
    return adventure


def create_simple_adventure():
    """
    Create a simpler, shorter adventure for testing: "The Goblin Cave"
    
    Returns:
        Adventure instance
    """
    adventure = Adventure(
        title="The Goblin Cave",
        description="A group of goblins has been raiding nearby farms. Track them to their cave and stop them!",
        starting_node_id="cave_entrance"
    )
    
    # Node 1: Cave Entrance
    entrance = GameNode(
        node_id="cave_entrance",
        title="Cave Entrance",
        description="You arrive at the mouth of a dark cave. You can hear goblin voices echoing from within."
    )
    entrance.add_choice("Enter the cave", "goblin_room")
    entrance.add_choice("Leave and return to town", "retreat")
    adventure.add_node(entrance)
    
    # Node 2: Goblin Room
    goblin_room = GameNode(
        node_id="goblin_room",
        title="Goblin Den",
        description="Three goblins are sitting around a fire, roasting something unpleasant. They spot you and attack!"
    )
    goblin_room.add_monster_encounter(['goblin', 'goblin', 'goblin'])
    goblin_room.add_treasure(["40 gold pieces", "Potion of Healing"])
    goblin_room.add_choice("Continue deeper into the cave", "boss_room")
    goblin_room.add_choice("Leave the cave victorious", "victory")
    adventure.add_node(goblin_room)
    
    # Node 3: Boss Room
    boss_room = GameNode(
        node_id="boss_room",
        title="Goblin Chief's Chamber",
        description="A large goblin chief sits on a throne made of stolen goods. He roars and charges at you!"
    )
    boss_room.add_monster_encounter('orc')  # Tougher enemy
    boss_room.add_treasure(["100 gold pieces", "Magic sword +1"])
    boss_room.add_choice("Return to town victorious", "victory")
    adventure.add_node(boss_room)
    
    # Node 4: Victory
    victory = GameNode(
        node_id="victory",
        title="Victory!",
        description="You have defeated the goblins! The farms are safe once again. Well done, hero!"
    )
    victory.set_victory()
    adventure.add_node(victory)
    
    # Node 5: Retreat
    retreat = GameNode(
        node_id="retreat",
        title="Retreat",
        description="You decide not to risk it and return to town. The goblin raids continue..."
    )
    retreat.set_defeat()
    adventure.add_node(retreat)
    
    return adventure
