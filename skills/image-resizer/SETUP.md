# Image Resizer — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Free — no subscription, no API keys required

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| pip | Python package manager | Free |
| Pillow | Python image processing library | Free |
| smfworks-skills repository | Cloned via git | Free |

---

## Step 1 — Verify Python

```bash
python3 --version
```

Expected: `Python 3.9.x` or newer.

---

## Step 2 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 3 — Install Pillow

```bash
pip install Pillow
```

Expected output:
```
Collecting Pillow
  Downloading Pillow-10.1.0-cp311-cp311-linux_x86_64.whl (3.8 MB)
Installing collected packages: Pillow
Successfully installed Pillow-10.1.0
```

---

## Step 4 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/image-resizer
```

---

## Step 5 — Verify

```bash
python3 main.py
```

Expected:
```
Usage: python main.py <command> [options]
Commands:
  resize <input> <output> <width> [height]
  compress <input> <output> [quality]
  convert <input> <output>
  batch-resize <input_dir> <output_dir> <width>
  info <input>
```

---

## Verify Your Setup

Test with a real image:

```bash
python3 main.py info ~/Pictures/any-photo.jpg
```

Expected:
```
✅ Success: {'success': True, 'filename': 'any-photo.jpg', 'format': 'JPEG', 'mode': 'RGB', 'size': (4032, 3024), 'width': 4032, 'height': 3024, 'file_size_kb': 4847.23}
```

If you don't have a `.jpg` handy, download a test image:

```bash
curl -o /tmp/test.jpg https://picsum.photos/800/600
python3 main.py info /tmp/test.jpg
```

Expected output includes format, dimensions, and file size. If you see this, setup is complete.

---

## Configuration Options

No configuration file or environment variables needed.

---

## Troubleshooting

**`Pillow not installed`** — Run `pip install Pillow`.

**`pip: command not found`** — Try `pip3 install Pillow` or `python3 -m pip install Pillow`.

**HEIC files not supported** — Convert iPhone HEIC photos to JPEG first using macOS's built-in export or `brew install imagemagick && convert photo.heic photo.jpg`.

---

## Next Steps

Setup complete. See **HOWTO.md** for walkthroughs on resizing, compressing, batch processing, and cron automation.
