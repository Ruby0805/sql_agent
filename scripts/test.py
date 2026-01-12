#!/usr/bin/env python3
"""
Simple test script for the Text-to-SQL agent
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sql_agent import TextToSQLAgent, format_results


def main():
    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("=" * 80)
        print("ERROR: GEMINI_API_KEY environment variable not set")
        print("=" * 80)
        print("\nTo get a free API key:")
        print("1. Go to: https://aistudio.google.com/app/apikey")
        print("2. Click 'Create API Key'")
        print("3. Set it in your environment:")
        print()
        print("   export GEMINI_API_KEY='your-api-key-here'")
        print()
        print("=" * 80)
        sys.exit(1)

    print("=" * 80)
    print("Text-to-SQL Agent Test")
    print("=" * 80)
    print()

    # Initialize agent
    print("Initializing agent...")
    try:
        db_path = Path(__file__).parent.parent / "data" / "ecommerce.db"
        agent = TextToSQLAgent(database_path=str(db_path))
        print("✓ Agent initialized successfully")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize agent: {e}")
        sys.exit(1)

    # Test question
    question = "What are the top 5 customers by total spending?"

    print(f"Test Question: {question}")
    print()

    # Execute query
    print("Generating and executing SQL...")
    response = agent.ask(question)

    # Display results
    format_results(response, max_rows=10)

    if response.success and response.query_result and response.query_result.success:
        print("✓ Test completed successfully!")
    else:
        print("✗ Test failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
