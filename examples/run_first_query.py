"""
Run the first SQL query from example_queries.sql using the Pydantic tool
"""

import sys
from pathlib import Path

from sql_agent import SQLiteQueryExecutor

# Initialize the executor
db_path = Path(__file__).parent.parent / "data" / "ecommerce.db"
executor = SQLiteQueryExecutor(str(db_path))

# First query: Total revenue by month
query = """
SELECT
    strftime('%Y-%m', order_date) as month,
    COUNT(*) as total_orders,
    SUM(total_amount) as revenue,
    AVG(total_amount) as avg_order_value
FROM orders
WHERE order_status != 'Cancelled'
GROUP BY month
ORDER BY month DESC
"""

print("=" * 80)
print("Query 1: Total Revenue by Month")
print("=" * 80)
print(f"\nExecuting query:\n{query}\n")

# Execute the query
result = executor.execute_raw(query)

# Display results
if result.success:
    print(f"✓ Query executed successfully in {result.execution_time_ms:.2f}ms")
    print(f"✓ Query type: {result.query_type.value}")
    print(f"✓ Columns: {result.columns}")
    print(f"✓ Rows returned: {len(result.data)}\n")

    print("-" * 80)
    print(f"{'Month':<12} {'Orders':<12} {'Revenue':<20} {'Avg Order Value':<20}")
    print("-" * 80)

    for row in result.data:
        print(f"{row['month']:<12} {row['total_orders']:<12} ${row['revenue']:>18,.2f} ${row['avg_order_value']:>18,.2f}")

    print("-" * 80)

    # Calculate totals
    total_orders = sum(row['total_orders'] for row in result.data)
    total_revenue = sum(row['revenue'] for row in result.data)
    overall_avg = total_revenue / total_orders if total_orders > 0 else 0

    print(f"\n{'TOTAL':<12} {total_orders:<12} ${total_revenue:>18,.2f} ${overall_avg:>18,.2f}")
    print("=" * 80)

else:
    print(f"✗ Query failed: {result.error_message}")
