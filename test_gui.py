#!/usr/bin/env python3

"""
Simple test script to verify the GUI works before building the full app.
Run this to test the interface without building the full package.
"""

import sys
import os

# Add current directory to path so we can import organize_videos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from video_organizer_gui import main
    print("✅ GUI module imported successfully")
    print("Starting GUI...")
    main()
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have installed the requirements with pipenv:")
    print("  pipenv install")
    print("  pipenv run python test_gui.py")
except Exception as e:
    print(f"❌ Error running GUI: {e}") 