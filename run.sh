#!/usr/bin/bash

source .env

Help() {
    echo "Usage: ./run.sh [option]"
    echo "Options:"
    echo "  start  - Start the application"
    echo "  format - Format the code"
    echo "  initdb - Initialize the database"
}

#!/bin/bash

RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m"
ScriptLog() {
    echo -e "${YELLOW}$1${NC}"
}
ScriptWarn() {
    echo -e "${RED}$1${NC}"
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
    initdb)
        ScriptLog "Removing existing database..."
        ScriptWarn "WARNING: This will delete all data in the database[y/N]"
        read -r response
        if [ "$response" != "y" ]; then
            ScriptLog "Aborting..."
            exit 0
        fi
        rm -f database.db
        ScriptLog "Initializing database..."
        poetry run python scripts/00_init_users.py
        ;;
    *)
        Help
        ;;
esac


