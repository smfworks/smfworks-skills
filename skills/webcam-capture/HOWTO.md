# Webcam Capture — How-To Guide

## Step 1: Capture a Photo

Open your OpenClaw TUI and say something like:

> "Take a photo with the webcam"

The AI will run:
```bash
python3 ~/.openclaw/skills/webcam-capture/scripts/capture.py
```

Photos save to: `~/.openclaw/workspace/captures/`

Or specify a custom path:
```
"Take a photo and save it to ~/Desktop/photo.jpg"
```

## Step 2: Share What You're Looking At

Hold something up to the camera — a whiteboard, document, product, whatever — and say:

> "Analyze what I'm showing you on the camera"

The AI captures a frame and describes what it sees.

## Step 3: Record a Video Clip

> "Record a 5-second video clip"

The AI runs:
```bash
python3 ~/.openclaw/skills/webcam-capture/scripts/capture.py --stream --duration 5
```

Videos save to: `~/.openclaw/workspace/captures/stream_YYYYMMDD_HHMMSS.mp4`

## Step 4: Use Multiple Cameras

If you have multiple cameras, tell the AI which one to use:

> "Take a photo using the second camera"

The script supports `--device /dev/video0` through `/dev/videoN`.

## Step 5: Document Your Workspace

Great for documentation:
> "Snap a photo of my workspace for my project notes"

The AI captures and can include the image in generated documentation.

## Privacy

**The camera light always blinks when capturing.** No silent surveillance is possible — you'll always know when the camera is active.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Device not found` | Run `--list-devices` to find your camera |
| `Permission denied` | Add yourself to the `video` group: `sudo usermod -a -G video $USER` |
| Dark image | Your room may be too dark — the ring light helps! |
| Wrong camera | Specify device: `--device /dev/video1` |

## Script Reference

```bash
# Basic capture
python3 capture.py

# Custom output
python3 capture.py -o ~/my_photo.jpg

# Specific camera
python3 capture.py -d /dev/video1

# List cameras
python3 capture.py --list-devices

# Record video
python3 capture.py --stream --duration 10
```
