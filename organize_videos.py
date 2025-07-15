#!/usr/bin/env python3

import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
from typing import Set, Dict, Tuple, List
import logging
import sys
import json

# Configure logging to use stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout  # Use stdout instead of stderr
)
logger = logging.getLogger(__name__)

# Constants
VERSION = "1.0.0"
SOURCE_DIR = ""  # Will be set by GUI or command line argument
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.MP4', '.MOV'}  # Add more if needed
JUMP_TIME_THRESHOLD = timedelta(minutes=20)  # Videos within this time are considered same jump
QUICK_HASH_SIZE = 1024 * 1024  # Read first 1MB for quick comparison
PRESERVE_NAMES = True  # Whether to preserve original names in parentheses

def get_quick_file_signature(file_path: Path) -> Tuple[int, bytes]:
    """Get file size and first 1MB of content for quick comparison."""
    try:
        size = os.path.getsize(file_path)
        with open(file_path, 'rb') as f:
            header = f.read(QUICK_HASH_SIZE)
        return size, header
    except Exception as e:
        logger.error(f"Error getting file signature for {file_path}: {e}")
        return 0, b''

def get_existing_files(target_dir: Path) -> Dict[Tuple[int, bytes], Path]:
    """Get a dictionary of existing files and their quick signatures in the target directory."""
    existing_files = {}
    if target_dir.exists():
        for file in target_dir.rglob("*"):
            if file.is_file():
                signature = get_quick_file_signature(file)
                existing_files[signature] = file
    return existing_files

def get_video_date(video_path: Path) -> datetime:
    """
    Get the creation date of a video file.
    Tries multiple sources in order of reliability:
    1. File birth time (Finder creation date)
    2. File modification time
    """
    try:
        # Get file stats
        stat_info = os.stat(video_path)
        
        # On macOS, st_birthtime contains the birth time (Finder creation date)
        if hasattr(stat_info, 'st_birthtime'):
            birth_timestamp = stat_info.st_birthtime
            birth_date = datetime.fromtimestamp(birth_timestamp)
        else:
            # Fallback to creation time if birth time not available
            birth_timestamp = stat_info.st_ctime
            birth_date = datetime.fromtimestamp(birth_timestamp)
        
        modification_timestamp = stat_info.st_mtime
        modification_date = datetime.fromtimestamp(modification_timestamp)
        
        logger.debug(f"File: {video_path.name}")
        logger.debug(f"  Birth time (Finder creation): {birth_date.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.debug(f"  Modification time: {modification_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Use the earlier of the two times (likely the actual recording time)
        if birth_date < modification_date:
            logger.debug(f"  Using birth time: {birth_date.strftime('%Y-%m-%d %H:%M:%S')}")
            return birth_date
        else:
            logger.debug(f"  Using modification time: {modification_date.strftime('%Y-%m-%d %H:%M:%S')}")
            return modification_date
            
    except Exception as e:
        logger.error(f"Error getting date for {video_path}: {e}")
        # Fallback to modification time
        modification_timestamp = os.path.getmtime(video_path)
        return datetime.fromtimestamp(modification_timestamp)

def group_videos_by_time(video_files: List[Tuple[Path, datetime]]) -> List[List[Tuple[Path, datetime]]]:
    """
    Group videos that were recorded within JUMP_TIME_THRESHOLD of each other.
    Returns a list of groups, where each group is a list of (path, datetime) tuples.
    """
    if not video_files:
        return []
    
    # Sort videos by time
    sorted_videos = sorted(video_files, key=lambda x: x[1])
    groups = []
    current_group = [sorted_videos[0]]
    
    for video in sorted_videos[1:]:
        if video[1] - current_group[-1][1] <= JUMP_TIME_THRESHOLD:
            current_group.append(video)
        else:
            groups.append(current_group)
            current_group = [video]
    
    if current_group:
        groups.append(current_group)
    
    return groups



def rename_videos_in_directory(directory: Path):
    """Rename videos in a directory based on their recording times."""
    # Get all video files in the directory, filtering out invalid files
    video_files = []
    for ext in VIDEO_EXTENSIONS:
        video_files.extend([(f, get_video_date(f)) for f in directory.glob(f"*{ext}") if is_valid_video_file(f)])
    
    # Group videos by time
    video_groups = group_videos_by_time(video_files)
    
    # Rename videos in each group
    for jump_num, group in enumerate(video_groups, 1):
        # Sort videos within the group by time
        group.sort(key=lambda x: x[1])
        
        for video_num, (video_path, video_time) in enumerate(group, 1):
            # Create new filename
            time_str = video_time.strftime("%H-%M")
            
            if PRESERVE_NAMES:
                # Extract original name - if already renamed, get the name from parentheses
                current_name = video_path.stem  # filename without extension
                
                # Check if this is already in our format and extract original name from parentheses
                if current_name.startswith("Jump ") and " - Video " in current_name and " (" in current_name and current_name.endswith(")"):
                    # Extract the original name from the parentheses at the end
                    original_name = current_name.split(" (")[-1].rstrip(")")
                else:
                    # This is the first time renaming, use current name as original
                    original_name = current_name
                
                new_name = f"Jump {jump_num} - Video {video_num} - {time_str} ({original_name}){video_path.suffix}"
            else:
                # Simple naming without preserving original names
                new_name = f"Jump {jump_num} - Video {video_num} - {time_str}{video_path.suffix}"
            
            new_path = video_path.parent / new_name
            
            try:
                if new_path.exists():
                    logger.debug(f"Target file already exists: {new_path}")
                    continue
                    
                video_path.rename(new_path)
                logger.info(f"Renamed {video_path.name} to {new_name}")
            except Exception as e:
                logger.error(f"Error renaming {video_path.name}: {e}")

def is_in_dated_folder(path: Path) -> bool:
    """
    Check if a file is already in a folder that matches the date format YYYY-MM-DD.
    """
    try:
        # Check if parent directory name matches date format
        parent_name = path.parent.name
        datetime.strptime(parent_name, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def check_and_fix_video_date(video_path: Path) -> datetime:
    """
    Check if video date is potentially incorrect (early 2016) and allow manual correction.
    Returns the corrected or original date.
    """
    video_date = get_video_date(video_path)
    
    # Check if date is from early 2016 (GoPro default)
    if video_date.year == 2016 and video_date.month <= 3:
        print(f"\nPotentially incorrect date detected for {video_path.name}")
        print(f"Current date: {video_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        while True:
            try:
                date_str = input("Please enter the correct date (YYYY-MM-DD): ")
                time_str = input("Please enter the correct time (HH:MM:SS): ")
                
                # Combine date and time
                datetime_str = f"{date_str} {time_str}"
                corrected_date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                
                # Update file timestamps
                timestamp = corrected_date.timestamp()
                os.utime(video_path, (timestamp, timestamp))
                
                print(f"Updated date for {video_path.name} to {corrected_date}")
                return corrected_date
                
            except ValueError:
                print("Invalid date/time format. Please use YYYY-MM-DD and HH:MM:SS format.")
                continue
    
    return video_date

def is_valid_video_file(file_path: Path) -> bool:
    """
    Check if a file is a valid video file to process.
    Excludes macOS metadata files and other hidden files.
    """
    # Skip files starting with ._ (macOS metadata files)
    if file_path.name.startswith('._'):
        return False
    # Skip hidden files
    if file_path.name.startswith('.'):
        return False
    return True

def organize_videos():
    """Main function to organize videos by date."""
    if not SOURCE_DIR:
        logger.error("Source directory not set! Please set SOURCE_DIR or use the GUI.")
        return
        
    source_path = Path(SOURCE_DIR)
    if not source_path.exists():
        logger.error(f"Source directory {SOURCE_DIR} does not exist!")
        return

    # Get all video files in top-level directory only
    video_files = []
    for ext in VIDEO_EXTENSIONS:
        video_files.extend([f for f in source_path.glob(f"*{ext}") if is_valid_video_file(f)])

    if not video_files:
        logger.info("No video files found in the source directory.")
        return

    # Process each video file
    for video_path in video_files:
        try:
            # Skip if already in a dated folder
            if is_in_dated_folder(video_path):
                logger.info(f"Skipping {video_path.name} - already in a dated folder")
                continue

            logger.info(f"Processing video: {video_path.name}")
            
            # Check and potentially fix video date
            video_date = check_and_fix_video_date(video_path)
            date_str = video_date.strftime("%Y-%m-%d")
            
            # Create target directory
            target_dir = source_path / "organized" / date_str
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Get existing files in target directory
            existing_files = get_existing_files(target_dir)
            
            # Get quick signature of current video
            current_signature = get_quick_file_signature(video_path)
            
            # Check if file already exists
            if current_signature in existing_files:
                logger.debug(f"Skipping {video_path.name} - already exists in {date_str}")
                continue
            
            # Move file to target directory
            target_path = target_dir / video_path.name
            if target_path.exists():
                logger.debug(f"Target file already exists: {target_path}")
                continue
                
            shutil.move(str(video_path), str(target_path))
            logger.info(f"Moved {video_path.name} to {date_str}")
            
        except Exception as e:
            logger.error(f"Error processing {video_path}: {e}")
    
    # Process each date directory to rename videos
    organized_dir = source_path / "organized"
    if organized_dir.exists():
        for date_dir in organized_dir.iterdir():
            if date_dir.is_dir():
                logger.debug(f"Processing directory: {date_dir}")
                rename_videos_in_directory(date_dir)

if __name__ == "__main__":
    organize_videos() 