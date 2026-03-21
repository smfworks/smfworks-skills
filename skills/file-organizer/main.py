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


# Maximum allowed file size for processing (100MB)
MAX_FILE_SIZE = 100 * 1024 * 1024

# Maximum allowed counter for duplicate handling
MAX_DUPLICATE_COUNTER = 1000


def is_safe_path(base_path: Path, target_path: Path) -> bool:
    """
    Verify that target_path is within base_path to prevent path traversal.
    """
    try:
        # Resolve both paths to absolute, normalized paths
        base = base_path.resolve()
        target = target_path.resolve()
        
        # Check if target starts with base path
        return str(target).startswith(str(base))
    except (OSError, ValueError):
        return False


def validate_source_path(source_dir: str) -> tuple[bool, Path, Optional[str]]:
    """
    Validate and sanitize the source directory path.
    Returns (is_valid, resolved_path, error_message).
    """
    try:
        source_path = Path(source_dir).resolve()
    except (OSError, ValueError) as e:
        return False, Path(), f"Invalid path: {source_dir}"
    
    # Check if path exists
    if not source_path.exists():
        return False, source_path, f"Source directory does not exist: {source_dir}"
    
    if not source_path.is_dir():
        return False, source_path, f"Source is not a directory: {source_dir}"
    
    # Security: Prevent operating on system directories
    system_dirs = ["/", "/bin", "/sbin", "/usr", "/etc", "/var", "/sys", "/proc", "/dev", "/boot", "/lib", "/lib64"]
    source_str = str(source_path)
    for sys_dir in system_dirs:
        if source_str == sys_dir or source_str.startswith(sys_dir + "/"):
            return False, source_path, f"Cannot operate on system directory: {source_dir}"
    
    # Check for path traversal attempts
    normalized = os.path.normpath(source_dir)
    if ".." in normalized.split(os.sep):
        return False, source_path, f"Path traversal detected: {source_dir}"
    
    return True, source_path, None


def validate_destination_path(dest_dir: str, source_path: Path) -> tuple[bool, Path, Optional[str]]:
    """
    Validate and sanitize the destination directory path.
    Prevents destination escape attacks.
    """
    try:
        dest_path = Path(dest_dir).resolve()
    except (OSError, ValueError) as e:
        return False, Path(), f"Invalid destination path: {dest_dir}"
    
    # Ensure destination is within allowed workspace
    # If destination is absolute, ensure it's within home or temp
    dest_str = str(dest_path)
    home = str(Path.home().resolve())
    allowed_roots = [home, "/tmp", "/var/tmp"]
    
    allowed = any(dest_str.startswith(root) for root in allowed_roots)
    if not allowed and dest_path.is_absolute():
        return False, dest_path, f"Destination must be within home directory or temp: {dest_dir}"
    
    return True, dest_path, None


def get_file_hash(filepath: str) -> Optional[str]:
    """
    Calculate MD5 hash of file for duplicate detection.
    Returns None if file is too large or cannot be read.
    """
    try:
        file_size = Path(filepath).stat().st_size
        if file_size > MAX_FILE_SIZE:
            return None  # Skip large files
        
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except (OSError, IOError, PermissionError):
        return None


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
    
    # Validate source path
    is_valid, source_path, error = validate_source_path(source_dir)
    if not is_valid:
        return {"success": False, "error": error}
    
    # Validate destination path
    is_valid, dest_path, error = validate_destination_path(dest_dir, source_path)
    if not is_valid:
        return {"success": False, "error": error}
    
    # Ensure destination is not escaping from source
    if dest_dir != source_dir and not is_safe_path(source_path, dest_path):
        return {"success": False, "error": "Destination path escape attempt detected"}
    
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
                # Check file size
                file_size = file_path.stat().st_size
                if file_size > MAX_FILE_SIZE:
                    results["errors"].append(f"Skipped large file {file_path.name}: {file_size} bytes")
                    continue
                
                # Get file modification date
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                year_month = mtime.strftime("%Y/%m")
                
                # Create destination directory
                dest_subdir = dest_path / year_month
                dest_subdir.mkdir(parents=True, exist_ok=True)
                
                # Verify destination is still safe after mkdir
                if not is_safe_path(dest_path, dest_subdir):
                    results["errors"].append(f"Security violation for {file_path.name}")
                    continue
                
                # Move file
                dest_file = dest_subdir / file_path.name
                
                # Handle name collisions with bounded counter
                counter = 1
                original_dest = dest_file
                while dest_file.exists() and counter <= MAX_DUPLICATE_COUNTER:
                    stem = original_dest.stem
                    suffix = original_dest.suffix
                    dest_file = original_dest.parent / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                if counter > MAX_DUPLICATE_COUNTER:
                    results["errors"].append(f"Too many duplicates for {file_path.name}")
                    continue
                
                # Verify final destination is safe
                if not is_safe_path(dest_path, dest_file):
                    results["errors"].append(f"Destination escape detected for {file_path.name}")
                    continue
                
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
    
    # Validate source path
    is_valid, source_path, error = validate_source_path(source_dir)
    if not is_valid:
        return {"success": False, "error": error}
    
    # Validate destination path
    is_valid, dest_path, error = validate_destination_path(dest_dir, source_path)
    if not is_valid:
        return {"success": False, "error": error}
    
    # Ensure destination is not escaping from source
    if dest_dir != source_dir and not is_safe_path(source_path, dest_path):
        return {"success": False, "error": "Destination path escape attempt detected"}
    
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
                # Check file size
                file_size = file_path.stat().st_size
                if file_size > MAX_FILE_SIZE:
                    results["errors"].append(f"Skipped large file {file_path.name}: {file_size} bytes")
                    continue
                
                # Determine file type
                ext = file_path.suffix.lower()
                category = "Other"
                
                for cat, extensions in type_map.items():
                    if ext in extensions:
                        category = cat
                        break
                
                # Sanitize category name for directory
                safe_category = "".join(c for c in category if c.isalnum() or c in " -_").strip()
                if not safe_category:
                    safe_category = "Other"
                
                # Create category directory
                dest_subdir = dest_path / safe_category
                dest_subdir.mkdir(parents=True, exist_ok=True)
                
                # Verify destination is still safe after mkdir
                if not is_safe_path(dest_path, dest_subdir):
                    results["errors"].append(f"Security violation for {file_path.name}")
                    continue
                
                # Move file
                dest_file = dest_subdir / file_path.name
                
                # Handle collisions with bounded counter
                counter = 1
                original_dest = dest_file
                while dest_file.exists() and counter <= MAX_DUPLICATE_COUNTER:
                    stem = original_dest.stem
                    suffix = original_dest.suffix
                    dest_file = original_dest.parent / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                if counter > MAX_DUPLICATE_COUNTER:
                    results["errors"].append(f"Too many duplicates for {file_path.name}")
                    continue
                
                # Verify final destination is safe
                if not is_safe_path(dest_path, dest_file):
                    results["errors"].append(f"Destination escape detected for {file_path.name}")
                    continue
                
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
    # Validate directory
    is_valid, dir_path, error = validate_source_path(directory)
    if not is_valid:
        return {"success": False, "error": error}
    
    hashes: Dict[str, List[str]] = {}
    errors = []
    
    try:
        # Walk directory with depth limit to prevent excessive traversal
        max_depth = 10
        current_depth = 0
        
        for root, dirs, files in os.walk(dir_path):
            current_depth = root.replace(str(dir_path), "").count(os.sep)
            if current_depth >= max_depth:
                del dirs[:]  # Don't go deeper
                continue
            
            for filename in files:
                file_path = Path(root) / filename
                try:
                    # Skip symlinks to prevent cycles
                    if file_path.is_symlink():
                        continue
                    
                    # Skip large files
                    file_size = file_path.stat().st_size
                    if file_size > MAX_FILE_SIZE:
                        continue
                    
                    file_hash = get_file_hash(str(file_path))
                    if file_hash is None:
                        continue
                    
                    if file_hash not in hashes:
                        hashes[file_hash] = []
                    hashes[file_hash].append(str(file_path))
                except (OSError, IOError, PermissionError):
                    errors.append(f"Cannot read: {file_path}")
                    continue
        
        # Filter to only duplicates
        duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
        
        return {
            "success": True,
            "duplicates_found": len(duplicates),
            "duplicate_groups": duplicates,
            "total_duplicate_files": sum(len(paths) for paths in duplicates.values()),
            "errors": errors[:10]  # Limit error reporting
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
            
            if result.get("errors"):
                print(f"\n⚠️  {len(result['errors'])} read errors")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    else:
        print(f"Unknown command: {command}")
        print("Run without arguments for usage help")
        sys.exit(1)


if __name__ == "__main__":
    main()
