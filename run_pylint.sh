#!/bin/bash

# This script runs pylint checks with severity-based output

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure we're in the project root directory
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set PYTHONPATH
export PYTHONPATH=src:$SCRIPT_DIR
echo "Using PYTHONPATH: $PYTHONPATH"

# Extract disabled warnings from .pylintrc
DISABLED_CHECKS=$(grep -oP '^disable=\K.*' .pylintrc | tr '\n' ',' | sed 's/,$//')
echo "Applying disabled warnings from .pylintrc"

# Find Python files to analyze
PYTHON_FILES=$(find ./src -name "*.py" | xargs)
if [ -z "$PYTHON_FILES" ]; then
    echo "No Python files found to analyze!"
    exit 0
fi

echo -e "\n======================================================================"
echo "                  FULL PYLINT OUTPUT                            "
echo "======================================================================"
PYTHONPATH=src pylint --rcfile=.pylintrc $PYTHON_FILES || echo "Pylint check completed with issues"
echo -e "\n"

# 1. Check for critical errors
echo -e "======================================================================"
echo "                  CRITICAL ERRORS (E)                            "
echo "                These will block merging                         "
echo "======================================================================"
CRITICAL_OUTPUT=$(PYTHONPATH=src pylint --rcfile=.pylintrc --disable=C,W,R,I --enable=E --msg-template="{path}:{line}:{column}: [{msg_id}({symbol}), {category}] {msg}" $PYTHON_FILES 2>&1)
CRITICAL_ERRORS=$(echo "$CRITICAL_OUTPUT" | grep -E "^\./|^src/" || echo "")

if [ -n "$CRITICAL_ERRORS" ]; then
    echo -e "\033[31m$CRITICAL_ERRORS\033[0m"  # Red
    HAS_CRITICAL_ERRORS=1
else
    echo -e "\033[32mNo critical errors found.\033[0m"  # Green
    HAS_CRITICAL_ERRORS=0
fi

# 2. Check for warnings
echo -e "\n======================================================================"
echo "                  WARNINGS (W)                                  "
echo "======================================================================"
WARNINGS_OUTPUT=$(PYTHONPATH=src pylint --rcfile=.pylintrc --disable=C,E,R,I --enable=W --msg-template="{path}:{line}:{column}: [{msg_id}({symbol}), {category}] {msg}" $PYTHON_FILES 2>&1)
WARNINGS=$(echo "$WARNINGS_OUTPUT" | grep -E "^\./|^src/" || echo "")

if [ -n "$WARNINGS" ]; then
    echo -e "\033[33m$WARNINGS\033[0m"  # Yellow
else
    echo -e "\033[32mNo warnings found.\033[0m"  # Green
fi

# 3. Check for refactoring suggestions
echo -e "\n======================================================================"
echo "                  REFACTORING SUGGESTIONS (R)                    "
echo "======================================================================"
REFACTORING_OUTPUT=$(PYTHONPATH=src pylint --rcfile=.pylintrc --disable=C,E,W,I --enable=R --msg-template="{path}:{line}:{column}: [{msg_id}({symbol}), {category}] {msg}" $PYTHON_FILES 2>&1)
REFACTORING=$(echo "$REFACTORING_OUTPUT" | grep -E "^\./|^src/" || echo "")

if [ -n "$REFACTORING" ]; then
    echo -e "\033[36m$REFACTORING\033[0m"  # Cyan
else
    echo -e "\033[32mNo refactoring suggestions found.\033[0m"  # Green
fi

# 4. Check for convention violations
echo -e "\n======================================================================"
echo "                  CONVENTION ISSUES (C)                         "
echo "======================================================================"
CONVENTIONS_OUTPUT=$(PYTHONPATH=src pylint --rcfile=.pylintrc --disable=E,W,R,I --enable=C --msg-template="{path}:{line}:{column}: [{msg_id}({symbol}), {category}] {msg}" $PYTHON_FILES 2>&1)
CONVENTIONS=$(echo "$CONVENTIONS_OUTPUT" | grep -E "^\./|^src/" || echo "")

if [ -n "$CONVENTIONS" ]; then
    echo -e "\033[35m$CONVENTIONS\033[0m"  # Magenta
else
    echo -e "\033[32mNo convention issues found.\033[0m"  # Green
fi

# 5. Summary
echo -e "\n======================================================================"
echo "                         SUMMARY                                "
echo "======================================================================"

# Get the final score
SCORE=$(PYTHONPATH=src pylint --rcfile=.pylintrc $PYTHON_FILES 2>&1 | grep "Your code has been rated" || echo "")
if [ -n "$SCORE" ]; then
    echo "$SCORE"
else
    echo "Unable to calculate score"
fi

# Exit with error if there are critical errors
if [ "$HAS_CRITICAL_ERRORS" -eq 1 ]; then
    echo -e "\n\033[31mCritical errors found! Please fix them before proceeding.\033[0m"
    exit 1
else
    echo -e "\n\033[32mNo critical errors found. All checks passed!\033[0m"
    exit 0
fi
