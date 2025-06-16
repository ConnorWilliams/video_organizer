# Skydiving Video Organizer

This tool automatically organizes skydiving videos from GoPro and Insta360 cameras. It monitors a specified directory for new videos, organizes them by date, and groups them into jumps based on recording time.

## Features

- Automatically monitors for new videos
- Organizes videos into date-based folders
- Groups videos from the same jump (recorded within 20 minutes of each other)
- Prevents duplicate files using file hashing
- Runs automatically in the background
- Logs all operations for monitoring

## Prerequisites

- macOS
- Python 3.11 or later
- pipenv
- fswatch (installed via Homebrew)

## Installation

1. Install required tools:
```bash
# Install Homebrew if you haven't already
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install fswatch
brew install fswatch

# Install pipenv if you haven't already
pip install pipenv
```

2. Clone or download this repository:
```bash
cd /Users/connor/Skydiving
git clone <repository-url> video_organiser
cd video_organiser
```

3. Install Python dependencies:
```bash
pipenv install
```

4. Make the watch script executable:
```bash
chmod +x watch_videos.sh
```

5. Install the Launch Agent:
```bash
# Copy the Launch Agent configuration
cp com.skydiving.video-organizer.plist ~/Library/LaunchAgents/

# Load the Launch Agent
launchctl load ~/Library/LaunchAgents/com.skydiving.video-organizer.plist
```

## Usage

### Automatic Organization

Once installed, the tool will automatically:
1. Monitor `/Volumes/Connor SSD/Skydiving` for new videos
2. When new videos are detected:
   - Wait 5 seconds for file operations to complete
   - Create date-based folders (YYYY-MM-DD)
   - Group videos from the same jump (within 20 minutes)
   - Rename files with format: `Jump X - Video Y - HH-MM.ext`
   - Move files to appropriate folders

### Manual Organization

To manually organize videos:
```bash
cd /Users/connor/Skydiving/video_organiser
pipenv run python organize_videos.py
```

### Monitoring

- Check the logs for operation details:
  ```bash
  cat output.log  # Normal operation logs
  cat error.log   # Error logs
  ```

### Managing the Background Service

To stop the automatic monitoring:
```bash
launchctl unload ~/Library/LaunchAgents/com.skydiving.video-organizer.plist
```

To start it again:
```bash
launchctl load ~/Library/LaunchAgents/com.skydiving.video-organizer.plist
```

To check if the service is running:
```bash
launchctl list | grep video-organizer
```

### File Organization

Videos are organized as follows:
```
/Volumes/Connor SSD/Skydiving/
└── organized/
    └── YYYY-MM-DD/
        ├── Jump 1 - Video 1 - HH-MM.mp4
        ├── Jump 1 - Video 2 - HH-MM.mp4
        ├── Jump 2 - Video 1 - HH-MM.mp4
        └── ...
```

## Troubleshooting

1. If videos aren't being organized:
   - Check if the Launch Agent is running: `launchctl list | grep video-organizer`
   - Check the error log: `cat error.log`
   - Check the output log: `cat output.log`
   - Ensure the source directory exists and is accessible
   - Make sure your external drive is mounted at `/Volumes/Connor SSD/Skydiving`

2. If you need to modify the source directory:
   - Edit `organize_videos.py` and change the `SOURCE_DIR` constant
   - Restart the Launch Agent:
     ```bash
     launchctl unload ~/Library/LaunchAgents/com.skydiving.video-organizer.plist
     launchctl load ~/Library/LaunchAgents/com.skydiving.video-organizer.plist
     ```

3. If the script is running in a loop:
   - Stop the service: `launchctl unload ~/Library/LaunchAgents/com.skydiving.video-organizer.plist`
   - Check the logs for any errors
   - Restart the service: `launchctl load ~/Library/LaunchAgents/com.skydiving.video-organizer.plist`

## Uninstallation

To completely remove the tool:
```bash
# Stop and remove the Launch Agent
launchctl unload ~/Library/LaunchAgents/com.skydiving.video-organizer.plist
rm ~/Library/LaunchAgents/com.skydiving.video-organizer.plist

# Remove the tool directory
rm -rf /Users/connor/Skydiving/video_organiser
```

## Notes

- The script ignores the "organized" directory to prevent infinite loops
- There's a 5-second cooldown period after detecting changes to ensure all file operations are complete
- Videos are grouped into jumps if they were recorded within 20 minutes of each other
- The script uses file hashing to prevent duplicate files
- All operations are logged to `output.log` and `error.log` 