"""
SQL Agent - Natural Language to SQL Query Tool

A Pydantic-based tool for executing SQL queries and converting natural language
to SQL using Google's Gemini API.
"""

from .sql_query_tool import (
    SQLQueryRequest,
    QueryResult,
    QueryType,
    SQLiteQueryExecutor,
)

from .text_to_sql_agent import (
    TextToSQLRequest,
    TextToSQLResponse,
    TextToSQLAgent,
    format_results,
)

__version__ = "0.1.0"
__author__ = "SQL Agent Team"

__all__ = [
    # Query Executor
    "SQLQueryRequest",
    "QueryResult",
    "QueryType",
    "SQLiteQueryExecutor",
    # Text-to-SQL Agent
    "TextToSQLRequest",
    "TextToSQLResponse",
    "TextToSQLAgent",
    "format_results",
]
