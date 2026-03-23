# Image Resizer — Quick Reference

## Install
```bash
smfw install image-resizer
```

## Commands
```bash
python main.py resize input.jpg --width 800 --output small.jpg    # Resize by width
python main.py resize input.jpg --height 600 --output thumb.jpg   # Resize by height
python main.py resize input.jpg --width 800 --height 600          # Exact dimensions
python main.py batch ~/Photos/*.jpg --width 1200 --output ~/Small/  # Batch resize
python main.py info image.jpg                                      # Get image info
```

## Common Examples
```bash
# Resize photo to 800px width (maintains aspect ratio)
python main.py resize photo.jpg --width 800 --output small.jpg

# Create thumbnail (150px height)
python main.py resize photo.jpg --height 150 --output thumb.jpg

# Batch resize all JPEGs in a folder
python main.py batch ~/Downloads/*.jpg --width 1200 --output ~/Small/

# Get image dimensions and file size
python main.py info photo.jpg
```

## Help
```bash
python main.py --help
python main.py resize --help
```
