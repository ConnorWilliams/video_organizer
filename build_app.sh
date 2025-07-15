#!/bin/bash

echo "Building Skydiving Video Organizer macOS App..."

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This script is designed for macOS only."
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

# Check if pipenv is installed
if ! command -v pipenv &> /dev/null; then
    echo "Error: pipenv is not installed."
    echo "Install it with: pip3 install pipenv"
    exit 1
fi

echo "Installing dependencies with pipenv..."
pipenv install

echo "Building app with PyInstaller..."
pipenv run pyinstaller video_organizer.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "Your app is located at:"
    echo "  dist/Skydiving Video Organizer.app"
    echo ""
    echo "To install the app:"
    echo "  1. Drag 'Skydiving Video Organizer.app' to your Applications folder"
    echo "  2. Right-click the app and select 'Open' (first time only)"
    echo ""
    echo "To distribute the app:"
    echo "  - You can zip the .app folder and share it"
    echo "  - Or create a DMG installer for professional distribution"
    echo ""
else
    echo "❌ Build failed!"
    exit 1
fi 