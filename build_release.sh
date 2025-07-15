#!/bin/bash

# Skydiving Video Organizer - Release Build Script
# This script builds the application and creates release packages

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VERSION="1.0.0"
APP_NAME="Skydiving Video Organizer"
BUILD_DIR="dist"
RELEASE_DIR="release"

echo -e "${BLUE}🚀 Building ${APP_NAME} v${VERSION}${NC}"
echo "=================================="

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ Error: This script is designed for macOS only.${NC}"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 is not installed.${NC}"
    exit 1
fi

# Check if pipenv is installed
if ! command -v pipenv &> /dev/null; then
    echo -e "${RED}❌ Error: pipenv is not installed.${NC}"
    echo "Install it with: pip3 install pipenv"
    exit 1
fi

# Clean previous builds
echo -e "${YELLOW}🧹 Cleaning previous builds...${NC}"
rm -rf "$BUILD_DIR"
rm -rf "$RELEASE_DIR"
mkdir -p "$RELEASE_DIR"

# Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
pipenv install

# Run tests
echo -e "${YELLOW}🧪 Running tests...${NC}"
if pipenv run python test_gui.py; then
    echo -e "${GREEN}✅ Tests passed${NC}"
else
    echo -e "${RED}❌ Tests failed${NC}"
    exit 1
fi

# Build application
echo -e "${YELLOW}🔨 Building application with PyInstaller...${NC}"
pipenv run pyinstaller video_organizer.spec

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build successful!${NC}"
else
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi

# Create release packages
echo -e "${YELLOW}📦 Creating release packages...${NC}"

# Create ZIP package
ZIP_NAME="${APP_NAME// /_}_v${VERSION}_macOS.zip"
echo -e "${BLUE}Creating ZIP package: ${ZIP_NAME}${NC}"
cd "$BUILD_DIR"
zip -r "../$RELEASE_DIR/$ZIP_NAME" "${APP_NAME}.app"
cd ..

# Create DMG package (if hdiutil is available)
if command -v hdiutil &> /dev/null; then
    DMG_NAME="${APP_NAME// /_}_v${VERSION}_macOS.dmg"
    echo -e "${BLUE}Creating DMG package: ${DMG_NAME}${NC}"
    
    # Create a temporary directory for DMG contents
    TEMP_DMG_DIR="temp_dmg"
    mkdir -p "$TEMP_DMG_DIR"
    
    # Copy app to temp directory
    cp -R "$BUILD_DIR/${APP_NAME}.app" "$TEMP_DMG_DIR/"
    
    # Create DMG
    hdiutil create -volname "${APP_NAME} v${VERSION}" -srcfolder "$TEMP_DMG_DIR" -ov -format UDZO "$RELEASE_DIR/$DMG_NAME"
    
    # Clean up temp directory
    rm -rf "$TEMP_DMG_DIR"
    
    echo -e "${GREEN}✅ DMG created successfully${NC}"
else
    echo -e "${YELLOW}⚠️  hdiutil not available, skipping DMG creation${NC}"
fi

# Create source code package
SOURCE_ZIP_NAME="${APP_NAME// /_}_v${VERSION}_source.zip"
echo -e "${BLUE}Creating source package: ${SOURCE_ZIP_NAME}${NC}"

# Files to include in source package
SOURCE_FILES=(
    "video_organizer_gui.py"
    "organize_videos.py"
    "test_gui.py"
    "build_app.sh"
    "video_organizer.spec"
    "Pipfile"
    "Pipfile.lock"
    "README.md"
    "CHANGELOG.md"
    "LICENSE"
)

zip -r "$RELEASE_DIR/$SOURCE_ZIP_NAME" "${SOURCE_FILES[@]}"

# Generate checksums
echo -e "${YELLOW}🔍 Generating checksums...${NC}"
cd "$RELEASE_DIR"
for file in *.zip *.dmg; do
    if [ -f "$file" ]; then
        shasum -a 256 "$file" > "${file}.sha256"
        echo -e "${GREEN}✅ Checksum created for $file${NC}"
    fi
done
cd ..

# Create release notes
echo -e "${YELLOW}📝 Creating release notes...${NC}"
cat > "$RELEASE_DIR/RELEASE_NOTES.md" << EOF
# ${APP_NAME} v${VERSION} - Release Notes

## Download Options

### macOS Users (Recommended)
- **${ZIP_NAME}** - ZIP archive (drag to Applications folder)
$(if [ -f "$RELEASE_DIR/${APP_NAME// /_}_v${VERSION}_macOS.dmg" ]; then echo "- **${APP_NAME// /_}_v${VERSION}_macOS.dmg** - DMG installer"; fi)

### Developers
- **${SOURCE_ZIP_NAME}** - Source code package

## Installation

### From ZIP/DMG:
1. Download the ZIP or DMG file
2. Extract the ZIP or mount the DMG
3. Drag "${APP_NAME}.app" to your Applications folder
4. Right-click the app and select "Open" (first time only)

### From Source:
1. Download the source ZIP
2. Extract and follow the build instructions in README.md

## What's New in v${VERSION}

$(cat CHANGELOG.md | sed -n '/## \[1.0.0\]/,/^## /p' | head -n -1)

## System Requirements

- **macOS**: 10.15 (Catalina) or later
- **Storage**: At least 1GB free space
- **Memory**: 4GB RAM recommended

## Support

- Report issues: [GitHub Issues](https://github.com/yourusername/skydiving-video-organizer/issues)
- Join discussions: [GitHub Discussions](https://github.com/yourusername/skydiving-video-organizer/discussions)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
EOF

# Final summary
echo ""
echo -e "${GREEN}🎉 Release build completed successfully!${NC}"
echo "=================================="
echo -e "${BLUE}Release files created in: ${RELEASE_DIR}/${NC}"
echo ""

# List created files
echo -e "${YELLOW}📁 Created files:${NC}"
ls -la "$RELEASE_DIR"/

echo ""
echo -e "${GREEN}✅ Ready for GitHub release!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Upload files to GitHub Releases"
echo "2. Copy release notes from $RELEASE_DIR/RELEASE_NOTES.md"
echo "3. Tag the release as v${VERSION}"
echo ""
echo -e "${YELLOW}Happy organizing! 🪂${NC}" 