---
name: webcam-capture
description: Capture photos and short videos from a connected webcam. Use when: (1) user wants to share a screenshot or image via camera, (2) user asks to take a photo or capture from webcam, (3) analyzing something physical held up to the camera, (4) documenting a whiteboard or workspace, (5) capturing any visual from the webcam. Also use when a skill needs a visual input captured before processing. Triggers on: "take a photo", "capture from camera", "use the webcam", "snap a picture", "record video", "webcam capture".
---

# Webcam Capture

Capture still images or short video clips from a connected webcam using `ffmpeg`.

## Quick Use

```bash
# Single photo (saves to ~/.openclaw/workspace/captures/)
python3 skills/webcam-capture/scripts/capture.py

# Auto-named with timestamp
python3 skills/webcam-capture/scripts/capture.py --timestamp

# Custom output path
python3 skills/webcam-capture/scripts/capture.py -o /path/to/output.jpg

# Specific device if multiple cameras
python3 skills/webcam-capture/scripts/capture.py -d /dev/video1

# List available cameras
python3 skills/webcam-capture/scripts/capture.py --list-devices

# Record a 10-second video clip
python3 skills/webcam-capture/scripts/capture.py --stream --duration 10
```

## After Capture — Analyze Image

After capturing, use the `image` tool to analyze:

```
Tool: image
  image: /home/mikesai1/.openclaw/workspace/captures/capture_20260323_143052.jpg
  prompt: [describe what you see / analyze the content]
```

Captures save to: `~/.openclaw/workspace/captures/`

## Device Selection

Most systems have `/dev/video0`. If multiple cameras exist:
- `/dev/video0` — typically built-in webcam
- `/dev/video1` — typically USB/second camera

Use `--list-devices` to confirm before capturing.

## Requirements

- `ffmpeg` must be installed
- Video device must be accessible (check `/dev/video*` permissions if needed)

## Notes

- The camera light will briefly blink when capturing — no silent surveillance possible
- Images are JPEG, ~150KB per frame
- Videos are H.264 MP4, ~1MB per second
- Webcam must be physically connected and powered on
