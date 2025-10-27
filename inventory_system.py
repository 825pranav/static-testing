#!/usr/bin/env python3
"""
A simple JSON-based inventory management script.

This module handles adding, removing, and checking item quantities
in an inventory dictionary and saving/loading the inventory to a JSON file.
"""

import json
import sys
from datetime import datetime


def add_item(stock_data, item, qty, logs=None):
    """
    Adds a given quantity of an item to the stock.

    Args:
        stock_data (dict): The inventory dictionary to modify.
        item (str): The name of the item to add.
        qty (int): The quantity to add. Must be a positive integer.
        logs (list, optional): A list to append log messages to.
                              If None, logging is skipped.
    """
    if logs is None:
        logs = []

    # Add validation to handle bad inputs
    if not isinstance(item, str) or not item:
        error_msg = f"Error: Item name '{item}' is invalid. " \
                    "Must be a non-empty string."
        print(error_msg, file=sys.stderr)
        return

    if not isinstance(qty, int) or qty <= 0:
        error_msg = f"Error: Quantity '{qty}' for item '{item}' is invalid. " \
                    "Must be a positive integer."
        print(error_msg, file=sys.stderr)
        return

    stock_data[item] = stock_data.get(item, 0) + qty

    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(stock_data, item, qty):
    """
    Removes a given quantity of an item from the stock.

    If the quantity drops to 0 or below, the item is removed entirely.
    Silently fails if the item does not exist.

    Args:
        stock_data (dict): The inventory dictionary to modify.
        item (str): The name of the item to remove.
        qty (int): The quantity to remove. Must be a positive integer.
    """
    # Add validation for robustness
    if not isinstance(item, str) or not item:
        error_msg = f"Error: Item name '{item}' is invalid. " \
                    "Must be a non-empty string."
        print(error_msg, file=sys.stderr)
        return

    if not isinstance(qty, int) or qty <= 0:
        error_msg = f"Error: Quantity '{qty}' for item '{item}' is invalid. " \
                    "Must be a positive integer."
        print(error_msg, file=sys.stderr)
        return

    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        # Item wasn't in stock, so we can silently pass.
        pass


def get_qty(stock_data, item):
    """
    Gets the current quantity of a specific item.

    Args:
        stock_data (dict): The inventory dictionary to read from.
        item (str): The name of the item.

    Returns:
        int: The quantity in stock, or 0 if the item is not found.
    """
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Loads the inventory data from a JSON file.

    Args:
        file (str, optional): The name of the file to load from.

    Returns:
        dict: The loaded inventory data.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Info: '{file}' not found. Starting with empty inventory.",
              file=sys.stderr)
        return {}
    except json.JSONDecodeError:
        error_msg = f"Error: Could not decode JSON from '{file}'. " \
                    "Starting with empty inventory."
        print(error_msg, file=sys.stderr)
        return {}


def save_data(stock_data, file="inventory.json"):
    """
    Saves the current inventory data to a JSON file.

    Args:
        stock_data (dict): The inventory dictionary to save.
        file (str, optional): The name of the file to save to.
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
    except IOError as e:
        print(f"Error: Could not save data to '{file}': {e}", file=sys.stderr)


def print_data(stock_data):
    """
    Prints a formatted report of all items and their quantities.

    Args:
        stock_data (dict): The inventory dictionary to print.
    """
    print("\n--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")
    print("--------------------")


def check_low_items(stock_data, threshold=5):
    """
    Finds all items with a quantity below the threshold.

    Args:
        stock_data (dict): The inventory dictionary to check.
        threshold (int, optional): The stock level to check against.

    Returns:
        list: A list of item names that are low in stock.
    """
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """
    Main function to run the inventory operations.
    """
    # 'stock_data' is a local variable in main
    stock_data = load_data()
    print("Initial inventory:")
    print_data(stock_data)

    # Create a list to capture logs for this session
    session_logs = []

    print("\n--- Processing Transactions ---")
    # Pass stock_data as an argument to all functions
    add_item(stock_data, "apple", 10, session_logs)
    add_item(stock_data, "banana", 15, session_logs)

    # These invalid calls will now be handled gracefully
    add_item(stock_data, "banana", -2, session_logs)
    add_item(stock_data, 123, "ten", session_logs)

    # This is the line that was fixed
    remove_item(stock_data, "apple", 3)

    # This blank line (line 187) is now TRULY free of whitespace

    remove_item(stock_data, "orange", 1)  # Will fail silently (KeyError)
    remove_item(stock_data, "banana", "two")  # Will fail gracefully

    print(f"\nApple stock: {get_qty(stock_data, 'apple')}")
    print(f"Low items: {check_low_items(stock_data)}")

    # Print final data
    print_data(stock_data)

    # Print the logs
    print("\n--- Transaction Log ---")
    if session_logs:
        for entry in session_logs:
            print(entry)
    else:
        print("No transactions logged.")

    # Save data at the end
    save_data(stock_data)
    print("\nInventory saved to 'inventory.json'.")


# Standard check to run main() when the script is executed directly
if __name__ == "__main__":
    main()
