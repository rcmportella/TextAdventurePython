"""
Character system following OGL D20 rules
"""
import dice


class Character:
    """
    Player character with D20 attributes and stats
    """
    
    def __init__(self, name, char_class="Fighter", level=1):
        self.name = name
        self.char_class = char_class
        self.level = level
        
        # Core ability scores (3-18 range typically)
        self.strength = 10
        self.dexterity = 10
        self.constitution = 10
        self.intelligence = 10
        self.wisdom = 10
        self.charisma = 10
        
        # Combat stats
        self.max_hp = 10
        self.current_hp = 10
        self.base_attack_bonus = 0
        self.armor_class = 10
        
        # Saving throws (Fortitude, Reflex, Will)
        self.fortitude_save = 0
        self.reflex_save = 0
        self.will_save = 0
        
        # Inventory and equipment
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        
        # Spells (for spellcasting classes)
        self.known_spells = []
        self.spell_slots = {}  # {level: available_slots}
        
        # Experience
        self.experience = 0
        
    def roll_abilities(self):
        """Roll ability scores using 4d6 drop lowest method"""
        self.strength = dice.ability_score()
        self.dexterity = dice.ability_score()
        self.constitution = dice.ability_score()
        self.intelligence = dice.ability_score()
        self.wisdom = dice.ability_score()
        self.charisma = dice.ability_score()
        self._update_derived_stats()
        
    def set_abilities(self, str_score, dex, con, int_score, wis, cha):
        """Set ability scores manually"""
        self.strength = str_score
        self.dexterity = dex
        self.constitution = con
        self.intelligence = int_score
        self.wisdom = wis
        self.charisma = cha
        self._update_derived_stats()
        
    def _update_derived_stats(self):
        """Update HP, AC, and other derived stats based on abilities"""
        con_mod = self.get_ability_modifier('constitution')
        
        # Update HP based on class and constitution
        if self.char_class == "Fighter":
            self.max_hp = 10 + con_mod + (self.level - 1) * (6 + con_mod)
            self.base_attack_bonus = self.level
            self.fortitude_save = 2 + (self.level // 2)
            self.reflex_save = 0 + (self.level // 3)
            self.will_save = 0 + (self.level // 3)
        elif self.char_class == "Wizard":
            self.max_hp = 4 + con_mod + (self.level - 1) * (3 + con_mod)
            self.base_attack_bonus = self.level // 2
            self.fortitude_save = 0 + (self.level // 3)
            self.reflex_save = 0 + (self.level // 3)
            self.will_save = 2 + (self.level // 2)
            self._setup_wizard_spells()
        elif self.char_class == "Rogue":
            self.max_hp = 6 + con_mod + (self.level - 1) * (4 + con_mod)
            self.base_attack_bonus = (self.level * 3) // 4
            self.fortitude_save = 0 + (self.level // 3)
            self.reflex_save = 2 + (self.level // 2)
            self.will_save = 0 + (self.level // 3)
        elif self.char_class == "Cleric":
            self.max_hp = 8 + con_mod + (self.level - 1) * (5 + con_mod)
            self.base_attack_bonus = (self.level * 3) // 4
            self.fortitude_save = 2 + (self.level // 2)
            self.reflex_save = 0 + (self.level // 3)
            self.will_save = 2 + (self.level // 2)
            self._setup_cleric_spells()
        
        # Ensure HP is at least 1 per level
        self.max_hp = max(self.max_hp, self.level)
        self.current_hp = self.max_hp
        
        # Base AC is 10 + Dex modifier
        dex_mod = self.get_ability_modifier('dexterity')
        self.armor_class = 10 + dex_mod
        
    def _setup_wizard_spells(self):
        """Setup spell slots for wizard"""
        # Simplified spell slots per level
        slots_per_level = {
            1: {0: 3, 1: 1},
            2: {0: 3, 1: 2},
            3: {0: 3, 1: 2, 2: 1},
            4: {0: 4, 1: 3, 2: 2},
            5: {0: 4, 1: 3, 2: 2, 3: 1}
        }
        self.spell_slots = slots_per_level.get(self.level, {0: 3, 1: 1})
        
    def _setup_cleric_spells(self):
        """Setup spell slots for cleric"""
        # Simplified spell slots per level
        slots_per_level = {
            1: {0: 3, 1: 1},
            2: {0: 4, 1: 2},
            3: {0: 4, 1: 2, 2: 1},
            4: {0: 5, 1: 3, 2: 2},
            5: {0: 5, 1: 3, 2: 2, 3: 1}
        }
        self.spell_slots = slots_per_level.get(self.level, {0: 3, 1: 1})
        
    def get_ability_modifier(self, ability):
        """Get the modifier for an ability score"""
        score = getattr(self, ability.lower())
        return dice.modifier(score)
        
    def attack_roll(self, target_ac, weapon_damage="1d8"):
        """
        Make an attack roll against a target.
        
        Args:
            target_ac: Target's Armor Class
            weapon_damage: Damage dice (e.g., "1d8", "2d6")
            
        Returns:
            Tuple of (hit: bool, damage: int)
        """
        # Attack roll: d20 + BAB + STR modifier (for melee)
        str_mod = self.get_ability_modifier('strength')
        attack_roll = dice.d20(1, self.base_attack_bonus + str_mod)
        
        if attack_roll >= target_ac:
            # Hit! Roll damage
            damage = self._roll_damage(weapon_damage) + str_mod
            return True, max(1, damage)
        else:
            return False, 0
            
    def _roll_damage(self, damage_dice):
        """Parse and roll damage dice string (e.g., '2d6', '1d8+2')"""
        if '+' in damage_dice:
            dice_part, mod = damage_dice.split('+')
            mod = int(mod)
        elif '-' in damage_dice:
            dice_part, mod = damage_dice.split('-')
            mod = -int(mod)
        else:
            dice_part = damage_dice
            mod = 0
            
        # Parse dice notation
        count, sides = dice_part.split('d')
        count = int(count)
        sides = int(sides)
        
        return dice.roll(sides, count, mod)
        
    def take_damage(self, damage):
        """Take damage and return True if still alive"""
        self.current_hp -= damage
        return self.current_hp > 0
        
    def heal(self, amount):
        """Heal damage, capped at max HP"""
        self.current_hp = min(self.current_hp + amount, self.max_hp)
        
    def is_alive(self):
        """Check if character is still alive"""
        return self.current_hp > 0
        
    def saving_throw(self, save_type):
        """
        Make a saving throw.
        
        Args:
            save_type: 'fortitude', 'reflex', or 'will'
            
        Returns:
            Roll result
        """
        if save_type == 'fortitude':
            return dice.d20(1, self.fortitude_save)
        elif save_type == 'reflex':
            return dice.d20(1, self.reflex_save)
        elif save_type == 'will':
            return dice.d20(1, self.will_save)
        else:
            return dice.d20()
            
    def add_item(self, item):
        """Add item to inventory"""
        self.inventory.append(item)
        
    def use_item(self, item_name):
        """Use an item from inventory"""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                effect = item.use(self)
                if item.consumable:
                    self.inventory.remove(item)
                return effect
        return None
        
    def learn_spell(self, spell):
        """Learn a new spell"""
        if spell not in self.known_spells:
            self.known_spells.append(spell)
            
    def can_cast_spell(self, spell):
        """Check if character can cast a spell"""
        if spell not in self.known_spells:
            return False
        spell_level = spell.level
        return self.spell_slots.get(spell_level, 0) > 0
        
    def cast_spell(self, spell, target=None):
        """Cast a spell"""
        if not self.can_cast_spell(spell):
            return False, "Cannot cast spell"
            
        # Use spell slot
        self.spell_slots[spell.level] -= 1
        
        # Execute spell effect
        result = spell.cast(self, target)
        return True, result
        
    def rest(self):
        """Rest to restore HP and spell slots"""
        self.current_hp = self.max_hp
        self._update_derived_stats()  # Restore spell slots
        
    def gain_experience(self, xp):
        """Gain experience points"""
        self.experience += xp
        # Simple level up at 1000 XP per level
        while self.experience >= self.level * 1000:
            self.level_up()
            
    def level_up(self):
        """Level up the character"""
        self.level += 1
        self._update_derived_stats()
        
    def __str__(self):
        return (f"{self.name} - Level {self.level} {self.char_class}\n"
                f"HP: {self.current_hp}/{self.max_hp} | AC: {self.armor_class}\n"
                f"STR: {self.strength} DEX: {self.dexterity} CON: {self.constitution}\n"
                f"INT: {self.intelligence} WIS: {self.wisdom} CHA: {self.charisma}")
