"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Yahzir Barron]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest data file '{filename}' not found.")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        raise CorruptedDataError("Unable to read quest data file.")

    # Split file by blank lines into blocks
    raw_blocks = content.strip().split("\n\n")
    quest_dict = {}

    for block in raw_blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        try:
            quest_data = parse_quest_block(lines)
            validate_quest_data(quest_data)
            quest_id = quest_data["quest_id"]
            quest_dict[quest_id] = quest_data
        except InvalidDataFormatError:
            raise
        except Exception:
            raise CorruptedDataError("Corrupted quest block detected.")

    return quest_dict


def load_items(filename="data/items.txt"):
    """
    Load item data from file
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item data file '{filename}' not found.")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        raise CorruptedDataError("Unable to read item data file.")

    raw_blocks = content.strip().split("\n\n")
    item_dict = {}

    for block in raw_blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        try:
            item_data = parse_item_block(lines)
            validate_item_data(item_data)
            item_id = item_data["item_id"]
            item_dict[item_id] = item_data
        except InvalidDataFormatError:
            raise
        except Exception:
            raise CorruptedDataError("Corrupted item block detected.")

    return item_dict


# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_data(quest_dict):
    required = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold",
        "required_level", "prerequisite"
    ]

    for key in required:
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing field in quest: {key}")

    # type checks
    if not isinstance(quest_dict["reward_xp"], int):
        raise InvalidDataFormatError("reward_xp must be an integer")

    if not isinstance(quest_dict["reward_gold"], int):
        raise InvalidDataFormatError("reward_gold must be an integer")

    if not isinstance(quest_dict["required_level"], int):
        raise InvalidDataFormatError("required_level must be an integer")

    return True


def validate_item_data(item_dict):
    required = ["item_id", "name", "type", "effect", "cost", "description"]
    valid_types = ["weapon", "armor", "consumable"]

    for key in required:
        if key not in item_dict:
            raise InvalidDataFormatError(f"Missing field in item: {key}")

    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Item cost must be an integer")

    # effect must be in form "stat:value"
    if ":" not in item_dict["effect"]:
        raise InvalidDataFormatError("Invalid effect format")

    return True


# ============================================================================
# DEFAULT FILE CREATION
# ============================================================================

def create_default_data_files():
    """
    Creates the data folder and basic default quest/item files.
    Only used when files are missing.
    """
    if not os.path.exists("data"):
        os.makedirs("data")

    # default quests
    if not os.path.exists("data/quests.txt"):
        with open("data/quests.txt", "w", encoding="utf-8") as f:
            f.write(
                "QUEST_ID: intro_1\n"
                "TITLE: The Beginning\n"
                "DESCRIPTION: Your adventure starts here.\n"
                "REWARD_XP: 50\n"
                "REWARD_GOLD: 20\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n"
            )

    # default items
    if not os.path.exists("data/items.txt"):
        with open("data/items.txt", "w", encoding="utf-8") as f:
            f.write(
                "ITEM_ID: basic_sword\n"
                "NAME: Basic Sword\n"
                "TYPE: weapon\n"
                "EFFECT: strength:5\n"
                "COST: 100\n"
                "DESCRIPTION: A simple beginner sword.\n"
            )


# ============================================================================
# PARSING FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Converts:
      QUEST_ID: something
    into a dict
    """
    quest = {}
    try:
        for line in lines:
            if ": " not in line:
                raise InvalidDataFormatError(f"Bad line format: {line}")

            key, value = line.split(": ", 1)
            key = key.strip()
            value = value.strip()

            if key == "QUEST_ID":
                quest["quest_id"] = value
            elif key == "TITLE":
                quest["title"] = value
            elif key == "DESCRIPTION":
                quest["description"] = value
            elif key == "REWARD_XP":
                quest["reward_xp"] = int(value)
            elif key == "REWARD_GOLD":
                quest["reward_gold"] = int(value)
            elif key == "REQUIRED_LEVEL":
                quest["required_level"] = int(value)
            elif key == "PREREQUISITE":
                quest["prerequisite"] = value
            else:
                raise InvalidDataFormatError(f"Unknown quest field: {key}")

    except ValueError:
        raise InvalidDataFormatError("Invalid numeric value in quest data.")

    return quest


def parse_item_block(lines):
    """
    Converts item block to dictionary
    """
    item = {}
    try:
        for line in lines:
            if ": " not in line:
                raise InvalidDataFormatError(f"Bad line format: {line}")

            key, value = line.split(": ", 1)
            key = key.strip()
            value = value.strip()

            if key == "ITEM_ID":
                item["item_id"] = value
            elif key == "NAME":
                item["name"] = value
            elif key == "TYPE":
                item["type"] = value
            elif key == "EFFECT":
                item["effect"] = value
            elif key == "COST":
                item["cost"] = int(value)
            elif key == "DESCRIPTION":
                item["description"] = value
            else:
                raise InvalidDataFormatError(f"Unknown item field: {key}")

    except ValueError:
        raise InvalidDataFormatError("Invalid numeric value in item data.")

    return item
