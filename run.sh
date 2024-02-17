#!/usr/bin/bash

source .env

Help() {
    echo "Usage: ./run.sh [option]"
    echo "Options:"
    echo "  start  - Start the application"
    echo "  format - Format the code"
}

#!/bin/bash

ScriptLog() {
    echo -e "\033[1;33m$1\033[0m"
}

case "$1" in
    start)
        ScriptLog "Starting server..."
        poetry run python app.py
        ;;
    format)
        ScriptLog "Formatting code..."
        poetry run black --line-length 120 .
        ScriptLog "Sorting imports..."
        poetry run isort .
        ;;
    *)
        Help
        ;;
esac


