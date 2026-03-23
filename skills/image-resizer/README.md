# Image Resizer

> Resize, compress, convert, and batch-process images — plus get file info — all from the terminal.

**Tier:** Free — no subscription required  
**Version:** 1.0  
**Category:** Productivity / Image Processing

---

## What It Does

Image Resizer is an OpenClaw skill for common image operations: resize to specific dimensions, compress to reduce file size (with optional target size in KB), convert between formats (JPG, PNG, WebP, BMP, etc.), batch-resize all images in a folder, and inspect an image's dimensions and metadata.

It uses Python's Pillow library and runs entirely on your local machine — no internet required.

**What it does NOT do:** It does not edit image content (crop, rotate, filters, watermarks), perform OCR, animate GIFs, process RAW camera files, or resize more than 100 images in a single batch.

---

## Prerequisites

- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed**
- [ ] **Pillow Python package** — installed during setup
- [ ] **No subscription required** — free tier skill
- [ ] **No API keys required**

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/image-resizer
pip install Pillow
python3 main.py
```

Expected output:
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

## Quick Start

Get information about an image:

```bash
python3 main.py info ~/Pictures/photo.jpg
```

Output:
```
✅ Success: {'success': True, 'filename': 'photo.jpg', 'format': 'JPEG', 'mode': 'RGB', 'size': (4032, 3024), 'width': 4032, 'height': 3024, 'file_size_kb': 4847.23}
```

---

## Command Reference

### `resize`

Resizes an image to a specified width and/or height. When only one dimension is given, the other is calculated proportionally to maintain the aspect ratio.

**Usage:**
```bash
python3 main.py resize <input> <output> <width> [height]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input` | ✅ Yes | Input image file | `photo.jpg` |
| `output` | ✅ Yes | Output image file | `photo-small.jpg` |
| `width` | ✅ Yes | Target width in pixels | `800` |
| `height` | ❌ No | Target height in pixels. If omitted, calculated to preserve aspect ratio. | `600` |

**Example — resize by width only (preserves aspect ratio):**
```bash
python3 main.py resize ~/Pictures/photo.jpg ~/Pictures/photo-800.jpg 800
```

Output:
```
✅ Success: {'success': True, 'original_size': (4032, 3024), 'new_size': (800, 600), 'output': '/home/user/Pictures/photo-800.jpg'}
```

**Example — resize to exact dimensions (may stretch):**
```bash
python3 main.py resize ~/Pictures/banner.png ~/Pictures/banner-1200x400.png 1200 400
```

When both width and height are specified, the image is thumbnailed (fit within the box without cropping). To force exact dimensions, edit the code to use `maintain_aspect=False`.

---

### `compress`

Reduces an image's file size by saving at a lower JPEG quality. Default quality is 85 (out of 100). You can also specify a target file size in KB and the skill finds the right quality automatically.

**Usage:**
```bash
python3 main.py compress <input> <output> [quality]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input` | ✅ Yes | Input image file | `photo.jpg` |
| `output` | ✅ Yes | Output compressed file | `photo-small.jpg` |
| `quality` | ❌ No | JPEG quality 1–100. Default: 85. | `70` |

**Example — compress with default quality:**
```bash
python3 main.py compress ~/Pictures/hero-image.jpg ~/Pictures/hero-compressed.jpg
```

Output:
```
✅ Success: {'success': True, 'original_size_kb': 4847.23, 'new_size_kb': 1247.18, 'reduction_percent': 74.27, 'output': '/home/user/Pictures/hero-compressed.jpg'}
```

**Example — compress aggressively:**
```bash
python3 main.py compress ~/Pictures/photo.jpg ~/Pictures/photo-web.jpg 60
```

---

### `convert`

Converts an image from one format to another. The output format is determined by the output filename's extension.

**Usage:**
```bash
python3 main.py convert <input> <output>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input` | ✅ Yes | Input image file | `logo.png` |
| `output` | ✅ Yes | Output file. Extension determines format. | `logo.jpg` |

**Supported formats:** .jpg/.jpeg, .png, .gif, .bmp, .tiff, .webp, .tga, .ico

**Example — PNG to JPEG:**
```bash
python3 main.py convert ~/Pictures/screenshot.png ~/Pictures/screenshot.jpg
```

Output:
```
✅ Success: {'success': True, 'input_format': '.png', 'output_format': '.jpg', 'output': '/home/user/Pictures/screenshot.jpg'}
```

**Example — JPEG to WebP:**
```bash
python3 main.py convert ~/Pictures/photo.jpg ~/Pictures/photo.webp
```

---

### `batch-resize`

Resizes all images in a folder to the same width. A proportional height is calculated for each image individually. Output goes to a separate folder.

**Usage:**
```bash
python3 main.py batch-resize <input_dir> <output_dir> <width>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input_dir` | ✅ Yes | Folder containing images to resize | `~/Photos/originals` |
| `output_dir` | ✅ Yes | Folder for resized output images | `~/Photos/resized` |
| `width` | ✅ Yes | Target width in pixels for all images | `1200` |

**Limits:** Max 100 files per batch.

**Example:**
```bash
python3 main.py batch-resize ~/Photos/product-photos ~/Photos/web-ready 800
```

Output:
```
✅ Success: {'success': True, 'processed': 24, 'total': 24, 'errors': 0, 'error_details': []}
```

---

### `info`

Displays metadata for an image: filename, format, color mode, dimensions, and file size.

**Usage:**
```bash
python3 main.py info <input>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input` | ✅ Yes | Image file to inspect | `photo.jpg` |

**Example:**
```bash
python3 main.py info ~/Downloads/product-shot.png
```

Output:
```
✅ Success: {'success': True, 'filename': 'product-shot.png', 'format': 'PNG', 'mode': 'RGBA', 'size': (1200, 800), 'width': 1200, 'height': 800, 'file_size_kb': 284.17}
```

---

## Use Cases

### 1. Resize a photo for email or web

Large camera photos (4–8 MB) are too big for email. Resize to web-friendly dimensions:

```bash
python3 main.py resize ~/Pictures/vacation.jpg ~/Pictures/vacation-web.jpg 1920
```

---

### 2. Compress all product photos for a website

Large images slow down websites. Compress to under 200 KB each:

```bash
python3 main.py compress ~/Photos/product.jpg ~/Photos/product-web.jpg 75
```

---

### 3. Batch resize all photos in a folder

Resize an entire folder of photos for a gallery or portfolio:

```bash
python3 main.py batch-resize ~/Photos/originals ~/Photos/gallery 1200
```

---

### 4. Convert PNG to WebP for modern web

WebP files are smaller than PNG/JPEG with similar quality:

```bash
python3 main.py convert ~/images/hero.png ~/images/hero.webp
```

---

### 5. Check image dimensions before uploading

Verify an image meets a required size before uploading it to a platform:

```bash
python3 main.py info ~/Desktop/profile-photo.jpg
```

---

## Configuration

No configuration file or environment variables needed.

**Built-in limits:**

| Setting | Value |
|---------|-------|
| Max input file size | 100 MB |
| Max input dimensions | 10,000 × 10,000 pixels |
| Max output dimensions | 8,000 × 8,000 pixels |
| Max batch files | 100 |

---

## Troubleshooting

### `Pillow not installed. Run: pip install Pillow`
**Fix:** `pip install Pillow`

### `File not found: /path/to/image.jpg`
**Fix:** Check the path with `ls ~/your-folder/`.

### `Unsupported file type: .heic`
HEIC (iPhone photos) is not supported.  
**Fix:** Convert HEIC to JPEG first using macOS's built-in converter or `brew install imagemagick && convert photo.heic photo.jpg`.

### `File too large: X bytes (max: 104857600)`
Input file is over 100 MB.  
**Fix:** Pre-process with ImageMagick or another tool that handles very large files.

### `Invalid width: 15000. Must be between 1 and 10000`
Width exceeds the maximum allowed dimension.  
**Fix:** Use a width of 10,000 or less.

### `Too many files (142). Max: 100`
More than 100 image files in the input directory.  
**Fix:** Split the directory into subfolders of 100 files or fewer and run batch-resize on each.

### Compress output is the same size or larger
For PNG files, JPEG compression converts them to JPEG format. If the original is already well-optimized or very small, compression may not help.  
**Fix:** Try a lower quality value (50–70). Or use the `convert` command to change to WebP, which typically compresses better.

---

## FAQ

**Q: Does resize modify the original file?**  
A: No. Always specify a different output filename. The input is never modified.

**Q: What's the difference between `resize` and `compress`?**  
A: `resize` changes pixel dimensions. `compress` keeps the same dimensions but reduces quality to shrink the file size.

**Q: Does `convert` to JPEG lose transparency?**  
A: Yes. JPEG doesn't support transparency. The skill replaces transparent areas with white when converting from PNG/RGBA to JPEG.

**Q: Can I batch compress (not just batch resize)?**  
A: Not directly — `batch-resize` only resizes. For batch compression, use a shell loop:
```bash
for f in ~/Photos/*.jpg; do python3 main.py compress "$f" "${f%.jpg}-compressed.jpg" 75; done
```

**Q: Does `batch-resize` process subdirectories?**  
A: No — only files directly in `input_dir`. Use a loop for recursive processing.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| Pillow | 9.0 or newer |
| OpenClaw | Any version |
| Operating System | Linux, macOS |
| Subscription Tier | Free |
| External APIs | None |
| Internet Connection | Not required |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/image-resizer)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
