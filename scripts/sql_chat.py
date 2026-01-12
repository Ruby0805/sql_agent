#!/usr/bin/env python3
"""
Interactive SQL Chat - Ask questions about your database in natural language

Usage:
    export GEMINI_API_KEY='your-key-here'
    python sql_chat.py

    Or provide the key interactively when prompted.
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sql_agent import TextToSQLAgent, format_results


def get_api_key() -> str:
    """Get API key from environment or user input"""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("=" * 80)
        print("Gemini API Key Required")
        print("=" * 80)
        print("\nYou can get a free API key from:")
        print("https://aistudio.google.com/app/apikey")
        print()
        print("Options:")
        print("1. Set environment variable: export GEMINI_API_KEY='your-key-here'")
        print("2. Enter it now (this session only)")
        print()

        api_key = input("Enter your Gemini API key (or press Ctrl+C to exit): ").strip()

        if not api_key:
            print("Error: API key cannot be empty")
            sys.exit(1)

    return api_key


def print_welcome():
    """Print welcome message"""
    print()
    print("=" * 80)
    print("SQL Chat - Natural Language Database Query Tool".center(80))
    print("=" * 80)
    print()
    print("Ask questions about your e-commerce database in plain English!")
    print()
    print("Examples:")
    print("  - What are the top 10 products by revenue?")
    print("  - Show me customers who spent more than $50,000")
    print("  - Which employees have processed the most orders?")
    print("  - What's the average order value by month?")
    print()
    print("Commands:")
    print("  /help     - Show this help message")
    print("  /examples - Show example questions")
    print("  /schema   - Show database schema")
    print("  /quit     - Exit the program")
    print("=" * 80)
    print()


def print_examples():
    """Print example questions"""
    print()
    print("=" * 80)
    print("Example Questions")
    print("=" * 80)
    print()

    examples = [
        ("Sales Analysis", [
            "What are the top 5 customers by total spending?",
            "Show me monthly revenue for the last 6 months",
            "Which products have the highest profit margins?",
            "What's the average order value?",
        ]),
        ("Customer Analysis", [
            "How many active customers do we have?",
            "Which customers haven't ordered in 6 months?",
            "What's the customer distribution by country?",
        ]),
        ("Inventory", [
            "Which products are low on stock?",
            "Show me products that have never been ordered",
            "What's the total inventory value?",
        ]),
        ("Employee Performance", [
            "Which employees have processed the most orders?",
            "Show me employees by department",
            "What's the average salary by department?",
        ]),
    ]

    for category, questions in examples:
        print(f"{category}:")
        for q in questions:
            print(f"  • {q}")
        print()

    print("=" * 80)
    print()


def show_schema(agent: TextToSQLAgent):
    """Show database schema"""
    print()
    print("=" * 80)
    print("Database Schema")
    print("=" * 80)
    print()
    print(agent.schema)
    print()
    print("=" * 80)
    print()


def main():
    """Run interactive SQL chat"""

    # Get API key
    try:
        api_key = get_api_key()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)

    # Initialize agent
    try:
        print("\nInitializing agent...")
        db_path = Path(__file__).parent.parent / "data" / "ecommerce.db"
        agent = TextToSQLAgent(api_key=api_key, database_path=str(db_path))
        print("Ready!\n")
    except Exception as e:
        print(f"Error initializing agent: {e}")
        sys.exit(1)

    # Print welcome message
    print_welcome()

    # Main loop
    while True:
        try:
            # Get user input
            question = input("Ask a question (or /help): ").strip()

            if not question:
                continue

            # Handle commands
            if question.startswith('/'):
                cmd = question.lower()

                if cmd in ['/quit', '/exit', '/q']:
                    print("\nGoodbye!")
                    break

                elif cmd == '/help':
                    print_welcome()
                    continue

                elif cmd == '/examples':
                    print_examples()
                    continue

                elif cmd == '/schema':
                    show_schema(agent)
                    continue

                else:
                    print(f"Unknown command: {question}")
                    print("Try /help for available commands")
                    print()
                    continue

            # Execute question
            print()
            response = agent.ask(question)
            format_results(response, max_rows=20)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break

        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
