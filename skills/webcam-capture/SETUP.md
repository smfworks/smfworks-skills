# Webcam Capture — Setup Guide

## Requirements

- `ffmpeg` installed on your system
- A working webcam (built-in or USB)
- Linux/macOS/Windows (WSL works too)

## Install ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use WSL.

## Verify Your Camera

```bash
# List available cameras
ls /dev/video*        # Linux
ls /dev/media*        # Linux (more detailed)

# Test capture
ffmpeg -f avfoundation -list_devices true -i "" 2>&1 | grep -i camera   # macOS
v4l2-ctl --list-devices  # Linux
```

## Set Permissions (Linux)

If you get permission errors:
```bash
# Check your user is in the video group
groups $USER

# Add yourself to video group
sudo usermod -a -G video $USER
# Then log out and back in
```

## Quick Test

```bash
# Capture a test photo
ffmpeg -y -f v4l2 -input_format mjpeg -i /dev/video0 -frames:v 1 -update 1 test.jpg

# Or use the script directly
python3 capture.py --list-devices
```
