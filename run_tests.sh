#!/usr/bin/env bash

# Stop the script if anything fails
set -e

echo "Activating virtual environment..."
source venv/Scripts/activate

echo "Running pytest..."
pytest

# If pytest exits with 0, tests passed
echo "All tests passed!"
exit 0
