"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Yahzir Barron

AI Usage:
ChatGPT assisted in filling in menu flow, game loop structure,
and safe exception handling. All logic has been reviewed and
verified by the student.

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

current_character = None      # dict
all_quests = {}               # dict
all_items = {}                # dict
game_running = False


# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """Display main menu and return player choice (1–3)."""
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    choice = input("Choose an option (1–3): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= 3:
        return int(choice)

    print("Invalid choice.")
    return main_menu()


# ============================================================================
# NEW GAME
# ============================================================================

def new_game():
    """Create a new character and enter the game loop."""
    global current_character

    print("\n=== NEW GAME ===")
    name = input("Enter your character name: ").strip()
    print("Classes: Warrior, Mage, Rogue, Cleric")
    char_class = input("Choose a class: ").strip()

    try:
        current_character = character_manager.create_character(name, char_class)
        print(f"\nCharacter '{name}' the {char_class} created!")
        game_loop()
    except InvalidCharacterClassError as e:
        print(f"ERROR: {e}")
        new_game()


# ============================================================================
# LOAD GAME
# ============================================================================

def load_game():
    """Load a saved character and enter the game loop."""
    global current_character

    print("\n=== LOAD GAME ===")
    saves = character_manager.list_saved_characters()

    if not saves:
        print("No saved games found.")
        return

    for i, filename in enumerate(saves, start=1):
        print(f"{i}. {filename}")

    choice = input("Choose a save file: ").strip()

    if not choice.isdigit() or not (1 <= int(choice) <= len(saves)):
        print("Invalid choice.")
        return

    try:
        selected = saves[int(choice) - 1]
        current_character = character_manager.load_character(selected)
        print(f"\nLoaded character '{current_character['name']}'!")
        game_loop()

    except (CharacterNotFoundError, SaveFileCorruptedError) as e:
        print(f"ERROR: {e}")


# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """Main game loop."""
    global game_running

    game_running = True
    print("\nEntering the world of Quest Chronicles...\n")

    while game_running:
        choice = game_menu()

        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Thanks for playing!")
            game_running = False

        # Auto-save after each action
        save_game()


# ============================================================================
# GAME MENU
# ============================================================================

def game_menu():
    """Display in-game menu and get player choice."""
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Battle)")
    print("5. Shop")
    print("6. Save & Quit")

    choice = input("Choose (1–6): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= 6:
        return int(choice)

    print("Invalid choice.")
    return game_menu()


# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character stats and quest progress."""
    global current_character, all_quests

    print("\n=== CHARACTER STATS ===")
    character_manager.display_character(current_character)

    print("\n=== QUEST PROGRESS ===")
    quest_handler.display_character_quest_progress(current_character, all_quests)


def view_inventory():
    """Show inventory and allow basic actions."""
    global current_character

    print("\n=== INVENTORY ===")
    inventory_system.display_inventory(current_character)

    print("\nOptions:")
    print("1. Use Item")
    print("2. Drop Item")
    print("3. Back")

    choice = input("Choose: ").strip()
    if choice == "1":
        item = input("Which item? ").strip()
        try:
            inventory_system.use_item(current_character, item)
        except InventoryError as e:
            print(f"ERROR: {e}")

    elif choice == "2":
        item = input("Drop which item? ").strip()
        try:
            inventory_system.remove_item(current_character, item)
        except InventoryError as e:
            print(f"ERROR: {e}")


def quest_menu():
    """Handle quest viewing, accepting, completing."""
    global current_character, all_quests

    print("\n=== QUEST MENU ===")
    print("1. Active Quests")
    print("2. Available Quests")
    print("3. Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest (Testing)")
    print("7. Back")

    choice = input("Choose: ").strip()

    if choice == "1":
        quests = quest_handler.get_active_quests(current_character, all_quests)
        quest_handler.display_quest_list(quests)

    elif choice == "2":
        quests = quest_handler.get_available_quests(current_character, all_quests)
        quest_handler.display_quest_list(quests)

    elif choice == "3":
        quests = quest_handler.get_completed_quests(current_character, all_quests)
        quest_handler.display_quest_list(quests)

    elif choice == "4":
        quest_id = input("Enter quest ID to accept: ").strip()
        try:
            quest_handler.accept_quest(current_character, quest_id, all_quests)
            print("Quest accepted!")
        except QuestError as e:
            print(f"ERROR: {e}")

    elif choice == "5":
        q = input("Quest ID to abandon: ").strip()
        try:
            quest_handler.abandon_quest(current_character, q)
            print("Quest abandoned.")
        except QuestNotActiveError as e:
            print(f"ERROR: {e}")

    elif choice == "6":
        q = input("Quest ID to complete: ").strip()
        try:
            rewards = quest_handler.complete_quest(current_character, q, all_quests)
            print("Quest completed:", rewards)
        except QuestError as e:
            print(f"ERROR: {e}")


def explore():
    """Trigger a random battle."""
    global current_character

    print("\n=== EXPLORING... ===")
    battle = combat_system.SimpleBattle(current_character)
    result = battle.start_battle()

    if result == "loss":
        handle_character_death()
    else:
        print("You won the battle!")


def shop():
    """Buy/sell items."""
    global current_character, all_items

    print("\n=== SHOP ===")
    print(f"You have {current_character['gold']} gold.")

    for item_id, info in all_items.items():
        print(f"- {item_id}: {info['price']} gold")

    choice = input("Buy which item (or 'back')? ").strip()
    if choice.lower() == "back":
        return

    if choice in all_items:
        price = all_items[choice]["price"]
        try:
            inventory_system.buy_item(current_character, choice, price)
            print(f"Bought {choice}!")
        except InventoryError as e:
            print(f"ERROR: {e}")
    else:
        print("Item not found.")


# ============================================================================
# HELPERS
# ============================================================================

def save_game():
    """Save current character state."""
    global current_character
    if current_character:
        try:
            character_manager.save_character(current_character)
        except Exception as e:
            print(f"ERROR saving game: {e}")


def load_game_data():
    """Load items and quests."""
    global all_items, all_quests

    all_quests = game_data.load_quest_data("data/quests.txt")
    all_items = game_data.load_item_data("data/items.txt")


def handle_character_death():
    """Handle death logic."""
    global game_running, current_character

    print("\n=== YOU DIED ===")
    if current_character["gold"] >= 20:
        choice = input("Revive for 20 gold? (y/n): ").strip().lower()
        if choice == "y":
            current_character["gold"] -= 20
            character_manager.revive_character(current_character)
            print("You have been revived!")
            return

    print("Game Over.")
    game_running = False


def display_welcome():
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("Welcome, hero!\n")


# ============================================================================
# MAIN ENTRY
# ============================================================================

def main():
    display_welcome()

    try:
        load_game_data()
        print("Game data loaded.\n")
    except Exception as e:
        print("ERROR loading data:", e)
        return

    while True:
        choice = main_menu()
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
