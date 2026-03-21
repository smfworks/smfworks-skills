#!/usr/bin/env python3
"""
Image Resizer Skill for OpenClaw
Resize, compress, and convert images in batch.
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple
import os

# Security limits
MAX_IMAGE_SIZE = 100 * 1024 * 1024  # 100MB max input file
MAX_DIMENSION = 10000  # Max width/height in pixels
MAX_OUTPUT_DIMENSION = 8000  # Max output dimensions
MAX_BATCH_FILES = 100  # Max files in batch processing
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.tga', '.ico'}


def validate_image_path(file_path: str, must_exist: bool = True) -> tuple[bool, Path, str]:
    """
    Validate an image file path for security.
    
    Returns:
        (is_valid, resolved_path, error_message)
    """
    try:
        path = Path(file_path).resolve()
    except (OSError, ValueError) as e:
        return False, Path(), f"Invalid path: {file_path}"
    
    # Check for path traversal
    normalized = os.path.normpath(file_path)
    if ".." in normalized.split(os.sep):
        return False, path, f"Path traversal detected: {file_path}"
    
    # Check extension
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return False, path, f"Unsupported file type: {path.suffix}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    
    if must_exist:
        if not path.exists():
            return False, path, f"File not found: {file_path}"
        
        if not path.is_file():
            return False, path, f"Not a file: {file_path}"
        
        # Check file size
        try:
            size = path.stat().st_size
            if size > MAX_IMAGE_SIZE:
                return False, path, f"File too large: {size} bytes (max: {MAX_IMAGE_SIZE})"
        except OSError:
            return False, path, f"Cannot access file: {file_path}"
    
    return True, path, ""


def validate_output_path(file_path: str) -> tuple[bool, Path, str]:
    """
    Validate output file path for security.
    """
    try:
        path = Path(file_path).resolve()
    except (OSError, ValueError):
        return False, Path(), f"Invalid path: {file_path}"
    
    # Check for path traversal
    normalized = os.path.normpath(file_path)
    if ".." in normalized.split(os.sep):
        return False, path, f"Path traversal detected: {file_path}"
    
    # Ensure extension is allowed
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        # Default to .png
        path = path.with_suffix('.png')
    
    return True, path, ""


def validate_dimensions(width: int = None, height: int = None) -> tuple[bool, str]:
    """
    Validate image dimensions to prevent memory exhaustion.
    """
    if width is not None:
        if not isinstance(width, int) or width <= 0 or width > MAX_DIMENSION:
            return False, f"Invalid width: {width}. Must be between 1 and {MAX_DIMENSION}"
    
    if height is not None:
        if not isinstance(height, int) or height <= 0 or height > MAX_DIMENSION:
            return False, f"Invalid height: {height}. Must be between 1 and {MAX_DIMENSION}"
    
    return True, ""


def resize_image(input_file: str, output_file: str, width: int = None, height: int = None, 
                 maintain_aspect: bool = True) -> Dict:
    """
    Resize an image.
    
    Args:
        input_file: Input image path
        output_file: Output image path
        width: Target width (optional)
        height: Target height (optional)
        maintain_aspect: Maintain aspect ratio
    
    Returns:
        Dict with operation results
    """
    try:
        from PIL import Image
        
        # Validate input path
        is_valid, input_path, error = validate_image_path(input_file)
        if not is_valid:
            return {"success": False, "error": error}
        
        # Validate output path
        is_valid, output_path, error = validate_output_path(output_file)
        if not is_valid:
            return {"success": False, "error": error}
        
        # Validate dimensions
        is_valid, error = validate_dimensions(width, height)
        if not is_valid:
            return {"success": False, "error": error}
        
        # Validate that at least one dimension is specified
        if width is None and height is None:
            return {"success": False, "error": "Either width or height must be specified"}
        
        with Image.open(input_path) as img:
            original_size = img.size
            
            # Check original dimensions
            if original_size[0] > MAX_DIMENSION or original_size[1] > MAX_DIMENSION:
                return {"success": False, "error": f"Input image too large: {original_size}. Max: {MAX_DIMENSION}x{MAX_DIMENSION}"}
            
            # Calculate new size
            if width and height:
                if maintain_aspect:
                    # Use thumbnail to maintain aspect
                    img.thumbnail((width, height), Image.Resampling.LANCZOS)
                else:
                    # Force resize
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
            elif width:
                ratio = width / original_size[0]
                new_height = int(original_size[1] * ratio)
                # Validate new dimensions
                if new_height > MAX_OUTPUT_DIMENSION:
                    return {"success": False, "error": f"Calculated height {new_height} exceeds maximum {MAX_OUTPUT_DIMENSION}"}
                img = img.resize((width, new_height), Image.Resampling.LANCZOS)
            elif height:
                ratio = height / original_size[1]
                new_width = int(original_size[0] * ratio)
                # Validate new dimensions
                if new_width > MAX_OUTPUT_DIMENSION:
                    return {"success": False, "error": f"Calculated width {new_width} exceeds maximum {MAX_OUTPUT_DIMENSION}"}
                img = img.resize((new_width, height), Image.Resampling.LANCZOS)
            
            # Ensure output directory exists
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                return {"success": False, "error": f"Cannot create output directory: {e}"}
            
            img.save(output_path)
            
            return {
                "success": True,
                "original_size": original_size,
                "new_size": img.size,
                "output": str(output_path)
            }
    except ImportError:
        return {"success": False, "error": "Pillow not installed. Run: pip install Pillow"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def compress_image(input_file: str, output_file: str, quality: int = 85, 
                   max_size_kb: int = None) -> Dict:
    """
    Compress an image to reduce file size.
    
    Args:
        input_file: Input image path
        output_file: Output image path
        quality: JPEG quality (1-100)
        max_size_kb: Target max size in KB (optional)
    
    Returns:
        Dict with operation results
    """
    try:
        from PIL import Image
        
        # Validate input path
        is_valid, input_path, error = validate_image_path(input_file)
        if not is_valid:
            return {"success": False, "error": error}
        
        # Validate output path
        is_valid, output_path, error = validate_output_path(output_file)
        if not is_valid:
            return {"success": False, "error": error}
        
        # Validate quality
        if not isinstance(quality, int) or quality < 1 or quality > 100:
            return {"success": False, "error": "Quality must be between 1 and 100"}
        
        # Validate max_size_kb
        if max_size_kb is not None:
            if not isinstance(max_size_kb, (int, float)) or max_size_kb <= 0:
                return {"success": False, "error": "max_size_kb must be a positive number"}
            if max_size_kb > 50000:  # Max 50MB target
                return {"success": False, "error": "max_size_kb too large (max 50000)"}
        
        original_size = input_path.stat().st_size
        
        with Image.open(input_path) as img:
            # Check image dimensions
            if img.size[0] > MAX_DIMENSION or img.size[1] > MAX_DIMENSION:
                return {"success": False, "error": f"Image too large: {img.size}. Max: {MAX_DIMENSION}x{MAX_DIMENSION}"}
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            
            # Ensure output directory exists
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                return {"success": False, "error": f"Cannot create output directory: {e}"}
            
            if max_size_kb:
                # Binary search for optimal quality with bounds
                low, high = 1, 95
                best_quality = low
                while low <= high:
                    mid = (low + high) // 2
                    img.save(output_path, 'JPEG', quality=mid)
                    current_size = output_path.stat().st_size / 1024
                    if current_size <= max_size_kb:
                        best_quality = mid
                        high = mid - 1
                    else:
                        low = mid + 1
                    
                    # Prevent infinite loop
                    if low > high:
                        break
                
                # Save with best found quality
                if best_quality != mid:
                    img.save(output_path, 'JPEG', quality=best_quality)
            else:
                img.save(output_path, 'JPEG', quality=quality)
        
        new_size = output_path.stat().st_size
        reduction = ((original_size - new_size) / original_size) * 100 if original_size > 0 else 0
        
        return {
            "success": True,
            "original_size_kb": round(original_size / 1024, 2),
            "new_size_kb": round(new_size / 1024, 2),
            "reduction_percent": round(reduction, 2),
            "output": str(output_path)
        }
    except ImportError:
        return {"success": False, "error": "Pillow not installed. Run: pip install Pillow"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def convert_format(input_file: str, output_file: str, format: str = None) -> Dict:
    """
    Convert image to different format.
    
    Args:
        input_file: Input image path
        output_file: Output image path
        format: Target format (optional, inferred from extension)
    
    Returns:
        Dict with operation results
    """
    try:
        from PIL import Image
        
        # Validate input path
        is_valid, input_path, error = validate_image_path(input_file)
        if not is_valid:
            return {"success": False, "error": error}
        
        # Validate output path
        is_valid, output_path, error = validate_output_path(output_file)
        if not is_valid:
            return {"success": False, "error": error}
        
        with Image.open(input_path) as img:
            # Check image dimensions
            if img.size[0] > MAX_DIMENSION or img.size[1] > MAX_DIMENSION:
                return {"success": False, "error": f"Image too large: {img.size}. Max: {MAX_DIMENSION}x{MAX_DIMENSION}"}
            
            # Ensure output directory exists
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                return {"success": False, "error": f"Cannot create output directory: {e}"}
            
            # Convert RGBA to RGB for JPEG
            if output_path.suffix.lower() in ('.jpg', '.jpeg') and img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            
            img.save(output_path, format=format)
            
            return {
                "success": True,
                "input_format": input_path.suffix.lower(),
                "output_format": output_path.suffix.lower(),
                "output": str(output_path)
            }
    except ImportError:
        return {"success": False, "error": "Pillow not installed. Run: pip install Pillow"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def batch_resize(input_dir: str, output_dir: str, width: int, height: int = None) -> Dict:
    """
    Resize all images in a directory.
    
    Args:
        input_dir: Input directory
        output_dir: Output directory
        width: Target width
        height: Target height (optional)
    
    Returns:
        Dict with operation results
    """
    try:
        from PIL import Image
        
        # Validate input directory
        is_valid, error = validate_dimensions(width, height)
        if not is_valid:
            return {"success": False, "error": error}
        
        try:
            input_path = Path(input_dir).resolve()
            output_path = Path(output_dir).resolve()
        except (OSError, ValueError) as e:
            return {"success": False, "error": f"Invalid directory path: {e}"}
        
        # Check for path traversal
        for dir_path in [input_dir, output_dir]:
            normalized = os.path.normpath(dir_path)
            if ".." in normalized.split(os.sep):
                return {"success": False, "error": f"Path traversal detected: {dir_path}"}
        
        if not input_path.exists():
            return {"success": False, "error": f"Input directory not found: {input_dir}"}
        
        try:
            output_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return {"success": False, "error": f"Cannot create output directory: {e}"}
        
        # Get image files
        image_extensions = ALLOWED_EXTENSIONS
        images = [f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]
        
        # Limit batch size
        if len(images) > MAX_BATCH_FILES:
            return {"success": False, "error": f"Too many files ({len(images)}). Max: {MAX_BATCH_FILES}"}
        
        processed = 0
        errors = []
        
        for img_file in images:
            try:
                output_file = output_path / img_file.name
                
                with Image.open(img_file) as img:
                    # Check dimensions
                    if img.size[0] > MAX_DIMENSION or img.size[1] > MAX_DIMENSION:
                        errors.append(f"{img_file.name}: Image too large")
                        continue
                    
                    if height:
                        img = img.resize((width, height), Image.Resampling.LANCZOS)
                    else:
                        ratio = width / img.size[0]
                        new_height = int(img.size[1] * ratio)
                        if new_height > MAX_OUTPUT_DIMENSION:
                            errors.append(f"{img_file.name}: Calculated height too large")
                            continue
                        img = img.resize((width, new_height), Image.Resampling.LANCZOS)
                    
                    img.save(output_file)
                    processed += 1
            except Exception as e:
                errors.append(f"{img_file.name}: {str(e)}")
        
        return {
            "success": True,
            "processed": processed,
            "total": len(images),
            "errors": len(errors),
            "error_details": errors[:5] if errors else []
        }
    except ImportError:
        return {"success": False, "error": "Pillow not installed. Run: pip install Pillow"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_image_info(input_file: str) -> Dict:
    """
    Get image information.
    
    Args:
        input_file: Input image path
    
    Returns:
        Dict with image info
    """
    try:
        from PIL import Image
        
        # Validate input path
        is_valid, input_path, error = validate_image_path(input_file)
        if not is_valid:
            return {"success": False, "error": error}
        
        with Image.open(input_path) as img:
            file_size = input_path.stat().st_size
            
            return {
                "success": True,
                "filename": input_path.name,
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "width": img.width,
                "height": img.height,
                "file_size_kb": round(file_size / 1024, 2)
            }
    except ImportError:
        return {"success": False, "error": "Pillow not installed. Run: pip install Pillow"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    """CLI interface for image resizer."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [options]")
        print("Commands:")
        print("  resize <input> <output> <width> [height]")
        print("  compress <input> <output> [quality]")
        print("  convert <input> <output>")
        print("  batch-resize <input_dir> <output_dir> <width>")
        print("  info <input>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "resize":
        if len(sys.argv) < 5:
            print("Error: resize requires input, output, and width")
            sys.exit(1)
        
        try:
            width = int(sys.argv[4]) if len(sys.argv) > 4 else None
            height = int(sys.argv[5]) if len(sys.argv) > 5 else None
        except ValueError:
            print("Error: Width and height must be integers")
            sys.exit(1)
        
        result = resize_image(sys.argv[2], sys.argv[3], width, height)
    elif command == "compress":
        if len(sys.argv) < 4:
            print("Error: compress requires input and output")
            sys.exit(1)
        
        try:
            quality = int(sys.argv[4]) if len(sys.argv) > 4 else 85
        except ValueError:
            print("Error: Quality must be an integer")
            sys.exit(1)
        
        result = compress_image(sys.argv[2], sys.argv[3], quality)
    elif command == "convert":
        if len(sys.argv) < 4:
            print("Error: convert requires input and output")
            sys.exit(1)
        result = convert_format(sys.argv[2], sys.argv[3])
    elif command == "batch-resize":
        if len(sys.argv) < 5:
            print("Error: batch-resize requires input_dir, output_dir, and width")
            sys.exit(1)
        
        try:
            width = int(sys.argv[4])
        except ValueError:
            print("Error: Width must be an integer")
            sys.exit(1)
        
        result = batch_resize(sys.argv[2], sys.argv[3], width)
    elif command == "info":
        if len(sys.argv) < 3:
            print("Error: info requires input file")
            sys.exit(1)
        result = get_image_info(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
    
    if result["success"]:
        print(f"✅ Success: {result}")
    else:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
