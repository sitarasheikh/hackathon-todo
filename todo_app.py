import sys
from typing import List
from todo_manager import TodoManager, Todo


class TodoApp:
    """Main application class that handles user interaction and command processing."""

    def __init__(self):
        self.todo_manager = TodoManager()
        self.running = True

    def display_help(self):
        """Display help information for available commands."""
        help_text = """
Available Commands:
  add "title" "description"    - Add a new todo item
  list                        - List all todo items
  complete <id>               - Mark a todo as completed
  delete <id>                 - Delete a todo item
  edit <id> "title" "desc"    - Edit a todo item
  help                        - Show this help message
  quit                        - Exit the application

Examples:
  add "Buy groceries" "Milk, bread, eggs"
  complete 1
  delete 2
  edit 3 "Updated title" "New description"
        """
        print(help_text)

    def display_todos(self):
        """Display all todos in a formatted way."""
        todos = self.todo_manager.list_todos()

        if not todos:
            print("No todos found.")
            return

        print("\nYour Todo List:")
        print("-" * 50)
        for todo in todos:
            status = "✓" if todo.completed else "○"
            print(f"[{status}] {todo.id}: {todo.title} - {todo.description}")
        print("-" * 50)
        print(f"Total: {len(todos)} todos")

    def handle_add(self, args: List[str]):
        """Handle the add command."""
        if len(args) < 1:
            print("Error: Please provide a title for the new todo.")
            print("Usage: add \"title\" \"description\" (description is optional)")
            return

        title = args[0]
        description = args[1] if len(args) > 1 else ""

        try:
            todo = self.todo_manager.add_todo(title, description)
            print(f"Added todo: {todo.title}")
        except ValueError as e:
            print(f"Error: {e}")

    def handle_list(self, args: List[str]):
        """Handle the list command."""
        self.display_todos()

    def handle_complete(self, args: List[str]):
        """Handle the complete command."""
        if len(args) != 1:
            print("Error: Please provide a valid todo ID.")
            print("Usage: complete <id>")
            return

        try:
            todo_id = int(args[0])
            success = self.todo_manager.complete_todo(todo_id)
            if success:
                print(f"Marked todo {todo_id} as completed.")
            else:
                print(f"Error: Todo with ID {todo_id} not found.")
        except ValueError:
            print("Error: Please provide a valid numeric ID.")

    def handle_delete(self, args: List[str]):
        """Handle the delete command."""
        if len(args) != 1:
            print("Error: Please provide a valid todo ID.")
            print("Usage: delete <id>")
            return

        try:
            todo_id = int(args[0])
            # Confirm deletion for safety
            todo = self.todo_manager.get_todo(todo_id)
            if not todo:
                print(f"Error: Todo with ID {todo_id} not found.")
                return

            print(f"You are about to delete: {todo.title}")
            confirm = input("Confirm deletion? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                success = self.todo_manager.delete_todo(todo_id)
                if success:
                    print(f"Deleted todo {todo_id}.")
                else:
                    print(f"Error: Todo with ID {todo_id} not found.")
            else:
                print("Deletion cancelled.")
        except ValueError:
            print("Error: Please provide a valid numeric ID.")

    def handle_edit(self, args: List[str]):
        """Handle the edit command."""
        if len(args) < 2:
            print("Error: Please provide a todo ID, title, and optionally a description.")
            print("Usage: edit <id> \"title\" \"description\" (description is optional)")
            return

        try:
            todo_id = int(args[0])
            new_title = args[1]
            new_description = args[2] if len(args) > 2 else ""

            success = self.todo_manager.edit_todo(todo_id, new_title, new_description)
            if success:
                print(f"Updated todo {todo_id}.")
            else:
                print(f"Error: Todo with ID {todo_id} not found.")
        except ValueError:
            print("Error: Please provide a valid numeric ID.")

    def handle_help_command(self, args: List[str]):
        """Handle the help command."""
        self.display_help()

    def handle_quit(self, args: List[str]):
        """Handle the quit command."""
        print("Goodbye!")
        self.running = False

    def process_command(self, user_input: str):
        """Process a user command."""
        if not user_input.strip():
            return

        parts = user_input.strip().split()
        command = parts[0].lower()
        args = parts[1:]

        # Handle quoted arguments
        if '"' in user_input or "'" in user_input:
            import re
            # Use regex to split while preserving quoted strings
            pattern = r'"([^"]*)"|\'([^\']*)\'|(\S+)'
            matches = re.findall(pattern, user_input)
            # Each match is a tuple of 3 elements, one of which will be non-empty
            parsed_parts = [match[0] or match[1] or match[2] for match in matches]
            command = parsed_parts[0].lower() if parsed_parts else ""
            args = parsed_parts[1:] if len(parsed_parts) > 1 else []

        # Command handlers
        command_handlers = {
            'add': self.handle_add,
            'list': self.handle_list,
            'complete': self.handle_complete,
            'delete': self.handle_delete,
            'edit': self.handle_edit,
            'help': self.handle_help_command,
            'quit': self.handle_quit,
            'exit': self.handle_quit,  # Alternative to quit
        }

        if command in command_handlers:
            command_handlers[command](args)
        else:
            print(f"Unknown command: {command}")
            print("Type 'help' for available commands.")

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Console-based Todo Application!")
        print("Type 'help' for available commands or 'quit' to exit.")

        while self.running:
            try:
                user_input = input("\n> ").strip()
                self.process_command(user_input)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break