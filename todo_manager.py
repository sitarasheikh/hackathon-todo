import json
import os
from datetime import datetime
from typing import List, Optional


class Todo:
    """Represents an individual todo item."""

    def __init__(self, id: int, title: str, description: str = "", completed: bool = False):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert the Todo object to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def update(self, title: Optional[str] = None, description: Optional[str] = None,
               completed: Optional[bool] = None):
        """Update the todo item with new values."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if completed is not None:
            self.completed = completed
        self.updated_at = datetime.now().isoformat()

    def __str__(self) -> str:
        """String representation of the todo item."""
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}: {self.title} - {self.description}"


class TodoManager:
    """Manages the collection of todo items."""

    def __init__(self, data_file: str = "data/todos.json"):
        self.data_file = data_file
        self.todos: List[Todo] = []
        self._ensure_data_directory()
        self.load_todos()

    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        data_dir = os.path.dirname(self.data_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def get_next_id(self) -> int:
        """Get the next available ID for a new todo."""
        if not self.todos:
            return 1
        return max(todo.id for todo in self.todos) + 1

    def add_todo(self, title: str, description: str = "") -> Todo:
        """Add a new todo item."""
        if not title.strip():
            raise ValueError("Title cannot be empty")

        new_id = self.get_next_id()
        todo = Todo(new_id, title.strip(), description.strip())
        self.todos.append(todo)
        self.save_todos()
        return todo

    def list_todos(self) -> List[Todo]:
        """Return all todo items."""
        return self.todos

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """Get a specific todo by ID."""
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def complete_todo(self, todo_id: int) -> bool:
        """Mark a todo as completed."""
        todo = self.get_todo(todo_id)
        if todo:
            todo.update(completed=True)
            self.save_todos()
            return True
        return False

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo by ID."""
        todo = self.get_todo(todo_id)
        if todo:
            self.todos.remove(todo)
            self.save_todos()
            return True
        return False

    def edit_todo(self, todo_id: int, new_title: Optional[str] = None,
                  new_description: Optional[str] = None) -> bool:
        """Edit a todo's title and/or description."""
        todo = self.get_todo(todo_id)
        if todo:
            todo.update(
                title=new_title.strip() if new_title else None,
                description=new_description.strip() if new_description else None
            )
            self.save_todos()
            return True
        return False

    def save_todos(self):
        """Save todos to the data file."""
        try:
            data = [todo.to_dict() for todo in self.todos]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise IOError(f"Error saving todos to file: {e}")

    def load_todos(self):
        """Load todos from the data file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                self.todos = []
                for item in data:
                    todo = Todo(
                        id=item['id'],
                        title=item['title'],
                        description=item.get('description', ''),
                        completed=item.get('completed', False)
                    )
                    # Preserve timestamps if they exist
                    if 'created_at' in item:
                        todo.created_at = item['created_at']
                    if 'updated_at' in item:
                        todo.updated_at = item['updated_at']
                    self.todos.append(todo)
            else:
                self.todos = []
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Warning: Error loading todos from file: {e}. Starting with empty todo list.")
            self.todos = []
        except Exception as e:
            raise IOError(f"Error loading todos from file: {e}")