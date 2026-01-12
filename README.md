# SQL Agent - Natural Language to SQL Query Tool

<div align="center">

**Ask questions about your database in plain English, powered by Google Gemini AI and Pydantic**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Pydantic](https://img.shields.io/badge/pydantic-2.0+-green.svg)](https://pydantic.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## 🚀 Features

- **🗣️ Natural Language Queries**: Ask questions in plain English, get SQL automatically
- **🔒 Type-Safe**: Full Pydantic validation for all inputs and outputs
- **🤖 AI-Powered**: Uses Google Gemini 2.0 for accurate SQL generation
- **📊 Rich Results**: Get SQL, explanations, and formatted query results
- **💬 Interactive CLI**: User-friendly command-line interface
- **🎯 Schema-Aware**: Agent understands your database structure
- **⚡ Fast Execution**: Optimized query execution with performance tracking
- **🛡️ Error Handling**: Comprehensive validation and error messages

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Interactive Chat](#interactive-chat)
  - [Programmatic Usage](#programmatic-usage)
  - [Command Line Tools](#command-line-tools)
- [Project Structure](#project-structure)
- [Example Queries](#example-queries)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Gemini API key (get free key from https://aistudio.google.com/app/apikey)
export GEMINI_API_KEY='your-api-key-here'

# 3. Run the demo (no API key needed)
python scripts/demo.py

# 4. Or start the interactive chat
python scripts/sql_chat.py
```

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- SQLite 3
- Google Gemini API key (free from [Google AI Studio](https://aistudio.google.com/app/apikey))

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install as Package

```bash
pip install -e .
```

This installs the package in editable mode and creates console scripts:
- `sql-chat` - Interactive chat interface
- `sql-demo` - Run the demo
- `sql-test` - Test the agent

## 🎯 Usage

### Interactive Chat

Start an interactive session to ask questions about your database:

```bash
python scripts/sql_chat.py
```

**Example conversation:**
```
Ask a question: What are the top 5 customers by total spending?

GENERATED SQL:
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status != 'Cancelled'
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 5;

EXPLANATION:
This query joins customers and orders tables, filters out cancelled orders,
and returns the top 5 customers sorted by total spending.

RESULTS:
customer_id | customer_name  | total_orders | total_spent
68          | Dennis Mathis  | 7            | 87893.10
493         | Ryan Hudson    | 6            | 74453.19
...
```

**Available Commands:**
- `/help` - Show help message
- `/examples` - Show example questions
- `/schema` - Display database schema
- `/quit` - Exit

### Programmatic Usage

Use the agent in your own Python scripts:

```python
from src.sql_agent import TextToSQLAgent, format_results

# Initialize agent
agent = TextToSQLAgent(database_path="data/ecommerce.db")

# Ask a question
response = agent.ask("What's the average order value by month?")

# Display formatted results
format_results(response)

# Or access data programmatically
if response.success and response.query_result.success:
    for row in response.query_result.data:
        print(f"{row['month']}: ${row['avg_order_value']:.2f}")
```

### Direct SQL Execution (No AI)

Use the Pydantic-based SQL executor directly:

```python
from src.sql_agent import SQLiteQueryExecutor

# Initialize executor
executor = SQLiteQueryExecutor("data/ecommerce.db")

# Execute query
result = executor.execute_raw(
    query="SELECT * FROM customers WHERE customer_id = ?",
    parameters=(123,)
)

# Access results
if result.success:
    print(f"Execution time: {result.execution_time_ms}ms")
    for row in result.data:
        print(row)
```

### Command Line Tools

**Run Demo** (no API key required):
```bash
python scripts/demo.py
```

Shows 4 pre-built examples with SQL generation and execution.

**Test Agent** (requires API key):
```bash
python scripts/test.py
```

Runs a simple test to verify your setup.

**Run Example Queries**:
```bash
python examples/run_first_query.py
```

## 📁 Project Structure

```
sql_agent/
├── README.md                    # Main documentation (you are here)
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── setup.py                     # Package installation script
├── .gitignore                   # Git ignore rules
│
├── src/sql_agent/              # Main package
│   ├── __init__.py             # Package exports
│   ├── sql_query_tool.py       # Pydantic-based SQL executor
│   └── text_to_sql_agent.py    # Gemini-powered Text-to-SQL agent
│
├── scripts/                     # Executable scripts
│   ├── sql_chat.py             # Interactive CLI (python scripts/sql_chat.py)
│   ├── demo.py                 # Demo without API key (python scripts/demo.py)
│   └── test.py                 # Test script (python scripts/test.py)
│
├── examples/                    # Usage examples
│   ├── run_first_query.py      # Example: Execute SQL with Pydantic tool
│   └── example_queries.sql     # 25+ sample business SQL queries
│
├── data/                        # Database and data files
│   ├── ecommerce.db            # SQLite database (3M rows, 15 tables)
│   ├── schema.sql              # Database schema definition
│   └── generate_data.py        # Script to regenerate test data
│
└── docs/                        # Documentation
    ├── AGENT_README.md         # Detailed agent documentation
    └── DATABASE.md             # Database schema and structure
```

## 💡 Example Queries

### Sales Analysis
- "What are the top 5 customers by total spending?"
- "Show me monthly revenue for 2025"
- "Which products have the highest profit margins?"
- "What's the average order value by payment method?"

### Customer Analytics
- "How many active customers do we have?"
- "Which customers haven't ordered in 6 months?"
- "What's the customer distribution by country?"
- "Show me customers with loyalty points over 4000"

### Inventory Management
- "Which products are low on stock?"
- "Show me products that have never been ordered"
- "What's the total inventory value?"
- "List products from supplier 'Acme Corp'"

### Employee Performance
- "Which employees have processed the most orders?"
- "Show me employees by department"
- "What's the average salary by department?"

### Advanced Analytics
- "Calculate customer lifetime value for top customers"
- "Show monthly sales growth rate"
- "Which promotions were most effective?"
- "Analyze shipping carrier performance"

See [`examples/example_queries.sql`](examples/example_queries.sql) for 25+ pre-written SQL queries.

## 📚 Documentation

- **[Agent Documentation](docs/AGENT_README.md)** - Complete Text-to-SQL agent guide
- **[Database Documentation](docs/DATABASE.md)** - Database schema and structure
- **[API Reference](#api-reference)** - Class and method documentation

## 🏗️ Architecture

### Components

1. **SQLiteQueryExecutor** (`sql_query_tool.py`)
   - Type-safe SQL execution with Pydantic
   - Input validation and error handling
   - Performance tracking and result formatting

2. **TextToSQLAgent** (`text_to_sql_agent.py`)
   - Natural language to SQL conversion using Gemini API
   - Schema-aware prompt engineering
   - Automatic SQL extraction and validation

3. **Interactive CLI** (`scripts/sql_chat.py`)
   - User-friendly command-line interface
   - Command support and help system
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
Validated Results (Pydantic Models)
    ↓
Formatted Output
```

## 🔑 API Reference

### Pydantic Models

**SQLQueryRequest**
```python
class SQLQueryRequest(BaseModel):
    query: str                          # SQL query to execute
    parameters: Optional[tuple | dict]  # Query parameters
    database_path: str                  # Path to database
    fetch_all: bool = True             # Fetch all results
```

**QueryResult**
```python
class QueryResult(BaseModel):
    success: bool                       # Execution status
    data: Optional[List[Dict]]          # Query results
    rows_affected: Optional[int]        # Rows modified
    columns: Optional[List[str]]        # Column names
    execution_time_ms: Optional[float]  # Execution time
    query_type: Optional[QueryType]     # Type of query
    error_message: Optional[str]        # Error details
```

**TextToSQLRequest**
```python
class TextToSQLRequest(BaseModel):
    question: str                       # Natural language question
    database_path: str                  # Database path
    include_explanation: bool = True    # Include SQL explanation
```

**TextToSQLResponse**
```python
class TextToSQLResponse(BaseModel):
    success: bool                       # Operation status
    question: str                       # Original question
    generated_sql: Optional[str]        # Generated SQL
    explanation: Optional[str]          # SQL explanation
    query_result: Optional[QueryResult] # Execution results
    error_message: Optional[str]        # Error details
```

## 🧪 Testing

Run the demo to test without an API key:
```bash
python scripts/demo.py
```

Run the test suite (requires API key):
```bash
python scripts/test.py
```

## 🛠️ Configuration

### Environment Variables

```bash
# Required for Text-to-SQL agent
export GEMINI_API_KEY='your-api-key-here'
```

### Custom Database

```python
agent = TextToSQLAgent(database_path="/path/to/your/database.db")
```

### Different Gemini Model

```python
agent = TextToSQLAgent(
    database_path="data/ecommerce.db",
    model_name="gemini-1.5-pro"  # or "gemini-2.0-flash-exp"
)
```

## 🎓 Database Information

The included e-commerce database (`data/ecommerce.db`) contains:

- **15 tables** with realistic relationships
- **Thousands of records** of test data
- **2-3 years** of historical transactions
- **Realistic data** generated with Faker

**Key Tables:**
- Customers (2,000 records)
- Products (500 records)
- Orders (3,000 records)
- Employees (150 records)
- And more...

See [docs/DATABASE.md](docs/DATABASE.md) for complete schema documentation.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini API** for powerful AI capabilities
- **Pydantic** for robust data validation
- **SQLite** for the embedded database engine
- **Faker** for realistic test data generation

## 📧 Support

- 📖 [Documentation](docs/)
- 🐛 [Report Issues](https://github.com/yourusername/sql_agent/issues)
- 💬 [Discussions](https://github.com/yourusername/sql_agent/discussions)

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

<div align="center">

**Built with ❤️ using Python, Pydantic, and Google Gemini**

</div>
