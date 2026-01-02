#!/usr/bin/env python3
"""
Main entry point for the Console-based Todo Application.

This application allows users to manage their todo items through a command-line interface.
It supports adding, listing, completing, deleting, and editing todo items with persistent storage.
"""

from todo_app import TodoApp


def main():
    """Main function to run the Todo application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()