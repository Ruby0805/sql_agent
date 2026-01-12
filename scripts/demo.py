#!/usr/bin/env python3
"""
Demo of the Text-to-SQL Agent (without requiring API key)

This script demonstrates how the agent works by using pre-defined SQL
queries instead of generating them with Gemini.
"""

import sys
from pathlib import Path

from sql_agent import SQLiteQueryExecutor, QueryResult, TextToSQLResponse, format_results

# Database path
DB_PATH = Path(__file__).parent.parent / "data" / "ecommerce.db"


def demo_question_1():
    """Demo: Top 5 customers by total spending"""

    question = "What are the top 5 customers by total spending?"

    # This is what Gemini would generate
    generated_sql = """SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.email,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status != 'Cancelled'
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 5;"""

    explanation = """This query joins the customers and orders tables to calculate
the total spending for each customer. It filters out cancelled orders,
groups by customer, and returns the top 5 customers sorted by total spending."""

    # Execute the SQL
    executor = SQLiteQueryExecutor(str(DB_PATH))
    query_result = executor.execute_raw(generated_sql.strip())

    # Create response
    response = TextToSQLResponse(
        success=True,
        question=question,
        generated_sql=generated_sql.strip(),
        explanation=explanation.strip(),
        query_result=query_result
    )

    return response


def demo_question_2():
    """Demo: Monthly revenue for 2025"""

    question = "Show me monthly revenue for 2025"

    generated_sql = """SELECT
    strftime('%Y-%m', order_date) as month,
    COUNT(*) as total_orders,
    SUM(total_amount) as revenue,
    AVG(total_amount) as avg_order_value
FROM orders
WHERE order_status != 'Cancelled'
    AND strftime('%Y', order_date) = '2025'
GROUP BY month
ORDER BY month;"""

    explanation = """This query uses strftime to extract year-month from order dates,
filters for 2025 orders that aren't cancelled, and calculates monthly metrics
including total orders, revenue, and average order value."""

    executor = SQLiteQueryExecutor(str(DB_PATH))
    query_result = executor.execute_raw(generated_sql.strip())

    response = TextToSQLResponse(
        success=True,
        question=question,
        generated_sql=generated_sql.strip(),
        explanation=explanation.strip(),
        query_result=query_result
    )

    return response


def demo_question_3():
    """Demo: Products with low stock"""

    question = "Which products are low on stock (below reorder level)?"

    generated_sql = """SELECT
    p.product_name,
    p.sku,
    c.category_name,
    i.quantity_on_hand,
    i.reorder_level,
    i.reorder_quantity,
    s.supplier_name
FROM inventory i
JOIN products p ON i.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
JOIN suppliers s ON p.supplier_id = s.supplier_id
WHERE i.quantity_on_hand <= i.reorder_level
    AND p.is_active = 1
ORDER BY (i.reorder_level - i.quantity_on_hand) DESC
LIMIT 10;"""

    explanation = """This query identifies products that need reordering by comparing
quantity on hand against the reorder level. It joins with products, categories,
and suppliers to provide complete context, and orders by urgency (how far below
the reorder level)."""

    executor = SQLiteQueryExecutor(str(DB_PATH))
    query_result = executor.execute_raw(generated_sql.strip())

    response = TextToSQLResponse(
        success=True,
        question=question,
        generated_sql=generated_sql.strip(),
        explanation=explanation.strip(),
        query_result=query_result
    )

    return response


def demo_question_4():
    """Demo: Employee performance"""

    question = "Which employees have processed the most orders?"

    generated_sql = """SELECT
    e.employee_id,
    e.first_name || ' ' || e.last_name as employee_name,
    e.position,
    d.department_name,
    COUNT(o.order_id) as orders_processed,
    SUM(o.total_amount) as total_sales,
    AVG(o.total_amount) as avg_order_value
FROM employees e
JOIN departments d ON e.department_id = d.department_id
LEFT JOIN orders o ON e.employee_id = o.employee_id
    AND o.order_status != 'Cancelled'
WHERE e.is_active = 1
GROUP BY e.employee_id
HAVING orders_processed > 0
ORDER BY orders_processed DESC
LIMIT 10;"""

    explanation = """This query measures employee performance by counting orders processed
and calculating total sales. It joins employees with their departments and orders,
filters for active employees and non-cancelled orders, and returns the top performers."""

    executor = SQLiteQueryExecutor(str(DB_PATH))
    query_result = executor.execute_raw(generated_sql.strip())

    response = TextToSQLResponse(
        success=True,
        question=question,
        generated_sql=generated_sql.strip(),
        explanation=explanation.strip(),
        query_result=query_result
    )

    return response


def main():
    """Run demo"""

    print()
    print("=" * 80)
    print("Text-to-SQL Agent Demo".center(80))
    print("=" * 80)
    print()
    print("This demo shows how the agent converts natural language to SQL")
    print("and executes queries against the e-commerce database.")
    print()
    print("Note: This demo uses pre-defined SQL queries to demonstrate the")
    print("agent's functionality. The actual agent uses Gemini AI to generate")
    print("SQL dynamically from any natural language question.")
    print()
    print("=" * 80)
    print()

    demos = [
        ("Customer Analysis", demo_question_1),
        ("Sales Trends", demo_question_2),
        ("Inventory Management", demo_question_3),
        ("Employee Performance", demo_question_4),
    ]

    for i, (category, demo_func) in enumerate(demos, 1):
        print(f"\n{'#' * 80}")
        print(f"DEMO {i}/{len(demos)}: {category}".center(80))
        print(f"{'#' * 80}\n")

        try:
            response = demo_func()
            format_results(response, max_rows=10)
        except Exception as e:
            print(f"Error running demo: {e}")

        if i < len(demos):
            try:
                input("\nPress Enter to continue to next demo...")
            except EOFError:
                # Non-interactive environment, continue automatically
                print("\n[Continuing to next demo...]")
                print()

    print()
    print("=" * 80)
    print("Demo Complete!".center(80))
    print("=" * 80)
    print()
    print("To use the actual Text-to-SQL agent with Gemini AI:")
    print()
    print("1. Get a free API key from: https://aistudio.google.com/app/apikey")
    print("2. Set it: export GEMINI_API_KEY='your-key-here'")
    print("3. Run: python sql_chat.py")
    print()
    print("Or see AGENT_README.md for full documentation.")
    print()


if __name__ == "__main__":
    main()
