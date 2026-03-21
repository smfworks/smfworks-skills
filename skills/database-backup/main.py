#!/usr/bin/env python3
"""
Database Backup - SMF Works Pro Skill
Automated backups for SQLite, PostgreSQL, and MySQL databases.

Usage:
    smf run database-backup backup --db-type sqlite --source ~/app.db --dest ~/backups/
    smf run database-backup schedule --config backup-config.json
    smf run database-backup list
    smf run database-backup restore --backup-file ~/backups/app-20260320-120000.sql.gz
"""

import sys
import os
import json
import gzip
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Add shared auth to path
shared_path = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from smf_auth import require_subscription, show_subscription_error

# Skill configuration
SKILL_NAME = "database-backup"
MIN_TIER = "pro"
BACKUP_DIR = Path.home() / ".smf" / "backups"
CONFIG_DIR = Path.home() / ".smf" / "config"


def ensure_dirs():
    """Ensure backup and config directories exist."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def generate_backup_filename(db_name: str, db_type: str) -> str:
    """Generate timestamped backup filename."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{db_name}-{timestamp}.{db_type}.sql.gz"


def backup_sqlite(source: str, dest_dir: str) -> Dict:
    """Backup SQLite database."""
    try:
        source_path = Path(source).expanduser()
        dest_path = Path(dest_dir).expanduser()
        dest_path.mkdir(parents=True, exist_ok=True)
        
        if not source_path.exists():
            return {"success": False, "error": f"Database not found: {source}"}
        
        db_name = source_path.stem
        backup_file = dest_path / generate_backup_filename(db_name, "sqlite")
        
        # SQLite backup using .dump command
        result = subprocess.run(
            ["sqlite3", str(source_path), ".dump"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return {"success": False, "error": f"SQLite dump failed: {result.stderr}"}
        
        # Compress and save
        with gzip.open(backup_file, 'wt') as f:
            f.write(result.stdout)
        
        # Get file size
        size_mb = backup_file.stat().st_size / (1024 * 1024)
        
        return {
            "success": True,
            "backup_file": str(backup_file),
            "original_size_mb": round(source_path.stat().st_size / (1024 * 1024), 2),
            "backup_size_mb": round(size_mb, 2),
            "compression_ratio": round((1 - size_mb / (source_path.stat().st_size / (1024 * 1024))) * 100, 1)
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def backup_postgres(host: str, port: str, database: str, user: str, password: str, dest_dir: str) -> Dict:
    """Backup PostgreSQL database."""
    try:
        dest_path = Path(dest_dir).expanduser()
        dest_path.mkdir(parents=True, exist_ok=True)
        
        backup_file = dest_path / generate_backup_filename(database, "postgres")
        
        # Set PGPASSWORD environment variable
        env = os.environ.copy()
        env["PGPASSWORD"] = password
        
        # Run pg_dump
        with gzip.open(backup_file, 'wb') as f:
            result = subprocess.run(
                ["pg_dump", "-h", host, "-p", port, "-U", user, "-d", database, "-F", "plain"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
            
            if result.returncode != 0:
                return {"success": False, "error": f"pg_dump failed: {result.stderr.decode()}"}
            
            f.write(result.stdout)
        
        size_mb = backup_file.stat().st_size / (1024 * 1024)
        
        return {
            "success": True,
            "backup_file": str(backup_file),
            "database": database,
            "backup_size_mb": round(size_mb, 2)
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def backup_mysql(host: str, port: str, database: str, user: str, password: str, dest_dir: str) -> Dict:
    """Backup MySQL database."""
    try:
        dest_path = Path(dest_dir).expanduser()
        dest_path.mkdir(parents=True, exist_ok=True)
        
        backup_file = dest_path / generate_backup_filename(database, "mysql")
        
        # Run mysqldump
        with gzip.open(backup_file, 'wb') as f:
            result = subprocess.run(
                ["mysqldump", "-h", host, "-P", port, "-u", user, f"-p{password}", database],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            if result.returncode != 0:
                stderr = result.stderr.decode()
                # Filter out password warning
                stderr = '\n'.join([line for line in stderr.split('\n') if 'password' not in line.lower()])
                return {"success": False, "error": f"mysqldump failed: {stderr}"}
            
            f.write(result.stdout)
        
        size_mb = backup_file.stat().st_size / (1024 * 1024)
        
        return {
            "success": True,
            "backup_file": str(backup_file),
            "database": database,
            "backup_size_mb": round(size_mb, 2)
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_backups() -> List[Dict]:
    """List all backups."""
    ensure_dirs()
    
    backups = []
    if BACKUP_DIR.exists():
        for backup_file in BACKUP_DIR.rglob("*.sql.gz"):
            stat = backup_file.stat()
            backups.append({
                "file": str(backup_file),
                "name": backup_file.name,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    
    # Sort by date (newest first)
    backups.sort(key=lambda x: x["created"], reverse=True)
    return backups


def restore_backup(backup_file: str, target: str, db_type: str) -> Dict:
    """Restore database from backup."""
    try:
        backup_path = Path(backup_file).expanduser()
        target_path = Path(target).expanduser()
        
        if not backup_path.exists():
            return {"success": False, "error": f"Backup file not found: {backup_file}"}
        
        print(f"⚠️  This will overwrite: {target}")
        confirm = input("Are you sure? (yes/no): ")
        
        if confirm.lower() != "yes":
            return {"success": False, "error": "Restore cancelled"}
        
        if db_type == "sqlite":
            # Decompress and restore SQLite
            with gzip.open(backup_path, 'rt') as f:
                sql = f.read()
            
            # Write to temp file and execute
            temp_sql = Path("/tmp/restore.sql")
            temp_sql.write_text(sql)
            
            result = subprocess.run(
                ["sqlite3", str(target_path)],
                stdin=temp_sql.open(),
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return {"success": False, "error": f"Restore failed: {result.stderr}"}
            
            return {"success": True, "message": f"Restored to {target}"}
        
        else:
            return {"success": False, "error": f"Restore not yet implemented for {db_type}"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def cleanup_old_backups(keep_days: int = 30) -> Dict:
    """Remove backups older than keep_days."""
    ensure_dirs()
    
    cutoff = datetime.now() - timedelta(days=keep_days)
    removed = 0
    total_size = 0
    
    for backup_file in BACKUP_DIR.rglob("*.sql.gz"):
        mtime = datetime.fromtimestamp(backup_file.stat().st_mtime)
        if mtime < cutoff:
            size = backup_path.stat().st_size
            backup_file.unlink()
            removed += 1
            total_size += size
    
    return {
        "success": True,
        "removed": removed,
        "freed_mb": round(total_size / (1024 * 1024), 2)
    }


def interactive_backup():
    """Interactive backup configuration."""
    print("\n💾 Database Backup")
    print("=" * 40)
    
    print("\nSelect database type:")
    print("  1. SQLite")
    print("  2. PostgreSQL")
    print("  3. MySQL")
    
    choice = input("\nChoice (1-3): ").strip()
    
    if choice == "1":
        # SQLite
        source = input("SQLite database file path: ").strip()
        dest = input("Backup destination directory [~/smf/backups]: ").strip()
        if not dest:
            dest = str(BACKUP_DIR)
        
        return backup_sqlite(source, dest)
    
    elif choice == "2":
        # PostgreSQL
        print("\nEnter PostgreSQL connection details:")
        host = input("Host [localhost]: ").strip() or "localhost"
        port = input("Port [5432]: ").strip() or "5432"
        database = input("Database name: ").strip()
        user = input("Username: ").strip()
        password = input("Password: ").strip()
        dest = input("Backup destination [~/smf/backups]: ").strip() or str(BACKUP_DIR)
        
        return backup_postgres(host, port, database, user, password, dest)
    
    elif choice == "3":
        # MySQL
        print("\nEnter MySQL connection details:")
        host = input("Host [localhost]: ").strip() or "localhost"
        port = input("Port [3306]: ").strip() or "3306"
        database = input("Database name: ").strip()
        user = input("Username: ").strip()
        password = input("Password: ").strip()
        dest = input("Backup destination [~/smf/backups]: ").strip() or str(BACKUP_DIR)
        
        return backup_mysql(host, port, database, user, password, dest)
    
    else:
        return {"success": False, "error": "Invalid choice"}


def show_stats():
    """Show backup statistics."""
    backups = list_backups()
    
    if not backups:
        print("No backups found.")
        return
    
    total_size = sum(b["size_mb"] for b in backups)
    
    # Group by database
    by_db = {}
    for backup in backups:
        # Extract db name from filename
        parts = backup["name"].split("-")
        if len(parts) >= 2:
            db_name = parts[0]
            by_db[db_name] = by_db.get(db_name, 0) + 1
    
    print("\n📊 Backup Statistics")
    print("=" * 40)
    print(f"Total backups: {len(backups)}")
    print(f"Total size: {total_size:.2f} MB")
    print(f"Backup location: {BACKUP_DIR}")
    print("")
    print("Backups by database:")
    for db, count in sorted(by_db.items(), key=lambda x: x[1], reverse=True):
        print(f"  {db}: {count} backup(s)")


def main():
    """CLI entry point."""
    # Check for test mode
    if "--test-mode" in sys.argv:
        sys.argv.remove("--test-mode")
        print("🔧 TEST MODE: Subscription check skipped")
        subscription = {"valid": True, "tier": "test"}
    else:
        # Check subscription
        subscription = require_subscription(SKILL_NAME, MIN_TIER)
        
        if not subscription["valid"]:
            show_subscription_error(subscription)
            return 1
        
        print(f"💾 Database Backup")
        print(f"   Subscription: {subscription['tier']}")
        print("")
    
    # Parse command
    if len(sys.argv) < 2:
        print("Usage: smf run database-backup <command> [options]")
        print("")
        print("Commands:")
        print("  backup              - Interactive backup wizard")
        print("  list                - List all backups")
        print("  stats               - Show backup statistics")
        print("  restore <file>      - Restore from backup (SQLite only)")
        print("  cleanup [days]      - Remove old backups (default: 30 days)")
        print("")
        print("Examples:")
        print("  smf run database-backup backup")
        print("  smf run database-backup list")
        print("  smf run database-backup restore ~/backups/app-20260320-120000.sqlite.sql.gz")
        print("  smf run database-backup cleanup 7")
        return 0
    
    command = sys.argv[1]
    
    if command == "backup":
        if len(sys.argv) > 2:
            # Command line args mode
            # Parse --db-type, --source, --dest, etc.
            print("Command line backup mode not yet implemented.")
            print("Use interactive mode: smf run database-backup backup")
            return 1
        else:
            # Interactive mode
            result = interactive_backup()
            
            if result["success"]:
                print(f"\n✅ Backup complete!")
                print(f"   File: {result['backup_file']}")
                print(f"   Size: {result['backup_size_mb']} MB")
                if "compression_ratio" in result:
                    print(f"   Compression: {result['compression_ratio']}%")
            else:
                print(f"\n❌ Backup failed: {result['error']}")
                return 1
    
    elif command == "list":
        backups = list_backups()
        
        if not backups:
            print("No backups found.")
            return 0
        
        print(f"\n💾 {len(backups)} Backup(s)")
        print("-" * 80)
        print(f"{'Name':<50} {'Size':<10} {'Date':<20}")
        print("-" * 80)
        
        for backup in backups:
            name = backup["name"][:48]
            size = f"{backup['size_mb']:.1f} MB"
            date = backup["created"][:19]
            print(f"{name:<50} {size:<10} {date:<20}")
    
    elif command == "stats":
        show_stats()
    
    elif command == "restore":
        if len(sys.argv) < 3:
            print("Error: restore requires backup file")
            return 1
        
        backup_file = sys.argv[2]
        target = input("Target database file: ").strip()
        db_type = input("Database type (sqlite/postgres/mysql): ").strip()
        
        result = restore_backup(backup_file, target, db_type)
        
        if result["success"]:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ Restore failed: {result['error']}")
            return 1
    
    elif command == "cleanup":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        
        print(f"Removing backups older than {days} days...")
        result = cleanup_old_backups(days)
        
        if result["success"]:
            print(f"✅ Removed {result['removed']} backup(s)")
            print(f"   Freed {result['freed_mb']} MB")
    
    else:
        print(f"Unknown command: {command}")
        print("Run without arguments for usage help")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
