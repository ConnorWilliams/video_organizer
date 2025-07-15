# Skydiving Video Organizer - Desktop App

A modern macOS desktop application for automatically organizing skydiving videos from GoPro and Insta360 cameras.

## Features

- **Modern GUI Interface**: Clean, intuitive interface built with PyQt6
- **Real-time Monitoring**: Automatically detect and organize new videos
- **Configurable Settings**: Customize video extensions and jump time thresholds
- **Progress Tracking**: Real-time progress updates and detailed logging
- **File Status View**: See all organized videos in a searchable table
- **Background Processing**: Non-blocking video organization
- **Native macOS App**: Properly packaged as a .app bundle

## Screenshots

The app features:
- Source directory selection with browse functionality
- Configurable video extensions and jump time thresholds
- Real-time log output with auto-scrolling
- Status table showing all organized videos
- Progress indicators and status messages

## Installation

### Option 1: Build from Source (Recommended)

1. **Prerequisites**:
   ```bash
   # Make sure you have Python 3.8+ installed
   python3 --version
   
   # Install pipenv if not already installed
   pip3 install pipenv
   ```

2. **Clone or download the project**:
   ```bash
   cd /path/to/your/project
   ```

3. **Build the app**:
   ```bash
   # Make the build script executable
   chmod +x build_app.sh
   
   # Run the build script
   ./build_app.sh
   ```

4. **Install the app**:
   - Navigate to the `dist` folder
   - Drag `Skydiving Video Organizer.app` to your Applications folder
   - Right-click the app and select "Open" (first time only, to bypass Gatekeeper)

### Option 2: Test the GUI First

Before building the full app, you can test the GUI:

```bash
# Install dependencies with pipenv
pipenv install

# Test the GUI
pipenv run python test_gui.py
```

## Usage

### First Launch

1. **Open the app** from your Applications folder
2. **Select Source Directory**: Click "Browse..." to select the folder containing your skydiving videos
3. **Configure Settings** (optional):
   - Video Extensions: Add or remove file extensions to process
   - Jump Time Threshold: Set how many minutes apart videos should be grouped as the same jump

### Organizing Videos

#### Manual Organization
1. Click "Organize Videos" to process all videos in the source directory
2. Watch the progress in the log output
3. Check the "Status" tab to see organized files

#### Automatic Monitoring
1. Click "Start Monitoring" to enable automatic detection
2. The app will check for new videos every 30 seconds
3. New videos will be automatically organized
4. Click "Stop Monitoring" to disable automatic processing

### Understanding the Interface

#### Main Tab
- **Source Directory**: Shows the currently selected folder for video processing
- **Configuration**: Adjust video extensions and jump time thresholds
- **Action Buttons**: 
  - "Organize Videos": Process all videos manually
  - "Start/Stop Monitoring": Toggle automatic monitoring
- **Log Output**: Real-time status updates and error messages

#### Status Tab
- **File Table**: Shows all organized videos with:
  - File name
  - Status (Organized)
  - Date folder
  - File size
- **Refresh Button**: Update the status table

## File Organization

Videos are organized as follows:
```
Source Directory/
└── organized/
    └── YYYY-MM-DD/
        ├── Jump 1 - Video 1 - HH-MM.mp4
        ├── Jump 1 - Video 2 - HH-MM.mp4
        ├── Jump 2 - Video 1 - HH-MM.mp4
        └── ...
```

## Troubleshooting

### Common Issues

1. **"App can't be opened because it's from an unidentified developer"**
   - Right-click the app and select "Open"
   - Click "Open" in the dialog that appears
   - This only needs to be done once

2. **Build fails with PyInstaller errors**
   - Make sure you have the latest version of PyInstaller
   - Try: `pipenv install --upgrade pyinstaller`
   - Check that all dependencies are installed: `pipenv install`

3. **GUI doesn't start**
   - Run `pipenv run python test_gui.py` to test the GUI directly
   - Check for missing dependencies
   - Ensure you're using Python 3.8 or later

4. **Videos not being organized**
   - Check the log output for error messages
   - Verify the source directory contains video files
   - Ensure video files have the correct extensions

### Log Files

The app logs all operations to the GUI. For debugging, you can also check:
- Console logs: Open Console.app and search for "Skydiving Video Organizer"
- System logs: Check System Preferences > Security & Privacy > Privacy > Full Disk Access

## Distribution

### Sharing the App

1. **Simple Distribution**:
   - Zip the `.app` folder and share it
   - Recipients can drag it to their Applications folder

2. **Professional Distribution**:
   - Create a DMG installer
   - Code sign the app (requires Apple Developer account)
   - Notarize the app for macOS Catalina+

### Creating a DMG Installer

```bash
# Install create-dmg if you have Homebrew
brew install create-dmg

# Create a DMG
create-dmg \
  --volname "Skydiving Video Organizer" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "Skydiving Video Organizer.app" 175 120 \
  --hide-extension "Skydiving Video Organizer.app" \
  --app-drop-link 425 120 \
  "Skydiving Video Organizer.dmg" \
  "dist/"
```

## Development

### Project Structure

```
video_organiser/
├── organize_videos.py          # Core video organization logic
├── video_organizer_gui.py      # PyQt6 GUI interface
├── video_organizer.spec        # PyInstaller configuration
├── Pipfile                     # pipenv dependencies
├── build_app.sh               # Build script
├── test_gui.py                # GUI test script
└── README_DESKTOP.md          # This file
```

### Modifying the App

1. **Change the GUI**: Edit `video_organizer_gui.py`
2. **Modify core logic**: Edit `organize_videos.py`
3. **Update dependencies**: Edit `Pipfile`
4. **Rebuild**: Run `./build_app.sh`

### Adding Features

The modular design makes it easy to add features:
- Add new configuration options in the GUI
- Extend the video processing logic
- Add new file formats or organization rules
- Implement additional monitoring options

## System Requirements

- **macOS**: 10.15 (Catalina) or later
- **Python**: 3.8 or later (for building)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB free space for the app

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the log output in the app
3. Test with the command-line version first
4. Check the original `organize_videos.py` script for reference 