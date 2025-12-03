"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    """
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full!")

    character['inventory'].append(item_id)
    return True


def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory")

    character['inventory'].remove(item_id)
    return True


def has_item(character, item_id):
    """Return True if character has the item"""
    return item_id in character['inventory']


def count_item(character, item_id):
    """Return number of times item appears"""
    return character['inventory'].count(item_id)


def get_inventory_space_remaining(character):
    """Return remaining item slots"""
    return MAX_INVENTORY_SIZE - len(character['inventory'])


def clear_inventory(character):
    """Clear all items and return list of removed items"""
    removed = character['inventory'][:]
    character['inventory'].clear()
    return removed

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError("Item not in inventory")

    if item_data['type'] != 'consumable':
        raise InvalidItemTypeError("Only consumables can be used")

    stat, value = parse_item_effect(item_data['effect'])
    apply_stat_effect(character, stat, value)
    remove_item_from_inventory(character, item_id)


    return f"{character['name']} used {item_id} and gained {stat} +{value}."


def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError("Weapon not in inventory")

    if item_data['type'] != 'weapon':
        raise InvalidItemTypeError("This item is not a weapon")

    # Unequip current weapon if exists
    if character.get('equipped_weapon') is not None:
        unequip_weapon(character)

    stat, value = parse_item_effect(item_data['effect'])
    apply_stat_effect(character, stat, value)

    character['inventory'].remove(item_id)
    character['equipped_weapon'] = item_id

    return f"{character['name']} equipped weapon: {item_id} (+{value} {stat})"


def equip_armor(character, item_id, item_data):
    """
    Equip armor
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError("Armor not in inventory")

    if item_data['type'] != 'armor':
        raise InvalidItemTypeError("This item is not armor")

    if character.get('equipped_armor') is not None:
        unequip_armor(character)

    stat, value = parse_item_effect(item_data['effect'])
    apply_stat_effect(character, stat, value)

    character['inventory'].remove(item_id)
    character['equipped_armor'] = item_id

    return f"Equipped armor: {item_data['name']} (+{value} {stat})"


def unequip_weapon(character):
    """
    Unequip weapon and return to inventory
    """
    weapon_id = character.get('equipped_weapon')
    if weapon_id is None:
        return None

    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("No space to unequip weapon")

    # Remove effect
    stat, value = parse_item_effect(character['item_data'][weapon_id]['effect'])
    apply_stat_effect(character, stat, -value)

    character['inventory'].append(weapon_id)
    character['equipped_weapon'] = None

    return weapon_id


def unequip_armor(character):
    """
    Unequip armor and return to inventory
    """
    armor_id = character.get('equipped_armor')
    if armor_id is None:
        return None

    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("No space to unequip armor")

    stat, value = parse_item_effect(character['item_data'][armor_id]['effect'])
    apply_stat_effect(character, stat, -value)

    character['inventory'].append(armor_id)
    character['equipped_armor'] = None

    return armor_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item
    """
    if character['gold'] < item_data['cost']:
        raise InsufficientResourcesError("Not enough gold")

    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full")

    character['gold'] -= item_data['cost']
    character['inventory'].append(item_id)
    return True


def sell_item(character, item_id, item_data):
    """
    Sell item for 50% cost
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError("Item not in inventory")

    sell_price = item_data['cost'] // 2

    character['inventory'].remove(item_id)
    character['gold'] += sell_price

    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Convert "stat:value" into ("stat", value)
    """
    stat, value = effect_string.split(":")
    return stat, int(value)


def apply_stat_effect(character, stat_name, value):
    """
    Apply stat changes safely
    """
    if stat_name not in character:
        return

    character[stat_name] += value

    # Health cannot exceed max_health
    if stat_name == "health":
        character['health'] = min(character['health'], character['max_health'])


def display_inventory(character, item_data_dict):
    """
    Pretty print inventory
    """
    if not character['inventory']:
        print("\nInventory is empty.\n")
        return

    counted = {}
    for item in character['inventory']:
        counted[item] = counted.get(item, 0) + 1

    print("\n=== INVENTORY ===")
    for item_id, amount in counted.items():
        data = item_data_dict[item_id]
        print(f"{data['name']} (x{amount}) - {data['type'].title()}")
    print("=================\n")
