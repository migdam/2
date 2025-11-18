# Testing Guide

Comprehensive testing documentation for the Strategy Mapper application.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Writing Tests](#writing-tests)
- [CI/CD](#cicd)
- [Troubleshooting](#troubleshooting)

## Overview

The Strategy Mapper test suite includes:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test complete workflows and component interactions
- **Mocked OpenAI API**: Avoid real API calls during testing
- **Coverage Reporting**: Track code coverage metrics
- **CI/CD**: Automated testing via GitHub Actions

### Test Statistics

- **Total Test Files**: 4
- **Unit Tests**: 40+
- **Integration Tests**: 15+
- **Coverage Target**: 80%+

## Quick Start

### 1. Install Test Dependencies

```bash
cd strategy_mapper
pip install -r requirements-dev.txt
```

### 2. Run All Tests

```bash
./run_tests.sh
```

### 3. Run Specific Test Types

```bash
# Unit tests only
./run_tests.sh unit

# Integration tests only
./run_tests.sh integration

# Fast tests (exclude slow tests)
./run_tests.sh fast

# With coverage report
./run_tests.sh coverage
```

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests
│   ├── test_db.py          # Database layer tests
│   ├── test_ai.py          # AI layer tests
│   └── test_utils.py       # Utils layer tests
├── integration/             # Integration tests
│   └── test_workflow.py    # End-to-end workflow tests
└── fixtures/                # Test data and fixtures
```

### Test Markers

Tests are organized with pytest markers:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow-running tests
- `@pytest.mark.db` - Database tests
- `@pytest.mark.ai` - AI/OpenAI tests
- `@pytest.mark.utils` - Utility tests

## Running Tests

### Using the Test Runner Script

```bash
# Run all tests
./run_tests.sh all

# Run only unit tests
./run_tests.sh unit

# Run only integration tests
./run_tests.sh integration

# Run fast tests (exclude slow tests)
./run_tests.sh fast

# Run with coverage report
./run_tests.sh coverage

# Run CI suite
./run_tests.sh ci
```

### Using pytest Directly

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_db.py

# Run specific test class
pytest tests/unit/test_db.py::TestDatabase

# Run specific test
pytest tests/unit/test_db.py::TestDatabase::test_connect

# Run tests with specific marker
pytest -m unit
pytest -m "not slow"

# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run tests in parallel
pytest -n auto
```

## Test Coverage

### Generate Coverage Report

```bash
# HTML report
./run_tests.sh coverage
open htmlcov/index.html

# Terminal report
pytest --cov=. --cov-report=term-missing

# XML report (for CI)
pytest --cov=. --cov-report=xml
```

### Coverage Targets

- **Overall**: 80%+
- **Database Layer**: 90%+
- **AI Layer**: 85%+
- **Utils Layer**: 85%+

### View Coverage

After running coverage tests:

```bash
# Open HTML report
open htmlcov/index.html

# View in terminal
pytest --cov=. --cov-report=term-missing
```

## Writing Tests

### Unit Test Example

```python
import pytest
from ai.scorer import compute_similarity

@pytest.mark.unit
@pytest.mark.ai
class TestScorer:
    def test_compute_similarity(self, mock_embedding, sample_strategies):
        """Test computing similarity scores."""
        strategies_dicts = [
            {"id": s[0], "name": s[1], "description": s[2], "embedding": s[3]}
            for s in sample_strategies
        ]

        results = compute_similarity(mock_embedding, strategies_dicts)

        assert len(results) == 3
        assert all("strategy" in r for r in results)
        assert all("score" in r for r in results)
```

### Integration Test Example

```python
import pytest

@pytest.mark.integration
class TestFullWorkflow:
    def test_complete_analysis(self, patch_db_path, mock_openai_embedding):
        """Test complete workflow from strategy creation to analysis."""
        # Step 1: Create strategy
        insert_strategy("Innovation", "AI products", mock_embedding)

        # Step 2: Analyze text
        text_embedding = get_embedding("AI automation")

        # Step 3: Compute similarity
        strategies = fetch_strategies()
        similarities = compute_similarity(text_embedding, strategies)

        # Step 4: Verify results
        assert len(similarities) > 0
```

### Available Fixtures

See `tests/conftest.py` for all available fixtures:

- `temp_db` - Temporary test database
- `mock_embedding` - Mock embedding vector
- `mock_openai_embedding` - Mock OpenAI embedding API
- `mock_openai_chat` - Mock OpenAI chat API
- `sample_strategies` - Sample strategy data
- `sample_text` - Sample text for testing
- `sample_chunks` - Sample text chunks
- `patch_db_path` - Patch DB path to use temp database

### Best Practices

1. **Isolation**: Each test should be independent
2. **Mocking**: Mock external APIs (OpenAI)
3. **Fixtures**: Use fixtures for common test data
4. **Markers**: Use markers to categorize tests
5. **Assertions**: Clear, descriptive assertions
6. **Documentation**: Docstrings for all tests
7. **Cleanup**: Ensure proper cleanup in fixtures

## CI/CD

### GitHub Actions

Tests run automatically on:

- Push to `main`, `develop`, or `claude/*` branches
- Pull requests to `main` or `develop`

### Workflow Jobs

1. **Test Job**
   - Runs on Ubuntu and macOS
   - Tests Python 3.8, 3.9, 3.10, 3.11
   - Runs unit and integration tests
   - Uploads coverage to Codecov

2. **Lint Job**
   - Runs flake8, black, isort
   - Checks code formatting and style

3. **Security Job**
   - Runs safety and bandit
   - Checks for security vulnerabilities

### Required Secrets

Set in GitHub repository settings:

- `OPENAI_API_KEY` - OpenAI API key for testing

### Viewing CI Results

1. Go to GitHub repository
2. Click "Actions" tab
3. View workflow runs and results

## Troubleshooting

### Common Issues

#### Import Errors

```bash
# Ensure test dependencies are installed
pip install -r requirements-dev.txt
```

#### Database Conflicts

```bash
# Tests use temporary databases, but if issues persist:
rm -f strategy_mapper.db
rm -f test_*.db
```

#### OpenAI API Mocking Issues

Tests should NOT require real OpenAI API keys. If you see real API calls:

1. Check that `mock_openai_embedding` fixture is used
2. Ensure `conftest.py` is properly loaded
3. Verify pytest is finding fixtures

#### Coverage Not Generated

```bash
# Install coverage tools
pip install pytest-cov coverage

# Run with coverage explicitly
pytest --cov=. --cov-report=html
```

#### Tests Running Slowly

```bash
# Run fast tests only
./run_tests.sh fast

# Run in parallel
pip install pytest-xdist
pytest -n auto
```

### Debug Mode

Run tests with verbose output and print statements:

```bash
pytest -vv -s
```

### Test Specific Component

```bash
# Test only database
pytest tests/unit/test_db.py -v

# Test only AI components
pytest -m ai -v

# Test specific function
pytest tests/unit/test_ai.py::TestEmbeddings::test_get_embedding_returns_vector -v
```

## Advanced Usage

### Custom Markers

Define custom markers in `pytest.ini`:

```ini
markers =
    slow: Slow running tests
    requires_api: Tests that require real API
```

Use in tests:

```python
@pytest.mark.slow
def test_large_document():
    # Slow test
    pass
```

### Parametrized Tests

Test multiple scenarios:

```python
@pytest.mark.parametrize("text,expected_chunks", [
    ("Short text", 1),
    ("Para 1\n\nPara 2", 2),
    ("Para 1\n\nPara 2\n\nPara 3", 3),
])
def test_chunking(text, expected_chunks):
    chunks = agentic_chunk(text)
    assert len(chunks) == expected_chunks
```

### Fixtures with Scope

```python
@pytest.fixture(scope="session")
def shared_resource():
    # Created once per test session
    return expensive_setup()

@pytest.fixture(scope="function")
def per_test_resource():
    # Created for each test
    return quick_setup()
```

## Continuous Improvement

### Adding New Tests

1. Identify untested code via coverage report
2. Write test in appropriate directory
3. Use existing fixtures when possible
4. Add markers for categorization
5. Run tests to verify
6. Check coverage improvement

### Maintaining Tests

- Review tests when code changes
- Update mocks when APIs change
- Keep fixtures up to date
- Monitor CI/CD results
- Address flaky tests immediately

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [GitHub Actions](https://docs.github.com/en/actions)

## Support

For testing issues:

1. Check this documentation
2. Review test output carefully
3. Check GitHub Actions logs
4. Review `conftest.py` for available fixtures
5. Create an issue with detailed error information

---

**Remember**: Good tests lead to confident deployments! 🚀
