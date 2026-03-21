#!/usr/bin/env python3
"""
Image Resizer Skill for OpenClaw
Resize, compress, and convert images in batch.
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple


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
        
        with Image.open(input_file) as img:
            original_size = img.size
            
            if width and height:
                if maintain_aspect:
                    img.thumbnail((width, height), Image.Resampling.LANCZOS)
                else:
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
            elif width:
                ratio = width / original_size[0]
                height = int(original_size[1] * ratio)
                img = img.resize((width, height), Image.Resampling.LANCZOS)
            elif height:
                ratio = height / original_size[1]
                width = int(original_size[0] * ratio)
                img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            img.save(output_file)
            
            return {
                "success": True,
                "original_size": original_size,
                "new_size": img.size,
                "output": output_file
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
        
        original_size = Path(input_file).stat().st_size
        
        with Image.open(input_file) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            
            if max_size_kb:
                # Binary search for optimal quality
                low, high = 1, 95
                while low < high:
                    mid = (low + high) // 2
                    img.save(output_file, 'JPEG', quality=mid)
                    current_size = Path(output_file).stat().st_size / 1024
                    if current_size <= max_size_kb:
                        high = mid
                    else:
                        low = mid + 1
            else:
                img.save(output_file, 'JPEG', quality=quality)
        
        new_size = Path(output_file).stat().st_size
        reduction = ((original_size - new_size) / original_size) * 100
        
        return {
            "success": True,
            "original_size_kb": round(original_size / 1024, 2),
            "new_size_kb": round(new_size / 1024, 2),
            "reduction_percent": round(reduction, 2),
            "output": output_file
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
        
        with Image.open(input_file) as img:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            
            # Convert RGBA to RGB for JPEG
            if output_file.lower().endswith(('.jpg', '.jpeg')) and img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            
            img.save(output_file, format=format)
            
            return {
                "success": True,
                "input_format": Path(input_file).suffix.lower(),
                "output_format": Path(output_file).suffix.lower(),
                "output": output_file
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
        
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
        images = [f for f in input_path.iterdir() if f.suffix.lower() in image_extensions]
        
        processed = 0
        errors = []
        
        for img_file in images:
            try:
                output_file = output_path / img_file.name
                with Image.open(img_file) as img:
                    if height:
                        img = img.resize((width, height), Image.Resampling.LANCZOS)
                    else:
                        ratio = width / img.size[0]
                        new_height = int(img.size[1] * ratio)
                        img = img.resize((width, new_height), Image.Resampling.LANCZOS)
                    
                    img.save(output_file)
                    processed += 1
            except Exception as e:
                errors.append(f"{img_file.name}: {str(e)}")
        
        return {
            "success": True,
            "processed": processed,
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
        
        with Image.open(input_file) as img:
            file_size = Path(input_file).stat().st_size
            
            return {
                "success": True,
                "filename": Path(input_file).name,
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
        result = resize_image(sys.argv[2], sys.argv[3], int(sys.argv[4]), 
                               int(sys.argv[5]) if len(sys.argv) > 5 else None)
    elif command == "compress":
        if len(sys.argv) < 4:
            print("Error: compress requires input and output")
            sys.exit(1)
        quality = int(sys.argv[4]) if len(sys.argv) > 4 else 85
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
        result = batch_resize(sys.argv[2], sys.argv[3], int(sys.argv[4]))
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
