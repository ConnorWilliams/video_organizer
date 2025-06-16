#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate pipenv and run the script
cd "$SCRIPT_DIR"

# Use full path to fswatch and pipenv
/opt/homebrew/bin/fswatch -o --exclude "organized" "/Volumes/Connor SSD/Skydiving" | while read; do
    echo "Changes detected, waiting 5 seconds for file operations to complete..."
    sleep 5
    echo "Running organizer..."
    # Use the full path to pipenv and ensure we're in the right directory
    export PATH="/opt/homebrew/bin:$PATH"
    export PIPENV_PIPFILE="$SCRIPT_DIR/Pipfile"
    /opt/homebrew/bin/pipenv run python organize_videos.py
    echo "Organizer completed."
    echo ""
done 