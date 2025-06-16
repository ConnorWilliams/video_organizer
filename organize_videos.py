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
SOURCE_DIR = "/Volumes/Connor SSD/Skydiving"
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.MP4', '.MOV'}  # Add more if needed
JUMP_TIME_THRESHOLD = timedelta(minutes=20)  # Videos within this time are considered same jump
QUICK_HASH_SIZE = 1024 * 1024  # Read first 1MB for quick comparison

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
    1. GoPro creation_time from metadata
    2. GoPro timecode from metadata
    3. File creation time
    4. File modification time
    """
    try:
        creation_timestamp = os.path.getctime(video_path)
        return datetime.fromtimestamp(creation_timestamp)
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
    # Get all video files in the directory
    video_files = []
    for ext in VIDEO_EXTENSIONS:
        video_files.extend([(f, get_video_date(f)) for f in directory.glob(f"*{ext}")])
    
    # Group videos by time
    video_groups = group_videos_by_time(video_files)
    
    # Rename videos in each group
    for jump_num, group in enumerate(video_groups, 1):
        # Sort videos within the group by time
        group.sort(key=lambda x: x[1])
        
        for video_num, (video_path, video_time) in enumerate(group, 1):
            # Create new filename
            time_str = video_time.strftime("%H-%M")
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

def organize_videos():
    """Main function to organize videos by date."""
    source_path = Path(SOURCE_DIR)
    if not source_path.exists():
        logger.error(f"Source directory {SOURCE_DIR} does not exist!")
        return

    # Get all video files in top-level directory only
    video_files = []
    for ext in VIDEO_EXTENSIONS:
        video_files.extend(source_path.glob(f"*{ext}"))

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

            logger.info(f"\nProcessing video: {video_path.name}")
            
            video_date = get_video_date(video_path)
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
                logger.info(f"Processing directory: {date_dir}")
                rename_videos_in_directory(date_dir)

if __name__ == "__main__":
    organize_videos() 