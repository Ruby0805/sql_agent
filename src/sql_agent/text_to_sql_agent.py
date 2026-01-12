"""
Text-to-SQL Agent using Google Gemini API and Pydantic

This agent converts natural language queries to SQL and executes them
using the SQLite query tool.
"""

import os
import re
from typing import Optional, List, Dict, Any
from pathlib import Path

import google.generativeai as genai
from pydantic import BaseModel, Field, field_validator

from .sql_query_tool import SQLiteQueryExecutor, QueryResult


class TextToSQLRequest(BaseModel):
    """Model for text-to-SQL request"""

    question: str = Field(
        ...,
        min_length=1,
        description="Natural language question about the data"
    )
    database_path: str = Field(
        default="ecommerce.db",
        description="Path to SQLite database"
    )
    include_explanation: bool = Field(
        default=True,
        description="Whether to include explanation of the generated SQL"
    )

    @field_validator('question')
    @classmethod
    def validate_question(cls, v: str) -> str:
        """Validate that question is not empty"""
        if not v.strip():
            raise ValueError("Question cannot be empty")
        return v.strip()


class TextToSQLResponse(BaseModel):
    """Model for text-to-SQL response"""

    success: bool = Field(
        ...,
        description="Whether the operation was successful"
    )
    question: str = Field(
        ...,
        description="Original natural language question"
    )
    generated_sql: Optional[str] = Field(
        default=None,
        description="Generated SQL query"
    )
    explanation: Optional[str] = Field(
        default=None,
        description="Explanation of the SQL query"
    )
    query_result: Optional[QueryResult] = Field(
        default=None,
        description="Result from executing the SQL query"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if operation failed"
    )


class TextToSQLAgent:
    """Agent that converts natural language to SQL using Gemini API"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        database_path: str = "ecommerce.db",
        model_name: str = "gemini-2.0-flash-exp"
    ):
        """
        Initialize the Text-to-SQL agent

        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
            database_path: Path to SQLite database
            model_name: Gemini model to use
        """
        self.database_path = database_path
        self.model_name = model_name

        # Configure Gemini API
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "Gemini API key required. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

        # Initialize SQL executor
        self.executor = SQLiteQueryExecutor(database_path)

        # Load database schema
        self.schema = self._load_schema()

    def _load_schema(self) -> str:
        """Load database schema from schema.sql file"""
        # Try multiple possible locations for schema file
        possible_paths = [
            Path("data/schema.sql"),
            Path("schema.sql"),
            Path("../data/schema.sql"),
            Path("../../data/schema.sql"),
        ]

        for schema_path in possible_paths:
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    return f.read()

        # Fallback: extract schema from database
        return self._extract_schema_from_db()

    def _extract_schema_from_db(self) -> str:
        """Extract schema directly from database"""
        result = self.executor.execute_raw(
            "SELECT sql FROM sqlite_master WHERE type='table' ORDER BY name"
        )

        if result.success and result.data:
            schema_parts = []
            for row in result.data:
                if row['sql']:
                    schema_parts.append(row['sql'] + ';')
            return '\n\n'.join(schema_parts)
        return ""

    def _create_prompt(self, question: str, include_explanation: bool = True) -> str:
        """Create prompt for Gemini API"""
        prompt = f"""You are an expert SQL query generator for SQLite databases.

DATABASE SCHEMA:
{self.schema}

TASK:
Convert the following natural language question into a valid SQLite SQL query.

QUESTION: {question}

REQUIREMENTS:
1. Generate ONLY executable SQL - no markdown code blocks, no explanations in the SQL
2. Use proper SQLite syntax and functions
3. Consider performance and use appropriate indexes
4. Handle NULL values appropriately
5. Use meaningful aliases for readability
6. Follow these specific rules:
   - For date operations, use strftime() function
   - For string operations, use SQLite string functions (LIKE, ||, etc.)
   - Always filter out cancelled orders when analyzing sales/revenue
   - Use appropriate JOINs based on foreign key relationships

OUTPUT FORMAT:
Generate the SQL query on the first line, followed by a blank line, then provide a brief explanation.

Example:
SELECT * FROM customers LIMIT 10;

This query retrieves the first 10 customer records from the customers table.

Now generate the SQL for the question above:"""

        return prompt

    def _extract_sql_from_response(self, response_text: str) -> tuple[str, str]:
        """
        Extract SQL query and explanation from Gemini response

        Returns:
            Tuple of (sql_query, explanation)
        """
        # Remove markdown code blocks if present
        response_text = re.sub(r'```sql\n?', '', response_text)
        response_text = re.sub(r'```\n?', '', response_text)

        # Split by double newline or look for first semicolon
        parts = response_text.split('\n\n', 1)

        if len(parts) == 2:
            sql = parts[0].strip()
            explanation = parts[1].strip()
        else:
            # Try to find SQL ending with semicolon
            lines = response_text.split('\n')
            sql_lines = []
            explanation_lines = []
            found_sql_end = False

            for line in lines:
                if not found_sql_end:
                    sql_lines.append(line)
                    if ';' in line:
                        found_sql_end = True
                else:
                    explanation_lines.append(line)

            sql = '\n'.join(sql_lines).strip()
            explanation = '\n'.join(explanation_lines).strip()

        # Clean up SQL
        sql = sql.strip()
        if not sql.endswith(';'):
            sql += ';'

        return sql, explanation

    def generate_sql(self, question: str, include_explanation: bool = True) -> tuple[str, str]:
        """
        Generate SQL from natural language question

        Args:
            question: Natural language question
            include_explanation: Whether to include explanation

        Returns:
            Tuple of (sql_query, explanation)
        """
        prompt = self._create_prompt(question, include_explanation)

        try:
            response = self.model.generate_content(prompt)
            sql, explanation = self._extract_sql_from_response(response.text)
            return sql, explanation

        except Exception as e:
            raise Exception(f"Failed to generate SQL: {str(e)}")

    def execute(self, request: TextToSQLRequest) -> TextToSQLResponse:
        """
        Execute a text-to-SQL request

        Args:
            request: TextToSQLRequest with question

        Returns:
            TextToSQLResponse with results
        """
        try:
            # Generate SQL from natural language
            sql, explanation = self.generate_sql(
                request.question,
                request.include_explanation
            )

            # Execute the generated SQL
            query_result = self.executor.execute_raw(sql.rstrip(';'))

            return TextToSQLResponse(
                success=True,
                question=request.question,
                generated_sql=sql,
                explanation=explanation if request.include_explanation else None,
                query_result=query_result
            )

        except Exception as e:
            return TextToSQLResponse(
                success=False,
                question=request.question,
                error_message=str(e)
            )

    def ask(
        self,
        question: str,
        include_explanation: bool = True
    ) -> TextToSQLResponse:
        """
        Convenience method to ask a question directly

        Args:
            question: Natural language question
            include_explanation: Whether to include explanation

        Returns:
            TextToSQLResponse with results
        """
        request = TextToSQLRequest(
            question=question,
            database_path=self.database_path,
            include_explanation=include_explanation
        )
        return self.execute(request)


def format_results(response: TextToSQLResponse, max_rows: int = 20) -> None:
    """Pretty print the results"""
    print("=" * 80)
    print("QUESTION:")
    print("=" * 80)
    print(response.question)
    print()

    if not response.success:
        print("=" * 80)
        print("ERROR:")
        print("=" * 80)
        print(response.error_message)
        return

    print("=" * 80)
    print("GENERATED SQL:")
    print("=" * 80)
    print(response.generated_sql)
    print()

    if response.explanation:
        print("=" * 80)
        print("EXPLANATION:")
        print("=" * 80)
        print(response.explanation)
        print()

    if response.query_result:
        result = response.query_result

        if not result.success:
            print("=" * 80)
            print("SQL EXECUTION ERROR:")
            print("=" * 80)
            print(result.error_message)
            return

        print("=" * 80)
        print("RESULTS:")
        print("=" * 80)
        print(f"Execution time: {result.execution_time_ms:.2f}ms")
        print(f"Query type: {result.query_type.value if result.query_type else 'N/A'}")

        if result.data is not None:
            print(f"Rows returned: {len(result.data)}")
            print()

            if len(result.data) > 0:
                # Display results
                display_rows = result.data[:max_rows]

                # Print column headers
                if result.columns:
                    print("-" * 80)
                    header = " | ".join(f"{col[:15]:<15}" for col in result.columns)
                    print(header)
                    print("-" * 80)

                # Print rows
                for row in display_rows:
                    values = []
                    for col in result.columns:
                        val = row[col]
                        if val is None:
                            val_str = "NULL"
                        elif isinstance(val, float):
                            val_str = f"{val:.2f}"
                        else:
                            val_str = str(val)
                        values.append(f"{val_str[:15]:<15}")

                    print(" | ".join(values))

                if len(result.data) > max_rows:
                    print(f"\n... and {len(result.data) - max_rows} more rows")

                print("-" * 80)
            else:
                print("No rows returned")

        elif result.rows_affected is not None:
            print(f"Rows affected: {result.rows_affected}")
            if result.last_row_id:
                print(f"Last inserted row ID: {result.last_row_id}")

    print()


def main():
    """Example usage"""
    import sys

    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY environment variable not set")
        print("\nTo set it:")
        print("  export GEMINI_API_KEY='your-api-key-here'")
        print("\nGet your API key from: https://aistudio.google.com/app/apikey")
        sys.exit(1)

    # Initialize agent
    print("Initializing Text-to-SQL Agent...")
    agent = TextToSQLAgent(database_path="ecommerce.db")
    print("Agent ready!\n")

    # Example questions
    questions = [
        "What are the top 5 customers by total spending?",
        "Show me the monthly revenue for 2025",
        "Which products have never been ordered?",
        "What's the average order value by customer country?",
        "Find employees who have processed more than 10 orders",
    ]

    print("Running example queries...\n")

    for i, question in enumerate(questions, 1):
        print(f"\n{'#' * 80}")
        print(f"EXAMPLE {i}/{len(questions)}")
        print(f"{'#' * 80}\n")

        response = agent.ask(question)
        format_results(response, max_rows=10)

        if i < len(questions):
            input("\nPress Enter to continue to next example...")


if __name__ == "__main__":
    main()
