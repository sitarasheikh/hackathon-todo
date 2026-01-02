import json
import os
from typing import Any, Dict
import re


def save_to_file(data: Any, filepath: str) -> bool:
    """
    Save data to a JSON file.

    Args:
        data: The data to save (should be JSON serializable)
        filepath: The path to the file to save to

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving to file {filepath}: {e}")
        return False


def load_from_file(filepath: str) -> Any:
    """
    Load data from a JSON file.

    Args:
        filepath: The path to the file to load from

    Returns:
        The loaded data, or None if an error occurs
    """
    try:
        if not os.path.exists(filepath):
            # Return empty list if file doesn't exist
            return []

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {filepath}: {e}")
        return None
    except Exception as e:
        print(f"Error loading from file {filepath}: {e}")
        return None


def validate_todo_id(todo_id: str) -> bool:
    """
    Validate if the provided string is a valid todo ID (positive integer).

    Args:
        todo_id: String representation of the ID to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        id_num = int(todo_id)
        return id_num > 0
    except ValueError:
        return False


def parse_command(user_input: str) -> tuple:
    """
    Parse the user command and extract the command and arguments.

    Args:
        user_input: The raw user input string

    Returns:
        tuple: (command, list of arguments)
    """
    if not user_input.strip():
        return ("", [])

    parts = user_input.strip().split()
    command = parts[0].lower()
    args = parts[1:]

    # Handle quoted arguments
    if '"' in user_input or "'" in user_input:
        # Use regex to split while preserving quoted strings
        pattern = r'"([^"]*)"|\'([^\']*)\'|(\S+)'
        matches = re.findall(pattern, user_input)
        # Each match is a tuple of 3 elements, one of which will be non-empty
        parsed_parts = [match[0] or match[1] or match[2] for match in matches]
        command = parsed_parts[0].lower() if parsed_parts else ""
        args = parsed_parts[1:] if len(parsed_parts) > 1 else []

    return command, args


def format_todo_display(todo) -> str:
    """
    Format a todo item for display.

    Args:
        todo: A Todo object

    Returns:
        str: Formatted string representation of the todo
    """
    status = "✓" if todo.completed else "○"
    return f"[{status}] {todo.id}: {todo.title} - {todo.description}"


def is_valid_title(title: str) -> bool:
    """
    Validate if the provided title is valid (non-empty after stripping).

    Args:
        title: The title to validate

    Returns:
        bool: True if valid, False otherwise
    """
    return bool(title and title.strip())


def confirm_action(prompt: str) -> bool:
    """
    Ask the user for confirmation.

    Args:
        prompt: The confirmation message to display

    Returns:
        bool: True if user confirms, False otherwise
    """
    response = input(f"{prompt} (y/N): ").strip().lower()
    return response in ['y', 'yes']