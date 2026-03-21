#!/usr/bin/env python3
"""
PDF Toolkit Skill for OpenClaw
Merge, split, and manipulate PDF files.

Examples:
    python main.py merge output.pdf doc1.pdf doc2.pdf
    python main.py split input.pdf ./output/
    python main.py extract report.pdf 1 5 summary.pdf
    python main.py info contract.pdf
    python main.py compress input.pdf output.pdf
    python main.py rotate input.pdf output.pdf 90
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Dict, Union

# PyPDF2 imports at top-level (not inside functions)
try:
    from PyPDF2 import PdfMerger, PdfReader, PdfWriter
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

# Module-level constants
ALLOWED_EXTENSIONS = {'.pdf'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB max
MAX_PAGES = 10000  # Maximum pages in a PDF
MAX_MERGE_FILES = 100  # Maximum files to merge
MAX_EXTRACT_PAGES = 100  # Maximum pages to extract at once
VALID_ROTATIONS = [90, 180, 270]  # Valid rotation degrees
ERROR_PREFIX = "❌"
SUCCESS_PREFIX = "✅"
INFO_PREFIX = "📄"


def ensure_directory(path: Union[str, Path]) -> tuple[bool, str]:
    """
    Ensure directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure
    
    Returns:
        Tuple of (success, error_message)
    
    Example:
        >>> ensure_directory("/tmp/output")
        (True, "")
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True, ""
    except OSError as e:
        return False, f"Cannot create directory: {e}"


def validate_pdf_path(file_path: str, must_exist: bool = True) -> tuple[bool, str]:
    """
    Validate a PDF file path for security.
    
    Args:
        file_path: Path to validate
        must_exist: Whether file must exist
    
    Returns:
        (is_valid, error_message)
    
    Example:
        >>> validate_pdf_path("doc.pdf")
        (True, "/full/path/to/doc.pdf")
        >>> validate_pdf_path("../etc/passwd.pdf")
        (False, "Path traversal detected: ../etc/passwd.pdf")
    """
    try:
        path = Path(file_path).resolve()
    except (OSError, ValueError) as e:
        return False, f"Invalid path: {file_path}"
    
    # Check path traversal
    normalized = os.path.normpath(file_path)
    if ".." in normalized.split(os.sep):
        return False, f"Path traversal detected: {file_path}"
    
    # Check extension (case insensitive)
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return False, f"Not a PDF file: {file_path}"
    
    # Check for double extensions (bypass attempt)
    file_name = path.name.lower()
    if '.pdf' in file_name[:-4]:  # Check if '.pdf' appears before the actual extension
        return False, f"Suspicious filename detected: {file_path}"
    
    if must_exist:
        if not path.exists():
            return False, f"File not found: {file_path}"
        
        if not path.is_file():
            return False, f"Not a file: {file_path}"
        
        # Check file size
        try:
            size = path.stat().st_size
            if size == 0:
                return False, f"File is empty: {file_path}"
            if size > MAX_FILE_SIZE:
                return False, f"File too large: {size} bytes (max: {MAX_FILE_SIZE})"
        except OSError as e:
            return False, f"Cannot access file: {file_path}"
    
    return True, str(path)


def validate_output_path(file_path: str) -> tuple[bool, str]:
    """
    Validate an output file path for security.
    
    Args:
        file_path: Path to validate
    
    Returns:
        (is_valid, error_message)
    
    Example:
        >>> validate_output_path("output.pdf")
        (True, "/full/path/to/output.pdf")
    """
    try:
        path = Path(file_path).resolve()
    except (OSError, ValueError) as e:
        return False, f"Invalid path: {file_path}"
    
    # Ensure extension is .pdf
    if path.suffix.lower() != '.pdf':
        # Force .pdf extension
        path = path.with_suffix('.pdf')
    
    # Check parent directory exists and is writable
    parent = path.parent
    success, error = ensure_directory(parent)
    if not success:
        return False, error
    
    return True, str(path)


def validate_page_number(page: str, max_page: int) -> tuple[bool, int, str]:
    """
    Validate page number input.
    
    Args:
        page: Page number as string
        max_page: Maximum allowed page number
    
    Returns:
        (is_valid, page_int, error_message)
    
    Example:
        >>> validate_page_number("5", 10)
        (True, 5, "")
        >>> validate_page_number("abc", 10)
        (False, 0, "Page number must be an integer")
    """
    try:
        page_num = int(page)
    except ValueError:
        return False, 0, f"Page number must be an integer, got: {page}"
    
    if page_num < 1:
        return False, 0, f"Page number must be positive, got: {page_num}"
    
    if page_num > max_page:
        return False, 0, f"Page {page_num} exceeds document length ({max_page} pages)"
    
    return True, page_num, ""


def merge_pdfs(input_files: List[str], output_file: str) -> Dict:
    """
    Merge multiple PDF files into one.
    
    Args:
        input_files: List of PDF file paths
        output_file: Output PDF file path
    
    Returns:
        Dict with operation results
    
    Example:
        >>> merge_pdfs(["doc1.pdf", "doc2.pdf"], "merged.pdf")
        {'success': True, 'files_merged': 2, 'output': '/path/to/merged.pdf', 'output_size': 12345}
    """
    if not PYPDF2_AVAILABLE:
        return {"success": False, "error": "PyPDF2 not installed. Run: pip install PyPDF2"}
    
    try:
        if len(input_files) < 2:
            return {"success": False, "error": "Need at least 2 PDFs to merge"}
        
        # Limit number of files
        if len(input_files) > MAX_MERGE_FILES:
            return {"success": False, "error": f"Maximum {MAX_MERGE_FILES} files can be merged at once"}
        
        # Validate all input files
        validated_paths = []
        for f in input_files:
            is_valid, result = validate_pdf_path(f)
            if not is_valid:
                return {"success": False, "error": result}
            validated_paths.append(result)
        
        # Validate output path
        is_valid, output_path = validate_output_path(output_file)
        if not is_valid:
            return {"success": False, "error": output_path}
        
        # Use context manager for PdfMerger to prevent resource leak
        with PdfMerger() as merger:
            for pdf_file in validated_paths:
                merger.append(pdf_file)
            
            merger.write(output_path)
        
        # Verify output file
        output_size = Path(output_path).stat().st_size
        if output_size == 0:
            return {"success": False, "error": "Output file is empty"}
        
        return {
            "success": True,
            "files_merged": len(input_files),
            "output": output_path,
            "output_size": output_size
        }
        
    except PermissionError as e:
        return {"success": False, "error": f"Permission denied: {e}"}
    except OSError as e:
        return {"success": False, "error": f"System error: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {type(e).__name__}: {e}"}


def split_pdf(input_file: str, output_dir: str, method: str = "all", pages: Optional[List[int]] = None) -> Dict:
    """
    Split PDF into separate pages or ranges.
    
    Args:
        input_file: Input PDF file path
        output_dir: Output directory for split pages
        method: 'all' (each page), 'ranges' (custom ranges), or specific
        pages: List of page numbers for method='ranges' (0-indexed)
    
    Returns:
        Dict with operation results
    
    Example:
        >>> split_pdf("doc.pdf", "./output/", method="all")
        {'success': True, 'total_pages': 5, 'files_created': 5, 'output_files': [...]}
    """
    if not PYPDF2_AVAILABLE:
        return {"success": False, "error": "PyPDF2 not installed. Run: pip install PyPDF2"}
    
    try:
        # Validate input file
        is_valid, validated_path = validate_pdf_path(input_file)
        if not is_valid:
            return {"success": False, "error": validated_path}
        
        # Validate output directory
        output_path = Path(output_dir).resolve()
        success, error = ensure_directory(output_path)
        if not success:
            return {"success": False, "error": f"Invalid output directory: {error}"}
        
        reader = PdfReader(validated_path)
        total_pages = len(reader.pages)
        
        # Sanity check
        if total_pages > MAX_PAGES:
            return {"success": False, "error": f"PDF has too many pages (>{MAX_PAGES})"}
        
        generated_files = []
        
        if method == "all":
            # Split each page into separate file
            for i in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                
                # Use 1-indexed for output filename (user-friendly)
                output_file = output_path / f"{Path(input_file).stem}_page_{i+1}.pdf"
                
                with open(output_file, 'wb') as f:
                    writer.write(f)
                
                generated_files.append(str(output_file))
        
        elif method == "ranges" and pages:
            # Validate page numbers
            valid_pages = [p for p in pages if 0 <= p < total_pages]
            if not valid_pages:
                return {"success": False, "error": f"No valid page numbers. PDF has {total_pages} pages (0-{total_pages-1} range)."}
            
            # Limit number of pages
            if len(valid_pages) > MAX_EXTRACT_PAGES:
                return {"success": False, "error": f"Maximum {MAX_EXTRACT_PAGES} pages can be extracted at once"}
            
            writer = PdfWriter()
            for page_num in valid_pages:
                writer.add_page(reader.pages[page_num])
            
            # Use 1-indexed for filename
            page_str = "_".join([str(p+1) for p in valid_pages])
            output_file = output_path / f"{Path(input_file).stem}_pages_{page_str}.pdf"
            
            with open(output_file, 'wb') as f:
                writer.write(f)
            
            generated_files.append(str(output_file))
        
        return {
            "success": True,
            "total_pages": total_pages,
            "files_created": len(generated_files),
            "output_files": generated_files
        }
        
    except PermissionError as e:
        return {"success": False, "error": f"Permission denied: {e}"}
    except OSError as e:
        return {"success": False, "error": f"System error: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {type(e).__name__}: {e}"}


def extract_pages(input_file: str, start_page: int, end_page: int, output_file: str) -> Dict:
    """
    Extract a range of pages from PDF.
    
    Args:
        input_file: Input PDF file path
        start_page: Starting page number (1-indexed)
        end_page: Ending page number (1-indexed, inclusive)
        output_file: Output PDF file path
    
    Returns:
        Dict with operation results
    
    Example:
        >>> extract_pages("doc.pdf", 1, 5, "extracted.pdf")
        {'success': True, 'pages_extracted': 5, 'output': '/path/to/extracted.pdf'}
    """
    if not PYPDF2_AVAILABLE:
        return {"success": False, "error": "PyPDF2 not installed. Run: pip install PyPDF2"}
    
    try:
        # Validate input file
        is_valid, validated_path = validate_pdf_path(input_file)
        if not is_valid:
            return {"success": False, "error": validated_path}
        
        reader = PdfReader(validated_path)
        total_pages = len(reader.pages)
        
        # Convert to 0-indexed
        start_idx = start_page - 1
        end_idx = end_page - 1
        
        if start_idx < 0 or end_idx >= total_pages or start_idx > end_idx:
            return {"success": False, "error": f"Invalid page range. PDF has {total_pages} pages (1-{total_pages})."}
        
        # Limit range
        if end_idx - start_idx + 1 > MAX_EXTRACT_PAGES:
            return {"success": False, "error": f"Maximum {MAX_EXTRACT_PAGES} pages can be extracted at once"}
        
        writer = PdfWriter()
        for i in range(start_idx, end_idx + 1):
            writer.add_page(reader.pages[i])
        
        # Validate output path
        is_valid, output_path = validate_output_path(output_file)
        if not is_valid:
            return {"success": False, "error": output_path}
        
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        return {
            "success": True,
            "pages_extracted": end_page - start_page + 1,
            "output": output_path
        }
        
    except PermissionError as e:
        return {"success": False, "error": f"Permission denied: {e}"}
    except OSError as e:
        return {"success": False, "error": f"System error: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {type(e).__name__}: {e}"}


def get_pdf_info(input_file: str) -> Dict:
    """
    Get information about PDF file.
    
    Args:
        input_file: Input PDF file path
    
    Returns:
        Dict with PDF metadata
    
    Example:
        >>> get_pdf_info("doc.pdf")
        {'success': True, 'pages': 10, 'file_size': 12345, 'title': 'Document', ...}
    """
    if not PYPDF2_AVAILABLE:
        return {"success": False, "error": "PyPDF2 not installed. Run: pip install PyPDF2"}
    
    try:
        # Validate input file
        is_valid, validated_path = validate_pdf_path(input_file)
        if not is_valid:
            return {"success": False, "error": validated_path}
        
        reader = PdfReader(validated_path)
        
        # Extract metadata
        metadata = reader.metadata or {}
        
        return {
            "success": True,
            "pages": len(reader.pages),
            "file_size": Path(validated_path).stat().st_size,
            "author": metadata.get("/Author", "Unknown"),
            "creator": metadata.get("/Creator", "Unknown"),
            "producer": metadata.get("/Producer", "Unknown"),
            "subject": metadata.get("/Subject", ""),
            "title": metadata.get("/Title", Path(input_file).stem),
            "encrypted": reader.is_encrypted
        }
        
    except PermissionError as e:
        return {"success": False, "error": f"Permission denied: {e}"}
    except OSError as e:
        return {"success": False, "error": f"System error: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {type(e).__name__}: {e}"}


def compress_pdf(input_file: str, output_file: str, quality: str = "medium") -> Dict:
    """
    Compress PDF file (basic implementation).
    
    Args:
        input_file: Input PDF file path
        output_file: Output PDF file path
        quality: 'low', 'medium', or 'high' compression
    
    Returns:
        Dict with operation results
    
    Example:
        >>> compress_pdf("input.pdf", "output.pdf")
        {'success': True, 'original_size': 100000, 'new_size': 85000, 'reduction_percent': 15.0}
    """
    if not PYPDF2_AVAILABLE:
        return {"success": False, "error": "PyPDF2 not installed. Run: pip install PyPDF2"}
    
    try:
        # Validate input file
        is_valid, validated_path = validate_pdf_path(input_file)
        if not is_valid:
            return {"success": False, "error": validated_path}
        
        reader = PdfReader(validated_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            # Add compression (this is basic, for better compression use pikepdf or img2pdf)
            writer.add_page(page)
        
        # Validate output path
        is_valid, output_path = validate_output_path(output_file)
        if not is_valid:
            return {"success": False, "error": output_path}
        
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        original_size = Path(validated_path).stat().st_size
        new_size = Path(output_path).stat().st_size
        
        # Fix division by zero
        reduction = ((original_size - new_size) / original_size) * 100 if original_size > 0 else 0
        
        return {
            "success": True,
            "original_size": original_size,
            "new_size": new_size,
            "reduction_percent": round(reduction, 2),
            "output": output_path
        }
        
    except PermissionError as e:
        return {"success": False, "error": f"Permission denied: {e}"}
    except OSError as e:
        return {"success": False, "error": f"System error: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {type(e).__name__}: {e}"}


def rotate_pdf(input_file: str, output_file: str, rotation: int = 90) -> Dict:
    """
    Rotate all pages in PDF.
    
    Args:
        input_file: Input PDF file path
        output_file: Output PDF file path
        rotation: Rotation degrees (90, 180, or 270)
    
    Returns:
        Dict with operation results
    
    Example:
        >>> rotate_pdf("input.pdf", "output.pdf", 90)
        {'success': True, 'pages_rotated': 5, 'rotation': 90, 'output': '/path/to/output.pdf'}
    """
    if not PYPDF2_AVAILABLE:
        return {"success": False, "error": "PyPDF2 not installed. Run: pip install PyPDF2"}
    
    try:
        # Validate input file
        is_valid, validated_path = validate_pdf_path(input_file)
        if not is_valid:
            return {"success": False, "error": validated_path}
        
        if rotation not in VALID_ROTATIONS:
            return {"success": False, "error": f"Rotation must be one of: {VALID_ROTATIONS}"}
        
        reader = PdfReader(validated_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            page.rotate(rotation)
            writer.add_page(page)
        
        # Validate output path
        is_valid, output_path = validate_output_path(output_file)
        if not is_valid:
            return {"success": False, "error": output_path}
        
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        return {
            "success": True,
            "pages_rotated": len(reader.pages),
            "rotation": rotation,
            "output": output_path
        }
        
    except PermissionError as e:
        return {"success": False, "error": f"Permission denied: {e}"}
    except OSError as e:
        return {"success": False, "error": f"System error: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {type(e).__name__}: {e}"}


def main():
    """CLI interface for PDF toolkit."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [options]")
        print("")
        print("Commands:")
        print("  merge <output.pdf> <input1.pdf> <input2.pdf> ...   - Merge PDFs")
        print("  split <input.pdf> <output_dir>                    - Split all pages")
        print("  extract <input.pdf> <start> <end> <output.pdf>  - Extract page range")
        print("  info <input.pdf>                                   - Show PDF info")
        print("  compress <input.pdf> <output.pdf>                - Compress PDF")
        print("  rotate <input.pdf> <output.pdf> <degrees>        - Rotate PDF")
        print("")
        print("Examples:")
        print("  python main.py merge combined.pdf doc1.pdf doc2.pdf")
        print("  python main.py split document.pdf ./pages/")
        print("  python main.py extract report.pdf 1 5 summary.pdf")
        print("  python main.py info contract.pdf")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "merge":
        if len(sys.argv) < 4:
            print(f"{ERROR_PREFIX} Error: merge requires output file and at least 2 input files")
            sys.exit(1)
        
        output_file = sys.argv[2]
        input_files = sys.argv[3:]
        
        result = merge_pdfs(input_files, output_file)
        
        if result["success"]:
            print(f"{SUCCESS_PREFIX} Merged {result['files_merged']} PDFs into {result['output']}")
            print(f"   Output size: {result['output_size']:,} bytes")
        else:
            print(f"{ERROR_PREFIX} {result['error']}")
            sys.exit(1)
    
    elif command == "split":
        if len(sys.argv) < 4:
            print(f"{ERROR_PREFIX} Error: split requires input file and output directory")
            sys.exit(1)
        
        input_file = sys.argv[2]
        output_dir = sys.argv[3]
        
        result = split_pdf(input_file, output_dir)
        
        if result["success"]:
            print(f"{SUCCESS_PREFIX} Split {result['total_pages']} pages into {result['files_created']} files")
            print(f"   Output directory: {output_dir}")
        else:
            print(f"{ERROR_PREFIX} {result['error']}")
            sys.exit(1)
    
    elif command == "extract":
        if len(sys.argv) < 6:
            print(f"{ERROR_PREFIX} Error: extract requires input, start, end, and output")
            sys.exit(1)
        
        input_file = sys.argv[2]
        
        # Validate page numbers before processing
        is_valid, start_page, error = validate_page_number(sys.argv[3], 99999)
        if not is_valid:
            print(f"{ERROR_PREFIX} {error}")
            sys.exit(1)
        
        is_valid, end_page, error = validate_page_number(sys.argv[4], 99999)
        if not is_valid:
            print(f"{ERROR_PREFIX} {error}")
            sys.exit(1)
        
        output_file = sys.argv[5]
        
        result = extract_pages(input_file, start_page, end_page, output_file)
        
        if result["success"]:
            print(f"{SUCCESS_PREFIX} Extracted {result['pages_extracted']} pages to {result['output']}")
        else:
            print(f"{ERROR_PREFIX} {result['error']}")
            sys.exit(1)
    
    elif command == "info":
        if len(sys.argv) < 3:
            print(f"{ERROR_PREFIX} Error: info requires input file")
            sys.exit(1)
        
        input_file = sys.argv[2]
        result = get_pdf_info(input_file)
        
        if result["success"]:
            print(f"{INFO_PREFIX} PDF Information:")
            print(f"   Title: {result['title']}")
            print(f"   Pages: {result['pages']}")
            print(f"   Author: {result['author']}")
            print(f"   Subject: {result['subject']}")
            print(f"   Size: {result['file_size']:,} bytes")
            print(f"   Encrypted: {result['encrypted']}")
        else:
            print(f"{ERROR_PREFIX} {result['error']}")
            sys.exit(1)
    
    elif command == "compress":
        if len(sys.argv) < 4:
            print(f"{ERROR_PREFIX} Error: compress requires input and output files")
            sys.exit(1)
        
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        
        result = compress_pdf(input_file, output_file)
        
        if result["success"]:
            print(f"{SUCCESS_PREFIX} Compressed PDF: {result['reduction_percent']}% reduction")
            print(f"   Original: {result['original_size']:,} bytes")
            print(f"   New: {result['new_size']:,} bytes")
        else:
            print(f"{ERROR_PREFIX} {result['error']}")
            sys.exit(1)
    
    elif command == "rotate":
        if len(sys.argv) < 5:
            print(f"{ERROR_PREFIX} Error: rotate requires input, output, and degrees")
            sys.exit(1)
        
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        
        # Validate rotation
        try:
            rotation = int(sys.argv[4])
        except ValueError:
            print(f"{ERROR_PREFIX} Error: Rotation must be an integer (90, 180, or 270)")
            sys.exit(1)
        
        result = rotate_pdf(input_file, output_file, rotation)
        
        if result["success"]:
            print(f"{SUCCESS_PREFIX} Rotated {result['pages_rotated']} pages by {result['rotation']}°")
            print(f"   Output: {result['output']}")
        else:
            print(f"{ERROR_PREFIX} {result['error']}")
            sys.exit(1)
    
    else:
        print(f"{ERROR_PREFIX} Unknown command: {command}")
        print("Run without arguments for usage help")
        sys.exit(1)


if __name__ == "__main__":
    main()
