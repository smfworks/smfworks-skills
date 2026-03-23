#!/usr/bin/env python3
"""Webcam capture utility using ffmpeg.

Usage:
    python3 capture.py                    # Capture single frame, auto-named
    python3 capture.py -n 5               # Capture 5 frames
    python3 capture.py -d /dev/video1     # Use specific device
    python3 capture.py -o myphoto.jpg      # Custom output path
    python3 capture.py --list-devices      # List available cameras
    python3 capture.py --stream           # Show live preview (5s)

Requires: ffmpeg
"""

import argparse
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

DEFAULT_DEVICE = "/dev/video0"
OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "captures"


def list_devices():
    """List all available video devices."""
    print("Available video devices:")
    for i in range(10):
        dev = f"/dev/video{i}"
        if os.path.exists(dev):
            print(f"  {dev}")


def capture_frame(device: str, output_path: str) -> bool:
    """Capture a single frame from the webcam.

    Args:
        device: Video device path (e.g. /dev/video0)
        output_path: Where to save the image

    Returns:
        True if capture succeeded, False otherwise
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-f", "v4l2",
        "-input_format", "mjpeg",
        "-i", device,
        "-frames:v", "1",
        "-update", "1",
        output_path
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print(f"Error capturing from {device}:", file=sys.stderr)
        print(result.stderr[-500:], file=sys.stderr)
        return False

    size = os.path.getsize(output_path)
    print(f"Captured: {output_path} ({size} bytes)")
    return True


def capture_stream(device: str, duration: int = 5) -> str:
    """Capture a short video clip.

    Args:
        device: Video device path
        duration: Recording duration in seconds

    Returns:
        Path to saved video file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"stream_{timestamp}.mp4"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-f", "v4l2",
        "-input_format", "mjpeg",
        "-t", str(duration),
        "-i", device,
        "-c:v", "libx264",
        "-preset", "fast",
        str(output_path)
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print(f"Error recording stream: {result.stderr[-500:]}", file=sys.stderr)
        return ""

    print(f"Recorded {duration}s: {output_path}")
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(description="Webcam capture tool")
    parser.add_argument("-d", "--device", default=DEFAULT_DEVICE,
                        help=f"Video device (default: {DEFAULT_DEVICE})")
    parser.add_argument("-o", "--output", default="",
                        help="Output file path (default: auto-generated)")
    parser.add_argument("-n", "--frames", type=int, default=1,
                        help="Number of frames to capture")
    parser.add_argument("-t", "--timestamp", action="store_true",
                        help="Add timestamp to filename")
    parser.add_argument("--list-devices", action="store_true",
                        help="List available video devices and exit")
    parser.add_argument("--stream", action="store_true",
                        help="Capture video clip instead of photo")
    parser.add_argument("--duration", type=int, default=5,
                        help="Stream duration in seconds (default: 5)")

    args = parser.parse_args()

    if args.list_devices:
        list_devices()
        return 0

    if not os.path.exists(args.device):
        print(f"Device not found: {args.device}", file=sys.stderr)
        print("Use --list-devices to see available cameras.", file=sys.stderr)
        return 1

    if args.stream:
        output = capture_stream(args.device, args.duration)
        return 0 if output else 1

    # Generate output path if not specified
    if not args.output:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = str(OUTPUT_DIR / f"capture_{ts}.jpg")

    # Capture requested frames
    for i in range(args.frames):
        if args.frames > 1:
            frame_path = args.output.replace(".jpg", f"_{i+1}.jpg")
        else:
            frame_path = args.output

        if not capture_frame(args.device, frame_path):
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
