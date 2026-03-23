# Image Resizer

> Resize images for web, thumbnails, social media, and email — batch process entire folders

---

## What It Does

Image Resizer quickly reduces image file sizes for web, email, or social media. Resize by exact dimensions, scale by percentage, or batch process entire folders of images. Supports JPG, PNG, and WebP formats with quality control.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install image-resizer
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Resize a single image to web-friendly dimensions:

```bash
python main.py resize photo.jpg --width 800 --output small.jpg
```

---

## Commands

### `resize`

**What it does:** Resize a single image file.

**Usage:**
```bash
python main.py resize [input-file] [options]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input-file` | ✅ Yes | Image file to resize | `photo.jpg` |

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--width` | ❌ No | Target width in pixels | `--width 800` |
| `--height` | ❌ No | Target height in pixels | `--height 600` |
| `--output` | ❌ No | Output file path | `--output small.jpg` |
| `--quality` | ❌ No | JPEG quality 1-100 (default: 85) | `--quality 75` |

**Example:**
```bash
python main.py resize photo.jpg --width 800 --output small.jpg
python main.py resize photo.jpg --height 600 --output thumb.jpg
python main.py resize photo.jpg --width 800 --height 600 --output exact.jpg
python main.py resize photo.jpg --width 1200 --quality 70
```

**Output:**
```
✅ Resized: photo.jpg → small.jpg
   Original: 4032x3024 (3.2 MB)
   New size: 800x600 (245 KB)
   Reduction: 92%
```

---

### `batch`

**What it does:** Resize multiple images at once.

**Usage:**
```bash
python main.py batch [pattern] [options]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `pattern` | ✅ Yes | File pattern (use wildcards) | `~/Photos/*.jpg` |

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--width` | ❌ No | Target width | `--width 1200` |
| `--height` | ❌ No | Target height | `--height 800` |
| `--output` | ❌ No | Output folder | `--output ~/Small/` |
| `--quality` | ❌ No | JPEG quality 1-100 | `--quality 75` |

**Example:**
```bash
python main.py batch ~/Downloads/*.jpg --width 1200 --output ~/Small/
python main.py batch "~/Photos/*.png" --height 600 --output ~/Thumbs/
```

---

### `info`

**What it does:** Display image dimensions, format, and file size.

**Usage:**
```bash
python main.py info [image-file]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `image-file` | ✅ Yes | Image to inspect | `photo.jpg` |

**Example:**
```bash
python main.py info photo.jpg
```

**Output:**
```
📷 Image Info: photo.jpg
   Dimensions: 4032 x 3024 pixels
   Format: JPEG
   File size: 3.2 MB
   Mode: RGB
```

---

## Use Cases

- **Web optimization:** Reduce image sizes for faster page loads
- **Email attachments:** Resize photos before attaching to emails
- **Social media:** Prepare images to exact specs for platforms
- **Thumbnails:** Create smaller versions for galleries
- **Batch processing:** Resize entire event photo folders at once

---

## Tips & Tricks

- Use `--width` alone to scale proportionally by width
- Combine `--width` and `--height` for exact dimensions (may crop)
- Lower `--quality` values = smaller files but reduced quality
- Batch with wildcards: `*.jpg`, `*.png`, or specific folders

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Unsupported format" | Ensure file is JPG, PNG, or WebP |
| "PIL not installed" | Run `pip install Pillow` |
| Batch only processes one file | Use quotes around the pattern: `"~/Photos/*.jpg"` |
| Output file already exists | Use `--output` with a new filename |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- Pillow library (`pip install Pillow`)

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/image-resizer)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
