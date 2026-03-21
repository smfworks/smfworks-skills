#!/usr/bin/env python3
"""
System Monitor Skill for OpenClaw
Monitor disk space, memory, CPU, and system health.
"""

import os
import platform
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import time

# Rate limiting configuration
RATE_LIMIT_WINDOW = 60  # seconds
MAX_CALLS_PER_WINDOW = 30

# Track API calls for rate limiting
_call_history: List[float] = []


def check_rate_limit() -> tuple[bool, Optional[str]]:
    """
    Check if we're within rate limits.
    Returns (allowed, error_message).
    """
    global _call_history
    
    now = time.time()
    # Remove calls outside the window
    _call_history = [t for t in _call_history if now - t < RATE_LIMIT_WINDOW]
    
    if len(_call_history) >= MAX_CALLS_PER_WINDOW:
        return False, f"Rate limit exceeded. Max {MAX_CALLS_PER_WINDOW} calls per {RATE_LIMIT_WINDOW} seconds."
    
    _call_history.append(now)
    return True, None


def get_safe_path(path: str) -> tuple[bool, Path, Optional[str]]:
    """
    Validate and sanitize a path to prevent path disclosure vulnerabilities.
    """
    try:
        p = Path(path).resolve()
    except (OSError, ValueError) as e:
        return False, Path(), f"Invalid path: {path}"
    
    # Check for path traversal
    normalized = os.path.normpath(path)
    if ".." in normalized.split(os.sep):
        return False, p, "Path traversal detected"
    
    # Only allow paths that exist
    if not p.exists():
        return False, p, f"Path does not exist: {path}"
    
    return True, p, None


def get_disk_usage(path: str = "/") -> Dict:
    """
    Get disk usage for a path.
    
    Args:
        path: Path to check (default: root)
    
    Returns:
        Dict with disk usage info
    """
    # Rate limiting
    allowed, error = check_rate_limit()
    if not allowed:
        return {"error": error}
    
    # Validate path
    is_valid, safe_path, error = get_safe_path(path)
    if not is_valid:
        return {"error": error}
    
    try:
        usage = shutil.disk_usage(str(safe_path))
        
        total_gb = usage.total / (1024**3)
        used_gb = usage.used / (1024**3)
        free_gb = usage.free / (1024**3)
        percent_used = (usage.used / usage.total) * 100
        
        status = "good"
        if percent_used > 90:
            status = "critical"
        elif percent_used > 80:
            status = "warning"
        
        return {
            "path": path,  # Return original path, not resolved path
            "total_gb": round(total_gb, 2),
            "used_gb": round(used_gb, 2),
            "free_gb": round(free_gb, 2),
            "percent_used": round(percent_used, 1),
            "status": status
        }
    except Exception as e:
        return {"error": str(e)}


def get_memory_info() -> Dict:
    """
    Get memory usage information.
    
    Returns:
        Dict with memory info
    """
    # Rate limiting
    allowed, error = check_rate_limit()
    if not allowed:
        return {"error": error}
    
    try:
        import psutil
        
        memory = psutil.virtual_memory()
        
        total_gb = memory.total / (1024**3)
        available_gb = memory.available / (1024**3)
        used_gb = memory.used / (1024**3)
        
        return {
            "total_gb": round(total_gb, 2),
            "available_gb": round(available_gb, 2),
            "used_gb": round(used_gb, 2),
            "percent_used": memory.percent,
            "status": "critical" if memory.percent > 90 else "warning" if memory.percent > 80 else "good"
        }
    except ImportError:
        return {"error": "psutil not installed. Run: pip install psutil"}
    except Exception as e:
        return {"error": str(e)}


def get_cpu_info() -> Dict:
    """
    Get CPU information.
    
    Returns:
        Dict with CPU info
    """
    # Rate limiting
    allowed, error = check_rate_limit()
    if not allowed:
        return {"error": error}
    
    try:
        import psutil
        
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        return {
            "percent_used": cpu_percent,
            "core_count": cpu_count,
            "frequency_mhz": round(cpu_freq.current, 0) if cpu_freq else None,
            "status": "critical" if cpu_percent > 90 else "warning" if cpu_percent > 70 else "good"
        }
    except ImportError:
        return {"error": "psutil not installed. Run: pip install psutil"}
    except Exception as e:
        return {"error": str(e)}


def get_system_info() -> Dict:
    """
    Get general system information.
    
    Returns:
        Dict with system info
    """
    # Rate limiting
    allowed, error = check_rate_limit()
    if not allowed:
        return {"error": error}
    
    return {
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": platform.node(),
        "boot_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def get_large_files(directory: str = "~", n: int = 10, min_size_mb: int = 100) -> List[Dict]:
    """
    Find large files in a directory.
    
    Args:
        directory: Directory to search
        n: Number of files to return
        min_size_mb: Minimum file size in MB
    
    Returns:
        List of large files
    """
    # Rate limiting
    allowed, error = check_rate_limit()
    if not allowed:
        return [{"error": error}]
    
    # Validate and sanitize directory
    try:
        dir_path = Path(directory).expanduser().resolve()
    except (OSError, ValueError) as e:
        return [{"error": f"Invalid directory: {directory}"}]
    
    # Check for path traversal
    normalized = os.path.normpath(directory)
    if ".." in normalized.split(os.sep):
        return [{"error": "Path traversal detected"}]
    
    # Limit search to home directory and common data directories
    home = Path.home().resolve()
    allowed_roots = [
        str(home),
        "/tmp",
        "/var/tmp",
        "/home"
    ]
    
    dir_str = str(dir_path)
    allowed = any(dir_str.startswith(root) for root in allowed_roots)
    if not allowed:
        return [{"error": "Directory outside allowed search paths"}]
    
    if not dir_path.exists():
        return [{"error": f"Directory does not exist: {directory}"}]
    
    large_files = []
    files_checked = 0
    max_files_to_check = 10000  # Prevent excessive scanning
    
    try:
        for file_path in dir_path.rglob("*"):
            files_checked += 1
            if files_checked > max_files_to_check:
                break
            
            if file_path.is_file():
                try:
                    size_mb = file_path.stat().st_size / (1024**2)
                    if size_mb >= min_size_mb:
                        # Return relative path to prevent full path disclosure
                        try:
                            rel_path = file_path.relative_to(home)
                            display_path = f"~/{rel_path}"
                        except ValueError:
                            # Outside home, use basename only
                            display_path = file_path.name
                        
                        large_files.append({
                            "path": display_path,
                            "size_mb": round(size_mb, 2)
                        })
                except (OSError, IOError, PermissionError):
                    continue
    except Exception as e:
        return [{"error": str(e)}]
    
    # Sort by size and return top N
    large_files.sort(key=lambda x: x["size_mb"], reverse=True)
    return large_files[:min(n, 100)]  # Limit to max 100


def check_system_health() -> Dict:
    """
    Check overall system health.
    
    Returns:
        Dict with health status
    """
    health = {
        "timestamp": datetime.now().isoformat(),
        "status": "healthy",
        "checks": {}
    }
    
    # Check disk
    disk = get_disk_usage("/")
    if "error" not in disk:
        health["checks"]["disk"] = {
            "status": disk["status"],
            "percent_used": disk["percent_used"]
        }
        if disk["status"] == "critical":
            health["status"] = "critical"
        elif disk["status"] == "warning" and health["status"] == "healthy":
            health["status"] = "warning"
    
    # Check memory
    memory = get_memory_info()
    if "error" not in memory:
        health["checks"]["memory"] = {
            "status": memory["status"],
            "percent_used": memory["percent_used"]
        }
        if memory["status"] == "critical":
            health["status"] = "critical"
        elif memory["status"] == "warning" and health["status"] == "healthy":
            health["status"] = "warning"
    
    # Check CPU
    cpu = get_cpu_info()
    if "error" not in cpu:
        health["checks"]["cpu"] = {
            "status": cpu["status"],
            "percent_used": cpu["percent_used"]
        }
        if cpu["status"] == "critical":
            health["status"] = "critical"
        elif cpu["status"] == "warning" and health["status"] == "healthy":
            health["status"] = "warning"
    
    return health


def main():
    """CLI interface for system monitor."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [options]")
        print("")
        print("Commands:")
        print("  disk [path]                          - Check disk usage")
        print("  memory                               - Check memory usage")
        print("  cpu                                  - Check CPU usage")
        print("  info                                 - System information")
        print("  health                               - Overall system health")
        print("  large-files [directory] [n]          - Find large files")
        print("")
        print("Examples:")
        print("  python main.py disk")
        print("  python main.py memory")
        print("  python main.py health")
        print("  python main.py large-files ~/Downloads 20")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "disk":
        path = sys.argv[2] if len(sys.argv) > 2 else "/"
        result = get_disk_usage(path)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
        
        status_icon = "✅" if result["status"] == "good" else "⚠️" if result["status"] == "warning" else "🔴"
        print(f"{status_icon} Disk Usage ({result['path']})")
        print(f"   Total: {result['total_gb']} GB")
        print(f"   Used: {result['used_gb']} GB ({result['percent_used']}%)")
        print(f"   Free: {result['free_gb']} GB")
    
    elif command == "memory":
        result = get_memory_info()
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
        
        status_icon = "✅" if result["status"] == "good" else "⚠️" if result["status"] == "warning" else "🔴"
        print(f"{status_icon} Memory Usage")
        print(f"   Total: {result['total_gb']} GB")
        print(f"   Used: {result['used_gb']} GB ({result['percent_used']}%)")
        print(f"   Available: {result['available_gb']} GB")
    
    elif command == "cpu":
        result = get_cpu_info()
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
        
        status_icon = "✅" if result["status"] == "good" else "⚠️" if result["status"] == "warning" else "🔴"
        print(f"{status_icon} CPU Usage")
        print(f"   Usage: {result['percent_used']}%")
        print(f"   Cores: {result['core_count']}")
        if result["frequency_mhz"]:
            print(f"   Frequency: {result['frequency_mhz']} MHz")
    
    elif command == "info":
        result = get_system_info()
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
        
        print("📊 System Information")
        print(f"   Platform: {result['platform']}")
        print(f"   Hostname: {result['hostname']}")
        print(f"   Machine: {result['machine']}")
        print(f"   Processor: {result['processor']}")
        print(f"   Boot Time: {result['boot_time']}")
    
    elif command == "health":
        result = check_system_health()
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
        
        status_icon = "✅" if result["status"] == "healthy" else "⚠️" if result["status"] == "warning" else "🔴"
        print(f"{status_icon} System Health: {result['status'].upper()}")
        print(f"   Timestamp: {result['timestamp']}")
        print("")
        print("Checks:")
        for check, data in result["checks"].items():
            icon = "✅" if data["status"] == "good" else "⚠️" if data["status"] == "warning" else "🔴"
            print(f"   {icon} {check.capitalize()}: {data['percent_used']}%")
    
    elif command == "large-files":
        directory = sys.argv[2] if len(sys.argv) > 2 else "~"
        try:
            n = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        except ValueError:
            print("Error: n must be an integer")
            sys.exit(1)
        
        results = get_large_files(directory, n)
        
        if results and "error" in results[0]:
            print(f"❌ Error: {results[0]['error']}")
            sys.exit(1)
        
        print(f"📁 Top {len(results)} Large Files in {directory}")
        for i, file_info in enumerate(results, 1):
            print(f"   {i}. {file_info['path']} ({file_info['size_mb']} MB)")
    
    else:
        print(f"Unknown command: {command}")
        print("Run without arguments for usage help")
        sys.exit(1)


if __name__ == "__main__":
    main()
