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
    character_class = character_class.capitalize()
    base_stats = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15},
    }

    if character_class not in base_stats:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")

    stats = base_stats[character_class]

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
    os.makedirs(save_directory, exist_ok=True)

    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filename, "w") as f:
            f.write(f"NAME: {character['name']}\n")
            f.write(f"CLASS: {character['class']}\n")
            f.write(f"LEVEL: {character['level']}\n")
            f.write(f"HEALTH: {character['health']}\n")
            f.write(f"MAX_HEALTH: {character['max_health']}\n")
            f.write(f"STRENGTH: {character['strength']}\n")
            f.write(f"MAGIC: {character['magic']}\n")
            f.write(f"EXPERIENCE: {character['experience']}\n")
            f.write(f"GOLD: {character['gold']}\n")
            f.write(f"INVENTORY: {','.join(character['inventory'])}\n")
            f.write(f"ACTIVE_QUESTS: {','.join(character['active_quests'])}\n")
            f.write(f"COMPLETED_QUESTS: {','.join(character['completed_quests'])}\n")
        return True

    except IOError:
        raise


def load_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save file for {character_name}")

    try:
        with open(filename, "r") as f:
            data = f.readlines()
    except Exception:
        raise SaveFileCorruptedError("Error reading save file.")

    try:
        char = {}
        for line in data:
            key, value = line.strip().split(": ", 1)
            char[key] = value

        # Convert numeric fields
        char_data = {
            "name": char["NAME"],
            "class": char["CLASS"],
            "level": int(char["LEVEL"]),
            "health": int(char["HEALTH"]),
            "max_health": int(char["MAX_HEALTH"]),
            "strength": int(char["STRENGTH"]),
            "magic": int(char["MAGIC"]),
            "experience": int(char["EXPERIENCE"]),
            "gold": int(char["GOLD"]),
            "inventory": char["INVENTORY"].split(",") if char["INVENTORY"] else [],
            "active_quests": char["ACTIVE_QUESTS"].split(",") if char["ACTIVE_QUESTS"] else [],
            "completed_quests": char["COMPLETED_QUESTS"].split(",") if char["COMPLETED_QUESTS"] else []
        }

        validate_character_data(char_data)
        return char_data

    except Exception:
        raise InvalidSaveDataError("Save file format is invalid.")


def list_saved_characters(save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        return []

    files = os.listdir(save_directory)
    names = []

    for file in files:
        if file.endswith("_save.txt"):
            names.append(file.replace("_save.txt", ""))

    return names


def delete_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save file for {character_name}")

    os.remove(filename)
    return True


# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    if character["health"] <= 0:
        raise CharacterDeadError("Dead characters cannot gain XP.")

    character["experience"] += xp_amount

    # Check for multiple level-ups
    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1

        # Increase stats
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2

        # Restore full health
        character["health"] = character["max_health"]


def add_gold(character, amount):
    new_gold = character["gold"] + amount

    if new_gold < 0:
        raise ValueError("Gold cannot go negative.")

    character["gold"] = new_gold
    return character["gold"]


def heal_character(character, amount):
    before = character["health"]
    character["health"] = min(character["max_health"], character["health"] + amount)
    return character["health"] - before


def is_character_dead(character):
    return character["health"] <= 0


def revive_character(character):
    if character["health"] > 0:
        return False  # Not dead

    character["health"] = character["max_health"] // 2
    return True


# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    required = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for key in required:
        if key not in character:
            raise InvalidSaveDataError(f"Missing field: {key}")

    numeric_fields = ["level", "health", "max_health", "strength", "magic", "experience", "gold"]
    for field in numeric_fields:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f"{field} must be an integer.")

    list_fields = ["inventory", "active_quests", "completed_quests"]
    for field in list_fields:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(f"{field} must be a list.")

    return True