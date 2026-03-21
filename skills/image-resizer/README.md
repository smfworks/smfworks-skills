# Image Resizer

An image processing skill for OpenClaw. Resize, compress, and convert images.

## Features

- **Resize Images**: Scale images by width/height with aspect ratio preservation
- **Compress Images**: Reduce file size with quality adjustment
- **Format Conversion**: Convert between image formats
- **Batch Processing**: Resize entire directories of images
- **Image Information**: Get image metadata

## Installation

```bash
pip install Pillow
```

## Usage

### Resize Image
```bash
# Resize to specific dimensions
python main.py resize input.jpg output.jpg 800 600

# Resize by width (maintains aspect ratio)
python main.py resize input.jpg output.jpg 800

# Resize by height (maintains aspect ratio)
python main.py resize input.jpg output.jpg 0 600
```

### Compress Image
```bash
python main.py compress input.jpg output.jpg 85
```
Quality range: 1-100 (higher = better quality, larger file)

### Convert Format
```bash
python main.py convert input.png output.jpg
```

### Batch Resize
```bash
python main.py batch-resize ./input/ ./output/ 800
```

### Get Image Info
```bash
python main.py info image.jpg
```

## Input Validation Limits

| Parameter | Limit |
|-----------|-------|
| Maximum file size | 100 MB |
| Maximum dimensions | 10,000 x 10,000 pixels |
| Maximum output dimensions | 8,000 x 8,000 pixels |
| Maximum batch files | 100 files |
| Allowed extensions | .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp, .tga, .ico |
| Quality range | 1-100 |

## Security Considerations

- **Path Traversal Protection**: Blocks `..` sequences in paths
- **File Extension Validation**: Only processes allowed image formats
- **File Size Limits**: Prevents processing of oversized files
- **Dimension Validation**: Prevents memory exhaustion from huge images
- **Safe Filename Handling**: Sanitizes output filenames

## Error Handling

Errors are categorized:
- **ImportError**: Pillow not installed
- **OSError**: File system errors
- **ValueError**: Invalid dimensions or parameters
- **PermissionError**: Insufficient file permissions

## Known Limitations

- RGBA to JPEG conversion adds white background
- Maximum 100 files per batch operation
- Large images (>10,000px) are rejected
- Limited to PIL-supported formats
- Memory usage scales with image size

## Examples

```bash
# Resize for web
python main.py resize photo.jpg photo-web.jpg 1200

# Compress for sharing
python main.py compress photo.jpg photo-compact.jpg 75

# Convert PNG to JPEG
python main.py convert screenshot.png screenshot.jpg

# Batch resize all images
python main.py batch-resize ./photos/ ./thumbnails/ 200
```
