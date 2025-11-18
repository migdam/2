#!/bin/bash

echo "🧪 Strategy Mapper Test Suite"
echo "=============================="
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Installing test dependencies..."
    pip install -r requirements-dev.txt
fi

# Parse command line arguments
TEST_TYPE="${1:-all}"
VERBOSE="${2:-}"

echo "📋 Running tests: $TEST_TYPE"
echo ""

case $TEST_TYPE in
    "unit")
        echo "🔬 Running unit tests only..."
        pytest tests/unit/ -v $VERBOSE
        ;;
    "integration")
        echo "🔗 Running integration tests only..."
        pytest tests/integration/ -v $VERBOSE
        ;;
    "fast")
        echo "⚡ Running fast tests (excluding slow tests)..."
        pytest -m "not slow" -v $VERBOSE
        ;;
    "coverage")
        echo "📊 Running tests with coverage report..."
        pytest --cov=. --cov-report=html --cov-report=term-missing
        echo ""
        echo "✅ Coverage report generated in htmlcov/index.html"
        ;;
    "ci")
        echo "🤖 Running CI test suite..."
        pytest -v --cov=. --cov-report=xml --cov-report=term-missing
        ;;
    "all")
        echo "🚀 Running all tests..."
        pytest -v $VERBOSE
        ;;
    *)
        echo "❌ Unknown test type: $TEST_TYPE"
        echo ""
        echo "Usage: ./run_tests.sh [TEST_TYPE] [VERBOSE]"
        echo ""
        echo "TEST_TYPE options:"
        echo "  all          - Run all tests (default)"
        echo "  unit         - Run unit tests only"
        echo "  integration  - Run integration tests only"
        echo "  fast         - Run fast tests (exclude slow tests)"
        echo "  coverage     - Run with coverage report"
        echo "  ci           - Run CI test suite"
        echo ""
        echo "VERBOSE options:"
        echo "  -vv          - Very verbose output"
        echo "  -s           - Show print statements"
        exit 1
        ;;
esac

TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed. Exit code: $TEST_EXIT_CODE"
fi

exit $TEST_EXIT_CODE
