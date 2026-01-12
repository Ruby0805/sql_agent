"""
SQL Query Tool using Pydantic and SQLite

This module provides a type-safe interface for executing SQL queries
against SQLite databases using Pydantic for validation.
"""

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator, ConfigDict


class QueryType(str, Enum):
    """Supported SQL query types"""
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    CREATE = "CREATE"
    DROP = "DROP"
    ALTER = "ALTER"


class SQLQueryRequest(BaseModel):
    """Model for SQL query request with validation"""

    model_config = ConfigDict(str_strip_whitespace=True)

    query: str = Field(
        ...,
        min_length=1,
        description="SQL query to execute"
    )
    parameters: Optional[Union[tuple, Dict[str, Any]]] = Field(
        default=None,
        description="Query parameters for parameterized queries"
    )
    database_path: str = Field(
        default="ecommerce.db",
        description="Path to SQLite database file"
    )
    fetch_all: bool = Field(
        default=True,
        description="Whether to fetch all results or just one"
    )

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Validate that query is not empty after stripping"""
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()

    @field_validator('database_path')
    @classmethod
    def validate_database_path(cls, v: str) -> str:
        """Validate that database file exists"""
        db_path = Path(v)
        if not db_path.exists():
            raise ValueError(f"Database file not found: {v}")
        if not db_path.is_file():
            raise ValueError(f"Database path is not a file: {v}")
        return v


class QueryResult(BaseModel):
    """Model for query execution results"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    success: bool = Field(
        ...,
        description="Whether the query executed successfully"
    )
    data: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Query results for SELECT queries"
    )
    rows_affected: Optional[int] = Field(
        default=None,
        description="Number of rows affected for INSERT/UPDATE/DELETE"
    )
    last_row_id: Optional[int] = Field(
        default=None,
        description="Last inserted row ID for INSERT queries"
    )
    columns: Optional[List[str]] = Field(
        default=None,
        description="Column names for SELECT queries"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if query failed"
    )
    execution_time_ms: Optional[float] = Field(
        default=None,
        description="Query execution time in milliseconds"
    )
    query_type: Optional[QueryType] = Field(
        default=None,
        description="Type of SQL query executed"
    )


class SQLiteQueryExecutor:
    """Execute SQL queries against SQLite database with Pydantic validation"""

    def __init__(self, database_path: str = "ecommerce.db"):
        """
        Initialize the query executor

        Args:
            database_path: Path to the SQLite database file
        """
        self.database_path = database_path
        self._validate_database()

    def _validate_database(self) -> None:
        """Validate that database exists and is accessible"""
        db_path = Path(self.database_path)
        if not db_path.exists():
            raise FileNotFoundError(f"Database file not found: {self.database_path}")
        if not db_path.is_file():
            raise ValueError(f"Database path is not a file: {self.database_path}")

    def _get_query_type(self, query: str) -> Optional[QueryType]:
        """Determine the type of SQL query"""
        query_upper = query.strip().upper()
        for query_type in QueryType:
            if query_upper.startswith(query_type.value):
                return query_type
        return None

    def _execute_query(
        self,
        connection: sqlite3.Connection,
        cursor: sqlite3.Cursor,
        request: SQLQueryRequest
    ) -> QueryResult:
        """Internal method to execute the query and return results"""
        start_time = datetime.now()

        try:
            # Execute query with or without parameters
            if request.parameters:
                cursor.execute(request.query, request.parameters)
            else:
                cursor.execute(request.query)

            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            # Determine query type
            query_type = self._get_query_type(request.query)

            # Handle SELECT queries
            if query_type == QueryType.SELECT:
                columns = [description[0] for description in cursor.description]

                if request.fetch_all:
                    rows = cursor.fetchall()
                else:
                    row = cursor.fetchone()
                    rows = [row] if row else []

                # Convert rows to list of dictionaries
                data = [dict(zip(columns, row)) for row in rows]

                return QueryResult(
                    success=True,
                    data=data,
                    columns=columns,
                    execution_time_ms=execution_time,
                    query_type=query_type
                )

            # Handle INSERT/UPDATE/DELETE queries
            else:
                connection.commit()
                return QueryResult(
                    success=True,
                    rows_affected=cursor.rowcount,
                    last_row_id=cursor.lastrowid if query_type == QueryType.INSERT else None,
                    execution_time_ms=execution_time,
                    query_type=query_type
                )

        except sqlite3.Error as e:
            connection.rollback()
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            return QueryResult(
                success=False,
                error_message=str(e),
                execution_time_ms=execution_time,
                query_type=self._get_query_type(request.query)
            )

    def execute(self, request: SQLQueryRequest) -> QueryResult:
        """
        Execute a SQL query with validation

        Args:
            request: SQLQueryRequest with query details

        Returns:
            QueryResult with execution results
        """
        connection = None
        try:
            # Enable row factory for dictionary-like access
            connection = sqlite3.connect(request.database_path)
            cursor = connection.cursor()

            # Execute the query
            result = self._execute_query(connection, cursor, request)

            return result

        except Exception as e:
            return QueryResult(
                success=False,
                error_message=f"Unexpected error: {str(e)}",
                query_type=None
            )

        finally:
            if connection:
                connection.close()

    def execute_raw(
        self,
        query: str,
        parameters: Optional[Union[tuple, Dict[str, Any]]] = None,
        fetch_all: bool = True
    ) -> QueryResult:
        """
        Convenience method to execute a query without creating a request object

        Args:
            query: SQL query string
            parameters: Optional query parameters
            fetch_all: Whether to fetch all results

        Returns:
            QueryResult with execution results
        """
        request = SQLQueryRequest(
            query=query,
            parameters=parameters,
            database_path=self.database_path,
            fetch_all=fetch_all
        )
        return self.execute(request)


def main():
    """Example usage of the SQL Query Tool"""

    # Initialize executor
    executor = SQLiteQueryExecutor("ecommerce.db")

    # Example 1: Simple SELECT query
    print("=" * 80)
    print("Example 1: Get top 5 customers by loyalty points")
    print("=" * 80)

    result = executor.execute_raw(
        query="""
        SELECT customer_id, first_name, last_name, email, loyalty_points
        FROM customers
        ORDER BY loyalty_points DESC
        LIMIT 5
        """
    )

    if result.success:
        print(f"Query executed in {result.execution_time_ms:.2f}ms")
        print(f"Columns: {result.columns}")
        print(f"Rows returned: {len(result.data)}")
        print("\nResults:")
        for row in result.data:
            print(f"  {row}")
    else:
        print(f"Error: {result.error_message}")

    # Example 2: Parameterized query
    print("\n" + "=" * 80)
    print("Example 2: Get products by category (parameterized)")
    print("=" * 80)

    result = executor.execute_raw(
        query="""
        SELECT product_id, product_name, unit_price, category_id
        FROM products
        WHERE category_id = ?
        LIMIT 5
        """,
        parameters=(1,)
    )

    if result.success:
        print(f"Query executed in {result.execution_time_ms:.2f}ms")
        print(f"Rows returned: {len(result.data)}")
        print("\nResults:")
        for row in result.data:
            print(f"  {row}")
    else:
        print(f"Error: {result.error_message}")

    # Example 3: Aggregate query
    print("\n" + "=" * 80)
    print("Example 3: Get order statistics")
    print("=" * 80)

    result = executor.execute_raw(
        query="""
        SELECT
            order_status,
            COUNT(*) as order_count,
            AVG(total_amount) as avg_amount,
            SUM(total_amount) as total_revenue
        FROM orders
        GROUP BY order_status
        """
    )

    if result.success:
        print(f"Query executed in {result.execution_time_ms:.2f}ms")
        print("\nResults:")
        for row in result.data:
            print(f"  Status: {row['order_status']}")
            print(f"  Orders: {row['order_count']}")
            print(f"  Avg Amount: ${row['avg_amount']:.2f}")
            print(f"  Total Revenue: ${row['total_revenue']:.2f}")
            print()
    else:
        print(f"Error: {result.error_message}")

    # Example 4: Using SQLQueryRequest for more control
    print("=" * 80)
    print("Example 4: Using SQLQueryRequest model")
    print("=" * 80)

    request = SQLQueryRequest(
        query="SELECT COUNT(*) as total FROM employees WHERE is_active = ?",
        parameters=(1,),
        database_path="ecommerce.db",
        fetch_all=True
    )

    result = executor.execute(request)

    if result.success:
        print(f"Active employees: {result.data[0]['total']}")
    else:
        print(f"Error: {result.error_message}")


if __name__ == "__main__":
    main()
