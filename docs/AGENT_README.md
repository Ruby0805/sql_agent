# Text-to-SQL Agent with Gemini API

A natural language interface for querying your SQLite database using Google's Gemini API and Pydantic for type safety.

## Features

- **Natural Language Queries**: Ask questions in plain English
- **AI-Powered SQL Generation**: Uses Google Gemini to generate accurate SQL
- **Type-Safe Execution**: Pydantic models ensure data validation
- **Interactive Chat Interface**: User-friendly command-line interface
- **Comprehensive Results**: Get SQL, explanations, and formatted results
- **Error Handling**: Robust error handling and validation

## Prerequisites

1. **Python 3.9+**
2. **Gemini API Key** (free from Google AI Studio)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get a Gemini API key:
   - Visit: https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy your API key

3. Set your API key:
```bash
export GEMINI_API_KEY='your-api-key-here'
```

## Usage

### Interactive Chat Mode

Start an interactive session to ask questions about your database:

```bash
python sql_chat.py
```

Example session:
```
Ask a question: What are the top 5 products by revenue?

GENERATED SQL:
SELECT p.product_name, SUM(oi.subtotal) as total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id
ORDER BY total_revenue DESC
LIMIT 5;

RESULTS:
product_name     | total_revenue
-----------------|--------------
Premium Laptop   | 125,430.50
Gaming Console   | 98,234.25
...
```

### Programmatic Usage

Use the agent in your own Python scripts:

```python
from text_to_sql_agent import TextToSQLAgent, format_results

# Initialize agent
agent = TextToSQLAgent(database_path="ecommerce.db")

# Ask a question
response = agent.ask("What are the top 10 customers by total spending?")

# Display results
format_results(response)

# Or access the data programmatically
if response.success:
    print(f"Generated SQL: {response.generated_sql}")
    print(f"Rows returned: {len(response.query_result.data)}")

    for row in response.query_result.data:
        print(row)
```

### Test Script

Run a simple test to verify everything works:

```bash
python test_agent.py
```

## Available Commands (Interactive Mode)

- `/help` - Show help message
- `/examples` - Show example questions
- `/schema` - Display database schema
- `/quit` - Exit the program

## Example Questions

**Sales Analysis:**
- "What are the top 5 customers by total spending?"
- "Show me monthly revenue for 2025"
- "Which products have the highest profit margins?"
- "What's the average order value by payment method?"

**Customer Analysis:**
- "How many active customers do we have?"
- "Which customers haven't ordered in 6 months?"
- "What's the customer distribution by country?"
- "Show me customers with more than 10 orders"

**Inventory:**
- "Which products are low on stock?"
- "Show me products that have never been ordered"
- "What's the total inventory value?"
- "List products from supplier 'Acme Corp'"

**Employee Performance:**
- "Which employees have processed the most orders?"
- "Show me employees by department"
- "What's the average salary by department?"

## Architecture

### Components

1. **TextToSQLAgent** (`text_to_sql_agent.py`)
   - Converts natural language to SQL using Gemini API
   - Executes queries using SQLiteQueryExecutor
   - Returns structured results with Pydantic models

2. **SQLiteQueryExecutor** (`sql_query_tool.py`)
   - Type-safe SQL query execution
   - Pydantic validation for inputs and outputs
   - Performance tracking and error handling

3. **Interactive CLI** (`sql_chat.py`)
   - User-friendly interface
   - Command support
   - Pretty-printed results

### Data Flow

```
User Question
    ↓
TextToSQLAgent
    ↓
Gemini API (SQL Generation)
    ↓
SQLiteQueryExecutor (Pydantic Validation)
    ↓
SQLite Database
    ↓
Structured Results (Pydantic Models)
    ↓
Formatted Output
```

## Pydantic Models

### TextToSQLRequest
- `question`: Natural language question
- `database_path`: Path to SQLite database
- `include_explanation`: Whether to include SQL explanation

### TextToSQLResponse
- `success`: Operation status
- `question`: Original question
- `generated_sql`: Generated SQL query
- `explanation`: SQL explanation
- `query_result`: QueryResult from execution
- `error_message`: Error details if failed

### SQLQueryRequest
- `query`: SQL query to execute
- `parameters`: Query parameters
- `database_path`: Database path
- `fetch_all`: Fetch all results flag

### QueryResult
- `success`: Execution status
- `data`: Query results as list of dicts
- `rows_affected`: Rows modified (INSERT/UPDATE/DELETE)
- `columns`: Column names
- `execution_time_ms`: Query execution time
- `query_type`: Type of SQL query

## Configuration

### Change Gemini Model

```python
agent = TextToSQLAgent(
    database_path="ecommerce.db",
    model_name="gemini-1.5-pro"  # Use different model
)
```

### Custom Database

```python
agent = TextToSQLAgent(
    database_path="/path/to/your/database.db"
)
```

## Error Handling

The agent includes comprehensive error handling:

- **API Key Missing**: Clear instructions for obtaining and setting key
- **Invalid SQL**: Returns error message from SQLite
- **Network Issues**: Handles Gemini API connection problems
- **Database Errors**: Validates database exists and is accessible
- **Query Validation**: Pydantic validates all inputs and outputs

## Tips for Best Results

1. **Be specific**: "Show top 10 customers by revenue in 2025" vs "Show customers"
2. **Use domain terms**: Reference table/column names when helpful
3. **Ask for aggregations**: "average", "total", "count", etc.
4. **Specify sorting**: "top 10", "highest", "lowest"
5. **Include filters**: "active customers", "non-cancelled orders"

## Troubleshooting

### "API key required" error
```bash
export GEMINI_API_KEY='your-key-here'
```

### "Database file not found" error
Ensure `ecommerce.db` exists in the current directory

### Poor SQL generation
Try being more specific or mentioning table/column names

### Rate limiting
Gemini API has rate limits. Wait a moment between requests.

## Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Validate user inputs in production environments
- Consider query timeouts for long-running queries
- Review generated SQL before execution in production

## License

MIT License

## Contributing

Contributions welcome! Please ensure:
- Code follows existing style
- All Pydantic models have proper validation
- Error handling is comprehensive
- Documentation is updated
