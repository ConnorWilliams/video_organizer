# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Windows support (coming soon)

## [1.0.0] - 2024-12-30

### Added
- Initial release of Skydiving Video Organizer
- Modern GUI application built with PySide6
- Automatic video organization by date
- Jump detection and grouping based on recording time
- Configurable video extensions and jump time thresholds
- Option to preserve original video names in parentheses
- Real-time progress monitoring and logging
- Duplicate file prevention using file hashing

- Support for GoPro, Insta360, and other action camera formats
- Manual date correction for videos with incorrect timestamps
- Comprehensive error handling and logging

### Features
- **Smart Organization**: Automatically creates date-based folders (YYYY-MM-DD)
- **Jump Grouping**: Groups videos recorded within configurable time threshold
- **Flexible Naming**: Choose between clean names or preserving original names
- **Cross-Platform**: macOS support with Windows coming soon
- **User-Friendly**: Intuitive GUI with real-time feedback
- **Robust**: Handles edge cases and provides detailed error messages

### Technical Details
- Built with Python 3.11+ and PySide6
- Uses PyInstaller for standalone executable creation
- Supports .mp4, .mov, .MP4, .MOV video formats
- Default jump time threshold: 20 minutes
- File size: ~50MB (compressed)
- System requirements: macOS 10.15+ (Catalina or later)

---

## Version History

### v1.0.0 (2024-12-30)
- 🎉 Initial public release
- 📱 Modern GUI interface
- 🪂 Smart jump detection
- 📁 Automatic file organization
- ⚙️ Configurable settings
- 🔍 Duplicate prevention
- 📝 Comprehensive logging 