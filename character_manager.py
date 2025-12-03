"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

           
import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)


# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    """
    # 1. Define valid classes and check if input is valid
    valid_char_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
    if character_class not in valid_char_classes:
        raise InvalidCharacterClassError(f"{character_class} is not an available class.")

    # 2. Assign base stats depending on class
    base_stats = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5}, 
        "Mage":    {"health": 80,  "strength": 8,  "magic": 20},
        "Rogue":   {"health": 90,  "strength": 12, "magic": 10},
        "Cleric":  {"health": 100, "strength": 10, "magic": 15}
    }
    stats = base_stats[character_class]

    # 3. Return character dictionary with all starting stats
    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }


def save_character(character, save_directory="data/save_games"):
    """
    Save character to a text file
    """
    # 1. Ensure the save directory exists
    os.makedirs(save_directory, exist_ok=True)

    # 2. Build the full file path for this character
    filepath = os.path.join(save_directory, f"{character['name']}_save.txt")

    # 3. Write each key/value to the file, converting lists to comma-separated strings
    try:
        with open(filepath, "w") as f:
            for key, value in character.items():
                if isinstance(value, list):
                    value = ",".join(value)
                f.write(f"{key}:{value}\n")
        return True
    except Exception:
        return False  # Return False if file save failed


def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from a save file
    """
    # 1. Build file path and check if it exists
    filepath = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Save file not found for: {character_name}")

    character = {}

    # 2. Read file line by line and parse key/value pairs
    try:
        with open(filepath, "r") as f:
            for line in f:
                if ":" not in line:
                    continue  # Skip invalid lines
                key, value = line.strip().split(":", 1)
                key = key.strip()
                value = value.strip()

                # 3. Convert strings to proper types (lists or ints)
                if "," in value:
                    value = value.split(",")
                elif value.isdigit():
                    value = int(value)
                character[key] = value

    except Exception as e:
        raise InvalidSaveDataError(f"Save data format is invalid for {character_name}: {e}")

    return character


def list_saved_characters(save_directory="data/save_games"):
    """
    Return a list of saved character names
    """
    # 1. Return empty list if directory does not exist
    if not os.path.exists(save_directory):
        return []

    # 2. List all files in the directory
    files = os.listdir(save_directory)

    # 3. Filter for _save.txt files and remove the extension
    return [f.replace("_save.txt", "") for f in files if f.endswith("_save.txt")]


def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character save file
    """
    # 1. Build file path
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)

    # 2. Check if file exists
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Character {character_name} was not found.")

    # 3. Delete the file
    os.remove(filepath)
    return True


# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience and handle level ups
    """
    # 1. Check if character is dead
    if character["health"] == 0:
        raise CharacterDeadError("Character is dead, cannot gain experience.")

    # 2. Add experience points
    character["experience"] += xp_amount

    # 3. Level up while experience reaches required XP
    while character["experience"] >= character["level"] * 100:
        level_up_xp = character["level"] * 100
        character["experience"] -= level_up_xp
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]


def add_gold(character, amount):
    """
    Add or remove gold from character
    """
    # 1. Get current gold
    current_gold = character.get("gold", 0)

    # 2. Calculate new gold and check for negative
    total_gold = current_gold + amount
    if total_gold < 0:
        raise ValueError("Not enough gold!")

    # 3. Update character gold
    character["gold"] = total_gold
    return total_gold


def heal_character(character, amount):
    """
    Heal character without exceeding max_health
    """
    # 1. Cannot heal dead character
    if character["health"] <= 0:
        raise CharacterDeadError("Character is dead, cannot heal.")

    # 2. Calculate actual healed amount
    healed_amount = min(character["health"] + amount, character["max_health"]) - character["health"]

    # 3. Update character health
    character["health"] = min(character["health"] + amount, character["max_health"])
    return healed_amount


def is_character_dead(character):
    """
    Check if character is dead
    """
    # 1. Check health
    return character.get("health", 0) <= 0


def revive_character(character):
    """
    Revive dead character at 50% health
    """
    # 1. Only revive if dead
    if not is_character_dead(character):
        return False

    # 2. Set health to 50% of max_health
    character["health"] = character["max_health"] // 2

    # 3. Return success
    return True


# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Check character has all required fields and correct types
    """
    # 1. Required fields with types
    required_fields = {
        "name": str,
        "class": str,
        "level": int,
        "health": int,
        "max_health": int,
        "strength": int,
        "magic": int,
        "experience": int,
        "gold": int,
        "inventory": list,
        "active_quests": list,
        "completed_quests": list
    }

