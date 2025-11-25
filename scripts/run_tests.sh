#!/bin/bash

# Run tests for gaming platform models

echo "=== Running Gaming Platform Model Tests ==="
echo ""

# Check if pytest is installed
if ! python -m pytest --version &> /dev/null; then
    echo "Error: pytest is not installed"
    echo "Install with: pip install -r requirements.txt"
    exit 1
fi

# Run tests with coverage
echo "Running tests with coverage..."
python -m pytest tests/ -v --cov=models --cov-report=term-missing --cov-report=html

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "=== All Tests Passed! ==="
    echo ""
    echo "Coverage report generated in htmlcov/index.html"
else
    echo ""
    echo "=== Some Tests Failed ==="
    exit 1
fi