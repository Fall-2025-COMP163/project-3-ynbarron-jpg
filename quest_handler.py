"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Yahzir Barron]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)


def accept_quest(character, quest_id, quest_data_dict):
    """Accept a new quest."""
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    quest = quest_data_dict[quest_id]

    # Level check
    if character['level'] < quest['required_level']:
        raise InsufficientLevelError("Character does not meet level requirement.")

    # Prerequisite check
    prereq = quest['prerequisite']
    if prereq != "NONE" and prereq not in character['completed_quests']:
        raise QuestRequirementsNotMetError("Prerequisite quest not completed.")

    # Already completed?
    if quest_id in character['completed_quests']:
        raise QuestAlreadyCompletedError("Quest already completed.")

    # Already active?
    if quest_id in character['active_quests']:
        raise QuestRequirementsNotMetError("Quest already active.")

    character['active_quests'].append(quest_id)
    return True


def complete_quest(character, quest_id, quest_data_dict):
    """Complete an active quest and grant rewards."""
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError("Quest not found.")

    if quest_id not in character['active_quests']:
        raise QuestNotActiveError("Quest is not currently active.")

    quest = quest_data_dict[quest_id]

    # Remove from active, add to completed
    character['active_quests'].remove(quest_id)
    character['completed_quests'].append(quest_id)

    # Grant rewards
    xp = quest['reward_xp']
    gold = quest['reward_gold']

    character['experience'] += xp
    character['gold'] += gold

    return {
        "quest_id": quest_id,
        "earned_xp": xp,
        "earned_gold": gold
    }


def abandon_quest(character, quest_id):
    """Remove a quest from active quests without completing it."""
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError("Quest is not active and cannot be abandoned.")

    character['active_quests'].remove(quest_id)
    return True


def get_active_quests(character, quest_data_dict):
    """Return list of full quest dictionaries for active quests."""
    active_list = []
    for q_id in character['active_quests']:
        if q_id in quest_data_dict:
            active_list.append(quest_data_dict[q_id])
    return active_list


def get_completed_quests(character, quest_data_dict):
    """Return list of full quest dictionaries for completed quests."""
    completed_list = []
    for q_id in character['completed_quests']:
        if q_id in quest_data_dict:
            completed_list.append(quest_data_dict[q_id])
    return completed_list


def get_available_quests(character, quest_data_dict):
    """Return quests the character can currently accept."""
    available = []
    for q_id, quest in quest_data_dict.items():
        if can_accept_quest(character, q_id, quest_data_dict):
            available.append(quest)
    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """Return True if quest completed."""
    return quest_id in character['completed_quests']


def is_quest_active(character, quest_id):
    """Return True if quest active."""
    return quest_id in character['active_quests']


def can_accept_quest(character, quest_id, quest_data_dict):
    """Check requirements for accepting a quest (no exceptions)."""
    if quest_id not in quest_data_dict:
        return False

    quest = quest_data_dict[quest_id]

    if quest_id in character['completed_quests']:
        return False

    if quest_id in character['active_quests']:
        return False

    # Level requirement
    if character['level'] < quest['required_level']:
        return False

    # Prerequisite
    prereq = quest['prerequisite']
    if prereq != "NONE" and prereq not in character['completed_quests']:
        return False

    return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """Return full chain of prerequisites leading to a quest."""
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    chain = []
    current = quest_id

    while True:
        if current not in quest_data_dict:
            raise QuestNotFoundError(f"Quest '{current}' not found.")

        chain.insert(0, current)
        prereq = quest_data_dict[current]['prerequisite']

        if prereq == "NONE":
            break

        current = prereq

    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """Return completion percentage from 0 to 100."""
    total = len(quest_data_dict)
    if total == 0:
        return 0.0

    completed = len(character['completed_quests'])
    percent = (completed / total) * 100
    return percent


def get_total_quest_rewards_earned(character, quest_data_dict):
    """Return total XP and gold earned from completed quests."""
    total_xp = 0
    total_gold = 0

    for q_id in character['completed_quests']:
        if q_id in quest_data_dict:
            quest = quest_data_dict[q_id]
            total_xp += quest['reward_xp']
            total_gold += quest['reward_gold']

    return {
        "total_xp": total_xp,
        "total_gold": total_gold
    }


def get_quests_by_level(quest_data_dict, min_level, max_level):
    """Return quests whose required_level is in [min_level, max_level]."""
    results = []
    for quest in quest_data_dict.values():
        lvl = quest['required_level']
        if min_level <= lvl <= max_level:
            results.append(quest)
    return results

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """Print detailed info about a quest."""
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Required Level: {quest_data['required_level']}")
    print(f"Prerequisite: {quest_data['prerequisite']}")
    print(f"Reward XP: {quest_data['reward_xp']}")
    print(f"Reward Gold: {quest_data['reward_gold']}\n")


def display_quest_list(quest_list):
    """Print summary of multiple quests."""
    for quest in quest_list:
        print(f"- {quest['title']} (Lvl {quest['required_level']}) | XP: {quest['reward_xp']} | Gold: {quest['reward_gold']}")


def display_character_quest_progress(character, quest_data_dict):
    """Show quest statistics for the character."""
    print("\n=== QUEST PROGRESS ===")
    active_count = len(character['active_quests'])
    completed_count = len(character['completed_quests'])
    percent = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion Percentage: {percent:.2f}%")
    print(f"Total XP Earned: {rewards['total_xp']}")
    print(f"Total Gold Earned: {rewards['total_gold']}\n")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """Ensure all prerequisites refer to real quests."""
    for q_id, quest in quest_data_dict.items():
        prereq = quest['prerequisite']
        if prereq != "NONE" and prereq not in quest_data_dict:
            raise QuestNotFoundError(f"Prerequisite '{prereq}' for quest '{q_id}' not found.")
    return True
