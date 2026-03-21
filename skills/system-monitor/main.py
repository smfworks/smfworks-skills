#!/usr/bin/env python3
"""
System Monitor Skill for OpenClaw
Monitor disk space, memory, CPU, and system health.
"""

import os
import platform
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def get_disk_usage(path: str = "/") -> Dict:
    """
    Get disk usage for a path.
    
    Args:
        path: Path to check (default: root)
    
    Returns:
        Dict with disk usage info
    """
    try:
        usage = shutil.disk_usage(path)
        
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
            "path": path,
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
    try:
        dir_path = Path(directory).expanduser()
        large_files = []
        
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                size_mb = file_path.stat().st_size / (1024**2)
                if size_mb >= min_size_mb:
                    large_files.append({
                        "path": str(file_path),
                        "size_mb": round(size_mb, 2)
                    })
        
        # Sort by size and return top N
        large_files.sort(key=lambda x: x["size_mb"], reverse=True)
        return large_files[:n]
    except Exception as e:
        return [{"error": str(e)}]


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
        
        print("📊 System Information")
        print(f"   Platform: {result['platform']}")
        print(f"   Hostname: {result['hostname']}")
        print(f"   Machine: {result['machine']}")
        print(f"   Processor: {result['processor']}")
        print(f"   Boot Time: {result['boot_time']}")
    
    elif command == "health":
        result = check_system_health()
        
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
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        
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
