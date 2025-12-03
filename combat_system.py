"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Yahzir Barron]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    enemy_type = enemy_type.lower()

    enemies = {
        "goblin": {
            "name": "Goblin",
            "health": 50,
            "max_health": 50,
            "strength": 8,
            "magic": 2,
            "xp_reward": 25,
            "gold_reward": 10
        },
        "orc": {
            "name": "Orc",
            "health": 80,
            "max_health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25
        },
        "dragon": {
            "name": "Dragon",
            "health": 200,
            "max_health": 200,
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100
        }
    }

    if enemy_type not in enemies:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")

    return enemies[enemy_type].copy()


def get_random_enemy_for_level(character_level):
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_count = 0

    def start_battle(self):
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character cannot start battle while dead.")

        display_battle_log("Battle begins!")

        while self.combat_active:
            display_combat_stats(self.character, self.enemy)

            # Player turn
            self.player_turn()
            winner = self.check_battle_end()
            if winner:
                break

            # Enemy turn
            self.enemy_turn()
            winner = self.check_battle_end()
            if winner:
                break

        # Determine results
        if winner == "player":
            rewards = get_victory_rewards(self.enemy)
            display_battle_log("You won the battle!")
            return {
                "winner": "player",
                "xp_gained": rewards["xp"],
                "gold_gained": rewards["gold"]
            }
        else:
            display_battle_log("You were defeated!")
            return {
                "winner": "enemy",
                "xp_gained": 0,
                "gold_gained": 0
            }

    def player_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError()

        print("\nYour turn:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Run")

        choice = input("Choose action: ").strip()

        if choice == "1":
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"You attack for {damage} damage!")
        elif choice == "2":
            result = use_special_ability(self.character, self.enemy)
            display_battle_log(result)
        elif choice == "3":
            if self.attempt_escape():
                display_battle_log("You successfully escaped!")
                return
            else:
                display_battle_log("Failed to escape!")
        else:
            display_battle_log("Invalid choice. You lose your turn.")

    def enemy_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError()

        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} attacks for {damage} damage!")

    def calculate_damage(self, attacker, defender):
        base = attacker["strength"] - (defender["strength"] // 4)
        return max(1, base)

    def apply_damage(self, target, damage):
        target["health"] = max(0, target["health"] - damage)

    def check_battle_end(self):
        if self.enemy["health"] <= 0:
            self.combat_active = False
            return "player"
        if self.character["health"] <= 0:
            self.combat_active = False
            return "enemy"
        return None

    def attempt_escape(self):
        success = random.random() < 0.5
        if success:
            self.combat_active = False
        return success


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    char_class = character["class"].lower()

    if char_class == "warrior":
        return warrior_power_strike(character, enemy)
    elif char_class == "mage":
        return mage_fireball(character, enemy)
    elif char_class == "rogue":
        return rogue_critical_strike(character, enemy)
    elif char_class == "cleric":
        return cleric_heal(character)
    else:
        return "No special ability available."

def warrior_power_strike(character, enemy):
    damage = character["strength"] * 2
    enemy["health"] = max(0, enemy["health"] - damage)
    return f"Warrior Power Strike! You deal {damage} damage."

def mage_fireball(character, enemy):
    damage = character["magic"] * 2
    enemy["health"] = max(0, enemy["health"] - damage)
    return f"Mage Fireball! {damage} damage scorches the enemy!"

def rogue_critical_strike(character, enemy):
    if random.random() < 0.5:
        damage = character["strength"] * 3
        enemy["health"] = max(0, enemy["health"] - damage)
        return f"Critical Hit! You deal {damage} massive damage!"
    else:
        return "Critical Strike failed! No damage dealt."

def cleric_heal(character):
    healed = 30
    before = character["health"]
    character["health"] = min(character["max_health"], character["health"] + healed)
    return f"Cleric Heal! Restored {character['health'] - before} HP."


# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    return character["health"] > 0

def get_victory_rewards(enemy):
    return {
        "xp": enemy["xp_reward"],
        "gold": enemy["gold_reward"]
    }

def display_combat_stats(character, enemy):
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")

def display_battle_log(message):
    print(f">>> {message}")
