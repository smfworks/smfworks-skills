#!/usr/bin/env python3
"""
File Organizer Skill for OpenClaw
Organizes files in a directory by date, type, or custom patterns.
"""

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import hashlib


def get_file_hash(filepath: str) -> str:
    """Calculate MD5 hash of file for duplicate detection."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def organize_by_date(source_dir: str, dest_dir: Optional[str] = None) -> Dict:
    """
    Organize files by modification date into YYYY/MM folders.
    
    Args:
        source_dir: Directory to organize
        dest_dir: Destination directory (optional, defaults to source_dir)
    
    Returns:
        Dict with operation results
    """
    if dest_dir is None:
        dest_dir = source_dir
    
    source_path = Path(source_dir).resolve()
    dest_path = Path(dest_dir).resolve()
    
    if not source_path.exists():
        return {"success": False, "error": f"Source directory does not exist: {source_dir}"}
    
    if not source_path.is_dir():
        return {"success": False, "error": f"Source is not a directory: {source_dir}"}
    
    # Security: Prevent operating on system directories
    system_dirs = ["/", "/bin", "/sbin", "/usr", "/etc", "/var", "/sys", "/proc", "/dev"]
    if str(source_path) in system_dirs:
        return {"success": False, "error": "Cannot operate on system directories"}
    
    results = {
        "success": True,
        "files_moved": 0,
        "errors": [],
        "organized_by": {}
    }
    
    try:
        # Get all files (not directories) in source
        files = [f for f in source_path.iterdir() if f.is_file()]
        
        for file_path in files:
            try:
                # Get file modification date
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                year_month = mtime.strftime("%Y/%m")
                
                # Create destination directory
                dest_subdir = dest_path / year_month
                dest_subdir.mkdir(parents=True, exist_ok=True)
                
                # Move file
                dest_file = dest_subdir / file_path.name
                
                # Handle name collisions
                counter = 1
                original_dest = dest_file
                while dest_file.exists():
                    stem = original_dest.stem
                    suffix = original_dest.suffix
                    dest_file = original_dest.parent / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                shutil.move(str(file_path), str(dest_file))
                
                results["files_moved"] += 1
                if year_month not in results["organized_by"]:
                    results["organized_by"][year_month] = 0
                results["organized_by"][year_month] += 1
                
            except Exception as e:
                results["errors"].append(f"Error moving {file_path.name}: {str(e)}")
        
        return results
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def organize_by_type(source_dir: str, dest_dir: Optional[str] = None) -> Dict:
    """
    Organize files by type (extension) into folders.
    
    Args:
        source_dir: Directory to organize
        dest_dir: Destination directory (optional)
    
    Returns:
        Dict with operation results
    """
    if dest_dir is None:
        dest_dir = source_dir
    
    source_path = Path(source_dir).resolve()
    dest_path = Path(dest_dir).resolve()
    
    if not source_path.exists():
        return {"success": False, "error": f"Source directory does not exist: {source_dir}"}
    
    # Security check
    system_dirs = ["/", "/bin", "/sbin", "/usr", "/etc", "/var", "/sys", "/proc", "/dev"]
    if str(source_path) in system_dirs:
        return {"success": False, "error": "Cannot operate on system directories"}
    
    # File type categories
    type_map = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"],
        "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
        "Presentations": [".ppt", ".pptx", ".odp", ".key"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".go", ".rs", ".rb", ".php"],
        "Data": [".json", ".xml", ".yaml", ".yml", ".sql", ".db"]
    }
    
    results = {
        "success": True,
        "files_moved": 0,
        "errors": [],
        "organized_by": {}
    }
    
    try:
        files = [f for f in source_path.iterdir() if f.is_file()]
        
        for file_path in files:
            try:
                # Determine file type
                ext = file_path.suffix.lower()
                category = "Other"
                
                for cat, extensions in type_map.items():
                    if ext in extensions:
                        category = cat
                        break
                
                # Create category directory
                dest_subdir = dest_path / category
                dest_subdir.mkdir(parents=True, exist_ok=True)
                
                # Move file
                dest_file = dest_subdir / file_path.name
                
                # Handle collisions
                counter = 1
                original_dest = dest_file
                while dest_file.exists():
                    stem = original_dest.stem
                    suffix = original_dest.suffix
                    dest_file = original_dest.parent / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                shutil.move(str(file_path), str(dest_file))
                
                results["files_moved"] += 1
                if category not in results["organized_by"]:
                    results["organized_by"][category] = 0
                results["organized_by"][category] += 1
                
            except Exception as e:
                results["errors"].append(f"Error moving {file_path.name}: {str(e)}")
        
        return results
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def find_duplicates(directory: str) -> Dict:
    """
    Find duplicate files by hash.
    
    Args:
        directory: Directory to scan
    
    Returns:
        Dict with duplicate groups
    """
    dir_path = Path(directory).resolve()
    
    if not dir_path.exists():
        return {"success": False, "error": f"Directory does not exist: {directory}"}
    
    hashes: Dict[str, List[str]] = {}
    
    try:
        # Walk directory
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                try:
                    file_hash = get_file_hash(str(file_path))
                    if file_hash not in hashes:
                        hashes[file_hash] = []
                    hashes[file_hash].append(str(file_path))
                except Exception:
                    continue  # Skip files we can't read
        
        # Filter to only duplicates
        duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
        
        return {
            "success": True,
            "duplicates_found": len(duplicates),
            "duplicate_groups": duplicates,
            "total_duplicate_files": sum(len(paths) for paths in duplicates.values())
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    """CLI interface for file organizer."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [options]")
        print("")
        print("Commands:")
        print("  organize-date <directory> [dest_directory]  - Organize by date")
        print("  organize-type <directory> [dest_directory]  - Organize by file type")
        print("  find-duplicates <directory>               - Find duplicate files")
        print("")
        print("Examples:")
        print("  python main.py organize-date ~/Downloads")
        print("  python main.py organize-type ~/Documents ~/Organized")
        print("  python main.py find-duplicates ~/Pictures")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "organize-date":
        if len(sys.argv) < 3:
            print("Error: Directory required")
            sys.exit(1)
        
        source = sys.argv[2]
        dest = sys.argv[3] if len(sys.argv) > 3 else None
        
        result = organize_by_date(source, dest)
        
        if result["success"]:
            print(f"✅ Organized {result['files_moved']} files by date")
            if result["organized_by"]:
                print("\nOrganized into:")
                for folder, count in sorted(result["organized_by"].items()):
                    print(f"  {folder}: {count} files")
            if result["errors"]:
                print(f"\n⚠️  {len(result['errors'])} errors")
                for error in result["errors"][:5]:  # Show first 5
                    print(f"  - {error}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    elif command == "organize-type":
        if len(sys.argv) < 3:
            print("Error: Directory required")
            sys.exit(1)
        
        source = sys.argv[2]
        dest = sys.argv[3] if len(sys.argv) > 3 else None
        
        result = organize_by_type(source, dest)
        
        if result["success"]:
            print(f"✅ Organized {result['files_moved']} files by type")
            if result["organized_by"]:
                print("\nOrganized into:")
                for category, count in sorted(result["organized_by"].items(), key=lambda x: -x[1]):
                    print(f"  {category}: {count} files")
            if result["errors"]:
                print(f"\n⚠️  {len(result['errors'])} errors")
                for error in result["errors"][:5]:
                    print(f"  - {error}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    elif command == "find-duplicates":
        if len(sys.argv) < 3:
            print("Error: Directory required")
            sys.exit(1)
        
        directory = sys.argv[2]
        result = find_duplicates(directory)
        
        if result["success"]:
            print(f"🔍 Found {result['duplicates_found']} duplicate groups")
            print(f"   Total duplicate files: {result['total_duplicate_files']}")
            
            if result["duplicates_found"] > 0:
                print("\nDuplicate groups:")
                for hash_val, paths in result["duplicate_groups"].items():
                    print(f"\n  Hash: {hash_val[:16]}...")
                    for path in paths:
                        print(f"    - {path}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    else:
        print(f"Unknown command: {command}")
        print("Run without arguments for usage help")
        sys.exit(1)


if __name__ == "__main__":
    main()
