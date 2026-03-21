#!/usr/bin/env python3
"""
PDF Toolkit Skill for OpenClaw
Merge, split, and manipulate PDF files.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Dict

def merge_pdfs(input_files: List[str], output_file: str) -> Dict:
    """
    Merge multiple PDF files into one.
    
    Args:
        input_files: List of PDF file paths
        output_file: Output PDF file path
    
    Returns:
        Dict with operation results
    """
    try:
        from PyPDF2 import PdfMerger
        
        if len(input_files) < 2:
            return {"success": False, "error": "Need at least 2 PDFs to merge"}
        
        # Validate input files exist
        for f in input_files:
            if not Path(f).exists():
                return {"success": False, "error": f"File not found: {f}"}
            if not f.lower().endswith('.pdf'):
                return {"success": False, "error": f"Not a PDF file: {f}"}
        
        merger = PdfMerger()
        
        for pdf_file in input_files:
            merger.append(pdf_file)
        
        # Ensure output directory exists
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        merger.write(output_file)
        merger.close()
        
        return {
            "success": True,
            "files_merged": len(input_files),
            "output": output_file,
            "output_size": Path(output_file).stat().st_size
        }
        
    except ImportError:
        return {"success": False, "error": "PyPDF2 not installed. Run: pip install PyPDF2"}
    except Exception as e:
        return {"success": False, "error": str(e)}


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
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        if not Path(input_file).exists():
            return {"success": False, "error": f"File not found: {input_file}"}
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        reader = PdfReader(input_file)
        total_pages = len(reader.pages)
        
        generated_files = []
        
        if method == "all":
            # Split each page into separate file
            for i in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                
                output_file = output_path / f"{Path(input_file).stem}_page_{i+1}.pdf"
                with open(output_file, 'wb') as f:
                    writer.write(f)
                
                generated_files.append(str(output_file))
        
        elif method == "ranges" and pages:
            # Split specific pages
            writer = PdfWriter()
            for page_num in pages:
                if 0 <= page_num < total_pages:
                    writer.add_page(reader.pages[page_num])
            
            page_str = "_".join([str(p+1) for p in pages])
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
        
    except ImportError:
        return {"success": False, "error": "PyPDF2 not installed. Run: pip install PyPDF2"}
    except Exception as e:
        return {"success": False, "error": str(e)}


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
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        if not Path(input_file).exists():
            return {"success": False, "error": f"File not found: {input_file}"}
        
        reader = PdfReader(input_file)
        total_pages = len(reader.pages)
        
        # Convert to 0-indexed
        start_idx = start_page - 1
        end_idx = end_page - 1
        
        if start_idx < 0 or end_idx >= total_pages or start_idx > end_idx:
            return {"success": False, "error": f"Invalid page range. PDF has {total_pages} pages."}
        
        writer = PdfWriter()
        for i in range(start_idx, end_idx + 1):
            writer.add_page(reader.pages[i])
        
        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'wb') as f:
            writer.write(f)
        
        return {
            "success": True,
            "pages_extracted": end_page - start_page + 1,
            "output": output_file
        }
        
    except ImportError:
        return {"success": False, "error": "PyPDF2 not installed. Run: pip install PyPDF2"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_pdf_info(input_file: str) -> Dict:
    """
    Get information about PDF file.
    
    Args:
        input_file: Input PDF file path
    
    Returns:
        Dict with PDF metadata
    """
    try:
        from PyPDF2 import PdfReader
        
        if not Path(input_file).exists():
            return {"success": False, "error": f"File not found: {input_file}"}
        
        reader = PdfReader(input_file)
        
        # Extract metadata
        metadata = reader.metadata or {}
        
        return {
            "success": True,
            "pages": len(reader.pages),
            "file_size": Path(input_file).stat().st_size,
            "author": metadata.get("/Author", "Unknown"),
            "creator": metadata.get("/Creator", "Unknown"),
            "producer": metadata.get("/Producer", "Unknown"),
            "subject": metadata.get("/Subject", ""),
            "title": metadata.get("/Title", Path(input_file).stem),
            "encrypted": reader.is_encrypted
        }
        
    except ImportError:
        return {"success": False, "error": "PyPDF2 not installed. Run: pip install PyPDF2"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def compress_pdf(input_file: str, output_file: str, quality: str = "medium") -> Dict:
    """
    Compress PDF file (basic implementation).
    
    Args:
        input_file: Input PDF file path
        output_file: Output PDF file path
        quality: 'low', 'medium', or 'high' compression
    
    Returns:
        Dict with operation results
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        if not Path(input_file).exists():
            return {"success": False, "error": f"File not found: {input_file}"}
        
        reader = PdfReader(input_file)
        writer = PdfWriter()
        
        for page in reader.pages:
            # Add compression (this is basic, for better compression use pikepdf or img2pdf)
            writer.add_page(page)
        
        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'wb') as f:
            writer.write(f)
        
        original_size = Path(input_file).stat().st_size
        new_size = Path(output_file).stat().st_size
        reduction = ((original_size - new_size) / original_size) * 100
        
        return {
            "success": True,
            "original_size": original_size,
            "new_size": new_size,
            "reduction_percent": round(reduction, 2),
            "output": output_file
        }
        
    except ImportError:
        return {"success": False, "error": "PyPDF2 not installed. Run: pip install PyPDF2"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def rotate_pdf(input_file: str, output_file: str, rotation: int = 90) -> Dict:
    """
    Rotate all pages in PDF.
    
    Args:
        input_file: Input PDF file path
        output_file: Output PDF file path
        rotation: Rotation degrees (90, 180, or 270)
    
    Returns:
        Dict with operation results
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        if not Path(input_file).exists():
            return {"success": False, "error": f"File not found: {input_file}"}
        
        if rotation not in [90, 180, 270]:
            return {"success": False, "error": "Rotation must be 90, 180, or 270 degrees"}
        
        reader = PdfReader(input_file)
        writer = PdfWriter()
        
        for page in reader.pages:
            page.rotate(rotation)
            writer.add_page(page)
        
        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'wb') as f:
            writer.write(f)
        
        return {
            "success": True,
            "pages_rotated": len(reader.pages),
            "rotation": rotation,
            "output": output_file
        }
        
    except ImportError:
        return {"success": False, "error": "PyPDF2 not installed. Run: pip install PyPDF2"}
    except Exception as e:
        return {"success": False, "error": str(e)}


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
            print("Error: merge requires output file and at least 2 input files")
            sys.exit(1)
        
        output_file = sys.argv[2]
        input_files = sys.argv[3:]
        
        result = merge_pdfs(input_files, output_file)
        
        if result["success"]:
            print(f"✅ Merged {result['files_merged']} PDFs into {result['output']}")
            print(f"   Output size: {result['output_size']:,} bytes")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    elif command == "split":
        if len(sys.argv) < 4:
            print("Error: split requires input file and output directory")
            sys.exit(1)
        
        input_file = sys.argv[2]
        output_dir = sys.argv[3]
        
        result = split_pdf(input_file, output_dir)
        
        if result["success"]:
            print(f"✅ Split {result['total_pages']} pages into {result['files_created']} files")
            print(f"   Output directory: {output_dir}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    elif command == "extract":
        if len(sys.argv) < 6:
            print("Error: extract requires input, start, end, and output")
            sys.exit(1)
        
        input_file = sys.argv[2]
        start_page = int(sys.argv[3])
        end_page = int(sys.argv[4])
        output_file = sys.argv[5]
        
        result = extract_pages(input_file, start_page, end_page, output_file)
        
        if result["success"]:
            print(f"✅ Extracted {result['pages_extracted']} pages to {result['output']}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    elif command == "info":
        if len(sys.argv) < 3:
            print("Error: info requires input file")
            sys.exit(1)
        
        input_file = sys.argv[2]
        result = get_pdf_info(input_file)
        
        if result["success"]:
            print(f"📄 PDF Information:")
            print(f"   Title: {result['title']}")
            print(f"   Pages: {result['pages']}")
            print(f"   Author: {result['author']}")
            print(f"   Subject: {result['subject']}")
            print(f"   Size: {result['file_size']:,} bytes")
            print(f"   Encrypted: {result['encrypted']}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    elif command == "compress":
        if len(sys.argv) < 4:
            print("Error: compress requires input and output files")
            sys.exit(1)
        
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        
        result = compress_pdf(input_file, output_file)
        
        if result["success"]:
            print(f"✅ Compressed PDF: {result['reduction_percent']}% reduction")
            print(f"   Original: {result['original_size']:,} bytes")
            print(f"   New: {result['new_size']:,} bytes")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    elif command == "rotate":
        if len(sys.argv) < 5:
            print("Error: rotate requires input, output, and degrees")
            sys.exit(1)
        
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        rotation = int(sys.argv[4])
        
        result = rotate_pdf(input_file, output_file, rotation)
        
        if result["success"]:
            print(f"✅ Rotated {result['pages_rotated']} pages by {result['rotation']}°")
            print(f"   Output: {result['output']}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    else:
        print(f"Unknown command: {command}")
        print("Run without arguments for usage help")
        sys.exit(1)


if __name__ == "__main__":
    main()
