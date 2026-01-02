#!/usr/bin/env python3
"""
Quick test script to verify the todo application functionality.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from todo_manager import TodoManager
from todo_app import TodoApp

def test_basic_functionality():
    print("Testing basic functionality...")

    # Test TodoManager
    tm = TodoManager("test_todos.json")

    # Test adding a todo
    todo1 = tm.add_todo("Test todo", "This is a test")
    print(f"Added todo: {todo1.title}")

    # Test listing todos
    todos = tm.list_todos()
    print(f"Number of todos: {len(todos)}")

    # Test completing a todo
    success = tm.complete_todo(todo1.id)
    print(f"Completed todo: {success}")

    # Test editing a todo
    success = tm.edit_todo(todo1.id, "Updated title", "Updated description")
    print(f"Edited todo: {success}")

    # Test deleting a todo
    success = tm.delete_todo(todo1.id)
    print(f"Deleted todo: {success}")

    # Clean up test file
    if os.path.exists("test_todos.json"):
        os.remove("test_todos.json")

    print("Basic functionality test completed successfully!")

if __name__ == "__main__":
    test_basic_functionality()