# Image Resizer — How-To Guide

**Prerequisites:** Setup complete (see SETUP.md). Pillow installed.

---

## Table of Contents

1. [How to Resize a Single Image](#1-how-to-resize-a-single-image)
2. [How to Compress an Image for Web or Email](#2-how-to-compress-an-image-for-web-or-email)
3. [How to Convert an Image to a Different Format](#3-how-to-convert-an-image-to-a-different-format)
4. [How to Batch Resize All Images in a Folder](#4-how-to-batch-resize-all-images-in-a-folder)
5. [How to Inspect an Image's Dimensions and Details](#5-how-to-inspect-an-images-dimensions-and-details)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Resize a Single Image

**What this does:** Changes the pixel dimensions of an image.

**When to use it:** A photo from your camera is 4032×3024 (4+ MB) and you need a smaller version for email, a web page, or a profile picture.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/image-resizer
```

**Step 2 — Check the original image dimensions.**

```bash
python3 main.py info ~/Pictures/vacation-photo.jpg
```

Output:
```
✅ Success: {'success': True, 'filename': 'vacation-photo.jpg', 'format': 'JPEG', 'mode': 'RGB', 'size': (4032, 3024), 'width': 4032, 'height': 3024, 'file_size_kb': 5124.71}
```

**Step 3 — Resize to 1920 pixels wide (preserving aspect ratio).**

When you specify only the width, the height is calculated automatically to preserve proportions.

```bash
python3 main.py resize ~/Pictures/vacation-photo.jpg ~/Pictures/vacation-1920.jpg 1920
```

Output:
```
✅ Success: {'success': True, 'original_size': (4032, 3024), 'new_size': (1920, 1440), 'output': '/home/user/Pictures/vacation-1920.jpg'}
```

**Step 4 — Verify the result.**

```bash
python3 main.py info ~/Pictures/vacation-1920.jpg
```

```
✅ Success: {'success': True, 'filename': 'vacation-1920.jpg', 'format': 'JPEG', 'mode': 'RGB', 'size': (1920, 1440), 'width': 1920, 'height': 1440, 'file_size_kb': 847.32}
```

**Result:** A 847 KB version of your 5 MB photo — small enough to email or post online.

---

## 2. How to Compress an Image for Web or Email

**What this does:** Reduces an image's file size by saving at a lower JPEG quality. The dimensions stay the same; only the quality (and therefore file size) changes.

**When to use it:** An image is too large to email (many email clients limit attachments to 10–25 MB), or your website images are loading slowly.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/image-resizer
```

**Step 2 — Check the original file size.**

```bash
python3 main.py info ~/Pictures/product-shot.jpg
```

Output:
```
✅ Success: {'success': True, 'filename': 'product-shot.jpg', 'format': 'JPEG', 'mode': 'RGB', 'size': (2400, 1600), 'width': 2400, 'height': 1600, 'file_size_kb': 3847.23}
```

**Step 3 — Compress with default quality (85).**

```bash
python3 main.py compress ~/Pictures/product-shot.jpg ~/Pictures/product-web.jpg
```

Output:
```
✅ Success: {'success': True, 'original_size_kb': 3847.23, 'new_size_kb': 847.18, 'reduction_percent': 77.98, 'output': '/home/user/Pictures/product-web.jpg'}
```

**Step 4 — If you need even smaller, use a lower quality.**

Quality 75 gives a good balance between size and appearance for most photos:

```bash
python3 main.py compress ~/Pictures/product-shot.jpg ~/Pictures/product-small.jpg 75
```

**Step 5 — Check the result.**

```bash
python3 main.py info ~/Pictures/product-small.jpg
```

**Result:** A compressed image at `~/Pictures/product-small.jpg` significantly smaller than the original. Quality 85 is generally undetectable to the naked eye.

---

## 3. How to Convert an Image to a Different Format

**What this does:** Saves an image in a new format (JPG, PNG, WebP, BMP, etc.) based on the output filename's extension.

**When to use it:** A platform requires PNG but you have JPEG. Or you want WebP for better web compression.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/image-resizer
```

**Step 2 — Convert PNG to JPEG.**

```bash
python3 main.py convert ~/Pictures/screenshot.png ~/Pictures/screenshot.jpg
```

Output:
```
✅ Success: {'success': True, 'input_format': '.png', 'output_format': '.jpg', 'output': '/home/user/Pictures/screenshot.jpg'}
```

**Step 3 — Convert JPEG to WebP (smaller for web).**

```bash
python3 main.py convert ~/Pictures/hero.jpg ~/Pictures/hero.webp
```

**Step 4 — Convert JPEG to PNG (lossless, if you need transparency).**

```bash
python3 main.py convert ~/Pictures/photo.jpg ~/Pictures/photo.png
```

**Result:** The image is saved in the new format. The original is unchanged.

**Important note about transparency:** PNG supports transparency; JPEG does not. Converting a PNG with a transparent background to JPEG replaces the transparent areas with white.

---

## 4. How to Batch Resize All Images in a Folder

**What this does:** Resizes every image in a source folder to the same target width and saves the results to a destination folder. Each image's height is calculated proportionally.

**When to use it:** You have a folder of product photos, blog images, or event photos and need all of them at a consistent width for a website or gallery.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/image-resizer
```

**Step 2 — Check how many images are in the folder.**

```bash
ls ~/Photos/product-originals/ | wc -l
```

The skill handles up to 100 images per batch.

**Step 3 — Create the output directory.**

```bash
mkdir -p ~/Photos/product-web
```

**Step 4 — Run batch-resize.**

This example resizes all images to 800px wide:

```bash
python3 main.py batch-resize ~/Photos/product-originals ~/Photos/product-web 800
```

Output:
```
✅ Success: {'success': True, 'processed': 34, 'total': 34, 'errors': 0, 'error_details': []}
```

**Step 5 — Verify one of the output images.**

```bash
python3 main.py info ~/Photos/product-web/product-001.jpg
```

```
✅ Success: {'success': True, 'filename': 'product-001.jpg', 'format': 'JPEG', 'mode': 'RGB', 'size': (800, 600), 'width': 800, 'height': 600, 'file_size_kb': 124.83}
```

**Result:** All 34 images in `~/Photos/product-web` are now 800px wide with proportional heights.

---

## 5. How to Inspect an Image's Dimensions and Details

**What this does:** Prints an image's filename, format, color mode, pixel dimensions, and file size.

**When to use it:** Before uploading an image to a platform with specific requirements. Or to check whether an image file is valid.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/image-resizer
```

**Step 2 — Run the info command.**

```bash
python3 main.py info ~/Downloads/logo.png
```

Output:
```
✅ Success: {'success': True, 'filename': 'logo.png', 'format': 'PNG', 'mode': 'RGBA', 'size': (512, 512), 'width': 512, 'height': 512, 'file_size_kb': 47.83}
```

**Step 3 — Interpret the mode.**

| Mode | Meaning |
|------|---------|
| `RGB` | Standard color (no transparency) |
| `RGBA` | Color with transparency (alpha channel) |
| `L` | Grayscale |
| `P` | Palette (indexed color, often GIFs) |

**Result:** You have the exact dimensions and format — no need to open an image viewer.

---

## 6. Automating with Cron

Schedule batch resizing to run automatically — for example, processing a new-photos folder every night.

### Open the cron editor

```bash
crontab -e
```

### Example: Batch resize new product photos every night at 11 PM

```bash
0 23 * * * python3 /home/yourname/smfworks-skills/skills/image-resizer/main.py batch-resize /home/yourname/Photos/incoming /home/yourname/Photos/web-ready 1200 >> /home/yourname/logs/image-resizer.log 2>&1
```

### Example: Compress a daily screenshot for sharing

```bash
0 9 * * * python3 /home/yourname/smfworks-skills/skills/image-resizer/main.py compress /home/yourname/Screenshots/daily.png /home/yourname/Screenshots/daily-compressed.jpg 80 >> /home/yourname/logs/image-resizer.log 2>&1
```

### Cron Expression Reference

| Expression | Meaning |
|------------|---------|
| `0 23 * * *` | Every day at 11 PM |
| `0 9 * * *` | Every day at 9 AM |
| `0 22 * * 0` | Every Sunday at 10 PM |

### Create the log directory

```bash
mkdir -p ~/logs
```

---

## 7. Combining with Other Skills

**Image Resizer + File Organizer:** Resize product images, then organize them by date:

```bash
python3 ~/smfworks-skills/skills/image-resizer/main.py batch-resize ~/Photos/raw ~/Photos/web 1200
python3 ~/smfworks-skills/skills/file-organizer/main.py organize-date ~/Photos/web
```

**Image Resizer + QR Generator:** Create a QR code, check its dimensions, then resize for print:

```bash
python3 ~/smfworks-skills/skills/qr-generator/main.py url https://mysite.com ~/Desktop/qr.png
python3 ~/smfworks-skills/skills/image-resizer/main.py resize ~/Desktop/qr.png ~/Desktop/qr-print.png 600
```

---

## 8. Troubleshooting Common Issues

### `Pillow not installed. Run: pip install Pillow`

**Fix:** `pip install Pillow`

---

### `Unsupported file type: .heic`

HEIC (iPhone) format is not supported.  
**Fix:** Convert to JPEG first: on macOS, use Preview (Export as JPEG), or `brew install imagemagick && convert photo.heic photo.jpg`

---

### `File too large: X bytes (max: 104857600)`

Input file exceeds 100 MB.  
**Fix:** Use ImageMagick for files over 100 MB: `convert large-input.tif output.jpg`

---

### `Too many files (142). Max: 100`

More than 100 images in the batch source directory.  
**Fix:** Split the directory into subfolders of 100 files or fewer.

---

### `Invalid width: 12000. Must be between 1 and 10000`

Width exceeds the 10,000-pixel maximum.  
**Fix:** Use 10,000 or less.

---

### Output image looks blurry

You're resizing to a much smaller dimension with a large source image. This is normal.  
**Tip:** For photos going to print, keep them at 300 DPI. For web, 72–96 DPI (150–300px/inch equivalent) is sufficient.

---

## 9. Tips & Best Practices

**Never overwrite your originals.** Always specify a different output filename. Once you overwrite an original, the higher-quality version is gone permanently.

**For web images, 1200–1920px wide is usually enough.** Most monitors and screens don't display images wider than 1920px. Going wider just wastes bandwidth.

**Quality 85 is the sweet spot for JPEG compression.** Below 70, compression artifacts become visible to most users. Quality 85 looks identical to the original in most cases and saves 50–80% of file size.

**Use WebP for web pages when possible.** WebP produces smaller files than JPEG or PNG with equivalent quality. Modern browsers (Chrome, Firefox, Safari, Edge) all support it.

**Check info before batch resize.** Run `info` on a sample file from the folder to understand what you're working with before batch processing 100 files.

**For profile photos and avatars, check the platform's required size before resizing.** Twitter wants 400×400, LinkedIn wants 400×400, Facebook wants 180×180. Resize to the exact required size to avoid platform-side resizing which can reduce quality.

**Use `batch-resize` for consistent widths, not consistent file sizes.** If you need all images under a certain file size, use a shell loop with `compress` instead.
