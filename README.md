# Skydiving Video Organizer

A desktop application for automatically organizing skydiving videos from GoPro, Insta360, and other action cameras. Organizes videos by date and groups them into jumps based on recording time.

## Features

- **🎯 Smart Video Organization**: Automatically organizes videos into date-based folders
- **🪂 Jump Detection**: Groups videos from the same jump (recorded within configurable time threshold)
- **📱 Modern GUI**: User-friendly interface with real-time progress monitoring
- **🔍 Duplicate Prevention**: Uses file hashing to prevent duplicate files
- **📝 Detailed Logging**: Comprehensive logging for monitoring and troubleshooting
- **⚙️ Configurable**: Customize video extensions, jump time thresholds, and naming preferences

- **💾 Name Preservation**: Option to preserve original video names

## Screenshots

*[Screenshots will be added here]*

## Download

### Latest Release
Download the latest version from [GitHub Releases](https://github.com/yourusername/skydiving-video-organizer/releases)

### System Requirements
- **macOS**: 10.15 (Catalina) or later
- **Windows**: Windows 10 or later (coming soon)
- **Storage**: At least 1GB free space for the application

## Quick Start

### Option 1: Download Pre-built App (Recommended)
1. Download the latest release from GitHub
2. Extract the ZIP file
3. Drag `Skydiving Video Organizer.app` to your Applications folder
4. Right-click the app and select "Open" (first time only)
5. Select your source directory and click "Organize Videos"

### Option 2: Build from Source
```bash
# Clone the repository
git clone https://github.com/yourusername/skydiving-video-organizer.git
cd skydiving-video-organizer

# Install dependencies
pip install pipenv
pipenv install

# Build the application
./build_app.sh
```

### Option 3: Command Line Only
```bash
# Clone the repository
git clone https://github.com/yourusername/skydiving-video-organizer.git
cd skydiving-video-organizer

# Install dependencies
pip install pipenv
pipenv install

# Run directly
pipenv run python organize_videos.py
```

## Usage

### GUI Application
1. **Launch the app** from your Applications folder
2. **Select source directory** containing your skydiving videos
3. **Configure settings**:
   - Video extensions (default: .mp4, .mov, .MP4, .MOV)
   - Jump time threshold (default: 20 minutes)
   - Preserve original names (optional)
4. **Click "Organize Videos"** to start processing
5. **Monitor progress** in the log output



## File Organization

Videos are organized into a structured hierarchy:

```
Source Directory/
└── organized/
    └── YYYY-MM-DD/
        ├── Jump 1 - Video 1 - HH-MM (original_name).mp4
        ├── Jump 1 - Video 2 - HH-MM (original_name).mp4
        ├── Jump 2 - Video 1 - HH-MM (original_name).mp4
        └── ...
```

### Naming Convention
- **Date folders**: `YYYY-MM-DD` format
- **Jump grouping**: Videos recorded within the time threshold are grouped as the same jump
- **Video numbering**: Sequential numbering within each jump
- **Time stamp**: Recording time in HH-MM format
- **Original name**: Preserved in parentheses (optional)

## Configuration

### Video Extensions
Supported formats: `.mp4`, `.mov`, `.MP4`, `.MOV`
Add more extensions in the GUI.

### Jump Time Threshold
Default: 20 minutes
Videos recorded within this time window are considered part of the same jump.

### Name Preservation
When enabled, original filenames are preserved in parentheses:
- `Jump 1 - Video 1 - 14-30 (GOPR1234).mp4`
- `Jump 1 - Video 1 - 14-30 (My awesome skydive).mp4`

When disabled, clean names are used:
- `Jump 1 - Video 1 - 14-30.mp4`

## Troubleshooting

### Common Issues

**App won't open on macOS:**
- Right-click the app and select "Open"
- Go to System Preferences > Security & Privacy and allow the app

**Videos not being organized:**
- Check that the source directory exists and contains video files
- Verify video file extensions are supported
- Check the log output for error messages

**Wrong dates detected:**
- The app uses file creation/modification times
- For GoPro files with incorrect timestamps, the app will prompt for manual correction

**Duplicate files:**
- The app uses file hashing to prevent duplicates
- Check the log for "already exists" messages

## Development

### Building from Source
```bash
# Install dependencies
pipenv install

# Run tests
pipenv run python test_gui.py

# Build application
./build_app.sh
```

### Project Structure
```
skydiving-video-organizer/
├── video_organizer_gui.py    # Main GUI application
├── organize_videos.py        # Core organization logic
├── build_app.sh             # Build script
├── video_organizer.spec     # PyInstaller specification
├── Pipfile                  # Python dependencies
└── README.md               # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/yourusername/skydiving-video-organizer/issues)
- **Discussions**: Join the conversation on [GitHub Discussions](https://github.com/yourusername/skydiving-video-organizer/discussions)

## Changelog

### v1.0.0
- Initial release
- GUI application with modern interface
- Automatic video organization by date
- Jump detection and grouping
- Configurable settings
- Name preservation option
- Comprehensive logging

---

**Made with ❤️ for the skydiving community** 