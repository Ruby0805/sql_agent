# Contributing to SQL Agent

Thank you for your interest in contributing to SQL Agent! This document provides guidelines and instructions for contributing.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/sql_agent.git
   cd sql_agent
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```
4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📂 Project Structure

```
sql_agent/
├── src/sql_agent/          # Main package code
├── scripts/                # Executable scripts
├── examples/               # Usage examples
├── data/                   # Database files
└── docs/                   # Documentation
```

## 🔧 Development Setup

### Prerequisites

- Python 3.9+
- SQLite 3
- Gemini API key (for testing Text-to-SQL features)

### Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Set API key for testing
export GEMINI_API_KEY='your-test-api-key'
```

## 📝 Code Style

- **PEP 8**: Follow Python style guide
- **Type Hints**: Use type annotations for all functions
- **Docstrings**: Write clear docstrings for all public methods
- **Pydantic Models**: Use Pydantic for all data validation

### Example

```python
from typing import List, Optional
from pydantic import BaseModel, Field

class ExampleModel(BaseModel):
    """
    Example Pydantic model with proper documentation

    Attributes:
        name: The name field with validation
        values: Optional list of integers
    """
    name: str = Field(..., min_length=1, description="Name field")
    values: Optional[List[int]] = Field(default=None, description="List of values")

def process_data(model: ExampleModel) -> dict:
    """
    Process the data from the model

    Args:
        model: ExampleModel instance with data to process

    Returns:
        Dictionary with processed results
    """
    return {"name": model.name, "count": len(model.values or [])}
```

## 🧪 Testing

### Running Tests

```bash
# Run the demo (no API key needed)
python scripts/demo.py

# Run test with API key
python scripts/test.py

# Run example queries
python examples/run_first_query.py
```

### Adding Tests

When adding new features, include tests that demonstrate:
- Expected behavior
- Error handling
- Edge cases

## 📋 Pull Request Process

1. **Update Documentation**
   - Update README.md if adding new features
   - Add docstrings to new functions/classes
   - Update relevant docs in `docs/`

2. **Test Your Changes**
   - Ensure all existing tests pass
   - Add tests for new functionality
   - Test with the demo script

3. **Commit Guidelines**
   - Use clear, descriptive commit messages
   - Reference issue numbers when applicable
   - Keep commits focused and atomic

   ```bash
   git commit -m "Add feature: natural language date parsing"
   git commit -m "Fix: handle NULL values in query results"
   ```

4. **Submit Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Include screenshots/examples if applicable

## 🐛 Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Minimal steps to reproduce the issue
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: Python version, OS, etc.
- **Error Messages**: Full error traceback if applicable

### Example Bug Report

```markdown
**Bug**: SQL generation fails for complex JOIN queries

**Steps to Reproduce**:
1. Ask question: "Show orders with customer and product details"
2. Agent generates invalid SQL
3. Error: "no such column"

**Expected**: Valid SQL with proper JOIN syntax
**Actual**: Missing table alias in WHERE clause

**Environment**: Python 3.10, macOS, Gemini 2.0 Flash

**Error**:
```
sqlite3.OperationalError: no such column: customer_id
```
```

## 💡 Feature Requests

We welcome feature requests! Please:

1. **Check existing issues** to avoid duplicates
2. **Describe the feature** clearly
3. **Explain the use case** - why is it needed?
4. **Provide examples** of how it would work

## 🎯 Areas for Contribution

### High Priority

- **More Database Support**: Add PostgreSQL, MySQL support
- **Query Optimization**: Suggest indexes and optimizations
- **Result Visualization**: Add charts and graphs
- **Caching**: Cache frequently asked questions

### Medium Priority

- **Multi-language Support**: Support queries in other languages
- **Query History**: Save and replay previous queries
- **Export Results**: CSV, JSON, Excel export
- **Web Interface**: Browser-based UI

### Good First Issues

- **Documentation**: Improve examples and guides
- **Error Messages**: Better error messages
- **Example Queries**: Add more example questions
- **Tests**: Expand test coverage

## 📖 Documentation

### Adding Documentation

- **README.md**: Main project documentation
- **docs/AGENT_README.md**: Agent-specific documentation
- **docs/DATABASE.md**: Database schema documentation
- **Code Comments**: Inline comments for complex logic
- **Docstrings**: All public functions and classes

### Documentation Style

- Clear and concise
- Include examples
- Update table of contents
- Use proper markdown formatting

## 🤝 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Unprofessional conduct

## 📧 Getting Help

- **Questions**: Open a discussion
- **Bugs**: Open an issue
- **Security**: Email maintainers directly

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Mentioned in README.md acknowledgments

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to SQL Agent! 🎉
