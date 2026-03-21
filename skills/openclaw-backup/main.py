#!/usr/bin/env python3
"""
OpenClaw Backup - SMF Works Pro Skill
Daily backup of your OpenClaw agent with 2-day rolling retention.

Requires: SMF Works Pro Subscription
"""

import os
import sys
import json
import argparse
import shutil
import tarfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Add shared module path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

try:
    from smf_auth import require_subscription
except ImportError:
    def require_subscription():
        token_path = os.path.expanduser("~/.smf/token")
        if not os.path.exists(token_path):
            print("❌ Pro skill requires SMF Works subscription")
            print("   Subscribe at: https://smf.works/subscribe")
            return False
        return True


DEFAULT_CONFIG = {
    "backup_dir": "~/.smf/backups",
    "retention_days": 2,
    "include_paths": [
        "~/.openclaw/workspace",
        "~/.openclaw/memory",
        "~/.openclaw/config"
    ],
    "exclude_patterns": [
        "*.log",
        "__pycache__",
        ".git",
        "node_modules",
        ".venv",
        "venv"
    ],
    "compress": True,
    "verify": True
}


def load_config():
    config_path = os.path.expanduser("~/.config/smf/skills/openclaw-backup/config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                config = DEFAULT_CONFIG.copy()
                config.update(json.load(f))
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Config error, using defaults: {e}", file=sys.stderr)
    return DEFAULT_CONFIG.copy()


def save_config(config):
    config_path = os.path.expanduser("~/.config/smf/skills/openclaw-backup/config.json")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    os.chmod(config_path, 0o600)


def get_backup_dir(config):
    """Get expanded backup directory path."""
    return os.path.expanduser(config.get('backup_dir', '~/.smf/backups'))


def calculate_dir_size(path):
    """Calculate directory size in bytes."""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total += os.path.getsize(fp)
            except OSError:
                pass
    return total


def verify_backup(backup_path: str, is_archive: bool = True) -> Dict:
    """Verify backup integrity."""
    print(f"\n🔍 Verifying backup...")
    
    if not os.path.exists(backup_path):
        return {"success": False, "error": "Backup file not found"}
    
    if is_archive:
        try:
            with tarfile.open(backup_path, 'r:gz') as tar:
                # Get list of members (this validates structure)
                members = tar.getmembers()
                # Verify each member is valid
                for member in members:
                    if not member.name or '..' in member.name or member.name.startswith('/'):
                        return {"success": False, "error": "Suspicious path in archive"}
                
                size = sum(m.size for m in members)
                
                return {
                    "success": True,
                    "files": len(members),
                    "size": size,
                    "message": "Backup verified successfully"
                }
        except tarfile.TarError as e:
            return {"success": False, "error": f"Archive corrupted: {e}"}
        except Exception as e:
            return {"success": False, "error": f"Verification failed: {e}"}
    else:
        # Uncompressed backup - verify files exist
        try:
            if not os.path.isdir(backup_path):
                return {"success": False, "error": "Backup directory not found"}
            
            # Check if at least one file exists
            file_count = sum(len(files) for _, _, files in os.walk(backup_path))
            
            if file_count == 0:
                return {"success": False, "error": "Backup directory is empty"}
            
            return {
                "success": True,
                "files": file_count,
                "message": "Backup directory verified"
            }
        except Exception as e:
            return {"success": False, "error": f"Verification failed: {e}"}


def tar_filter_factory(exclude_patterns):
    """Factory for creating tar filter function with exclude patterns."""
    def filter_func(tarinfo):
        # Check if any exclude pattern is in the path
        for pattern in exclude_patterns:
            if pattern in tarinfo.name:
                return None
        return tarinfo
    return filter_func


def create_backup(config, test_mode=False):
    """Create a new backup of OpenClaw with progress indication."""
    if not test_mode and not require_subscription():
        return None
    
    backup_dir = get_backup_dir(config)
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"openclaw_backup_{timestamp}"
    
    is_compressed = config.get('compress', True)
    if is_compressed:
        backup_path = os.path.join(backup_dir, f"{backup_name}.tar.gz")
    else:
        backup_path = os.path.join(backup_dir, backup_name)
    
    include_paths = [os.path.expanduser(p) for p in config.get('include_paths', [])]
    exclude_patterns = config.get('exclude_patterns', [])
    
    print(f"📦 Creating backup: {backup_name}")
    print(f"   Destination: {backup_path}")
    
    processed = 0
    skipped = 0
    errors = []
    
    try:
        if is_compressed:
            # Create tar.gz archive with progress
            with tarfile.open(backup_path, 'w:gz') as tar:
                for path in include_paths:
                    if os.path.exists(path):
                        arcname = os.path.basename(path)
                        try:
                            tar.add(
                                path, 
                                arcname=arcname, 
                                filter=tar_filter_factory(exclude_patterns)
                            )
                            processed += 1
                            print(f"   ✓ Added: {path}")
                        except Exception as e:
                            errors.append(f"Failed to add {path}: {e}")
                    else:
                        skipped += 1
                        print(f"   ⚠ Skipped (not found): {path}")
        else:
            # Create uncompressed copy
            os.makedirs(backup_path, exist_ok=True)
            for path in include_paths:
                if os.path.exists(path):
                    dest = os.path.join(backup_path, os.path.basename(path))
                    try:
                        if os.path.isdir(path):
                            shutil.copytree(path, dest, 
                                ignore=shutil.ignore_patterns(*exclude_patterns),
                                dirs_exist_ok=True)
                        else:
                            shutil.copy2(path, dest)
                        processed += 1
                        print(f"   ✓ Added: {path}")
                    except Exception as e:
                        errors.append(f"Failed to copy {path}: {e}")
                else:
                    skipped += 1
                    print(f"   ⚠ Skipped (not found): {path}")
        
        # Progress summary
        print(f"\n   Processed: {processed} items")
        if skipped:
            print(f"   Skipped: {skipped} items")
        if errors:
            print(f"   Errors: {len(errors)}")
            for err in errors[:3]:  # Show first 3 errors
                print(f"      • {err}")
        
        # Get backup size
        if os.path.exists(backup_path):
            if os.path.isfile(backup_path):
                size = os.path.getsize(backup_path)
            else:
                size = calculate_dir_size(backup_path)
            size_mb = size / (1024 * 1024)
            
            # Verify if enabled
            if config.get('verify', True) and is_compressed:
                verify_result = verify_backup(backup_path, is_archive=True)
                if not verify_result['success']:
                    print(f"\n⚠️  Verification warning: {verify_result.get('error')}")
            
            print(f"\n✅ Backup complete: {backup_name}")
            print(f"   Size: {size_mb:.2f} MB")
            print(f"   Location: {backup_path}")
            
            return {
                'name': backup_name,
                'path': backup_path,
                'size_mb': size_mb,
                'timestamp': datetime.now().isoformat(),
                'processed': processed,
                'skipped': skipped
            }
        else:
            print("\n❌ Backup file not created", file=sys.stderr)
            return None
    
    except Exception as e:
        print(f"\n❌ Backup failed: {e}", file=sys.stderr)
        return None


def list_backups(config):
    """List all available backups."""
    backup_dir = get_backup_dir(config)
    
    if not os.path.exists(backup_dir):
        print("No backups found.")
        return []
    
    backups = []
    for item in os.listdir(backup_dir):
        if item.startswith('openclaw_backup_'):
            path = os.path.join(backup_dir, item)
            try:
                stat = os.stat(path)
                
                if os.path.isfile(path):
                    size = stat.st_size
                else:
                    size = calculate_dir_size(path)
                
                backups.append({
                    'name': item,
                    'path': path,
                    'size_mb': size / (1024 * 1024),
                    'created': datetime.fromtimestamp(stat.st_mtime)
                })
            except OSError as e:
                print(f"⚠️  Could not read backup {item}: {e}")
                continue
    
    backups.sort(key=lambda x: x['created'], reverse=True)
    return backups


def cleanup_old_backups(config):
    """Remove backups older than retention period."""
    retention_days = config.get('retention_days', 2)
    cutoff = datetime.now() - timedelta(days=retention_days)
    
    backups = list_backups(config)
    removed = []
    errors = []
    
    for backup in backups:
        if backup['created'] < cutoff:
            try:
                if os.path.isfile(backup['path']):
                    os.remove(backup['path'])
                else:
                    shutil.rmtree(backup['path'])
                removed.append(backup['name'])
                print(f"   🗑️  Removed old backup: {backup['name']}")
            except Exception as e:
                errors.append(f"Failed to remove {backup['name']}: {e}")
    
    if errors:
        print(f"\n⚠️  {len(errors)} cleanup errors")
    
    return removed


def restore_backup(backup_path, restore_dir=None, test_mode=False):
    """Restore from a backup."""
    if not test_mode and not require_subscription():
        return False
    
    if not os.path.exists(backup_path):
        print(f"❌ Backup not found: {backup_path}")
        return False
    
    if restore_dir is None:
        restore_dir = os.path.expanduser("~/.openclaw_restored")
    
    print(f"📦 Restoring from: {os.path.basename(backup_path)}")
    print(f"   Destination: {restore_dir}")
    
    try:
        os.makedirs(restore_dir, exist_ok=True)
        
        if backup_path.endswith('.tar.gz'):
            # Verify archive before extracting
            verify_result = verify_backup(backup_path, is_archive=True)
            if not verify_result['success']:
                print(f"⚠️  Backup verification warning: {verify_result.get('error')}")
                response = input("Continue with restore? (yes/no): ").strip().lower()
                if response != 'yes':
                    print("❌ Restore cancelled")
                    return False
            
            with tarfile.open(backup_path, 'r:gz') as tar:
                tar.extractall(restore_dir)
        else:
            # Copy directory
            for item in os.listdir(backup_path):
                src = os.path.join(backup_path, item)
                dst = os.path.join(restore_dir, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
        
        print(f"\n✅ Restore complete!")
        print(f"   Files restored to: {restore_dir}")
        print(f"\nTo activate this restore:")
        print(f"   1. Stop OpenClaw if running")
        print(f"   2. Replace ~/.openclaw with restored files:")
        print(f"      rm -rf ~/.openclaw && mv {restore_dir} ~/.openclaw")
        print(f"   3. Restart OpenClaw")
        
        return True
    
    except tarfile.TarError as e:
        print(f"\n❌ Archive error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"\n❌ Restore failed: {e}", file=sys.stderr)
        return False


def configure():
    """Interactive configuration wizard."""
    print("💾 OpenClaw Backup - Configuration")
    print("=" * 50)
    
    config = load_config()
    
    print("\nStep 1: Backup Location")
    current = config.get('backup_dir', '~/.smf/backups')
    path = input(f"Backup directory [{current}]: ").strip()
    if path:
        config['backup_dir'] = path
    
    print("\nStep 2: Retention")
    current = config.get('retention_days', 2)
    days = input(f"Keep backups for how many days? [{current}]: ").strip()
    if days.isdigit():
        config['retention_days'] = int(days)
    
    print("\nStep 3: What to Backup")
    print("Default paths:")
    for p in config.get('include_paths', []):
        print(f"  - {p}")
    
    add = input("\nAdd additional paths? (comma-separated, or Enter to skip): ").strip()
    if add:
        config['include_paths'].extend([p.strip() for p in add.split(',')])
    
    print("\nStep 4: Verification")
    verify = input("Verify backups after creation? (y/n) [y]: ").strip().lower()
    config['verify'] = verify != 'n'
    
    print("\nStep 5: Schedule")
    print("Recommended: Run daily at 1:00 AM")
    print("Command: openclaw cron add --name 'openclaw-backup' --schedule '0 1 * * *' --command 'smf run openclaw-backup'")
    
    save_config(config)
    print(f"\n✅ Configuration saved!")
    print(f"\nRun 'smf run openclaw-backup' to create your first backup.")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw Backup - Daily backup with 2-day rolling retention",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smf run openclaw-backup              # Create backup
  smf run openclaw-backup --list      # List all backups
  smf run openclaw-backup --restore   # Restore from backup
  smf run openclaw-backup --configure # Configure settings
        """
    )
    
    parser.add_argument('--configure', '-c', action='store_true', help='Configure settings')
    parser.add_argument('--list', '-l', action='store_true', help='List backups')
    parser.add_argument('--restore', '-r', metavar='BACKUP', help='Restore from backup path')
    parser.add_argument('--cleanup', action='store_true', help='Remove old backups')
    parser.add_argument('--test-mode', '-t', action='store_true', help='Skip subscription check')
    
    args = parser.parse_args()
    
    if args.configure:
        configure()
        return
    
    config = load_config()
    
    if args.list:
        backups = list_backups(config)
        if backups:
            print(f"\n💾 Available Backups ({len(backups)} total):\n")
            for i, b in enumerate(backups, 1):
                print(f"{i}. {b['name']}")
                print(f"   Created: {b['created'].strftime('%Y-%m-%d %H:%M')}")
                print(f"   Size: {b['size_mb']:.2f} MB")
                print(f"   Path: {b['path']}")
                print()
        else:
            print("\nNo backups found.")
            print(f"Run 'smf run openclaw-backup' to create your first backup.")
        return
    
    if args.restore:
        restore_backup(args.restore, test_mode=args.test_mode)
        return
    
    if args.cleanup:
        print("🧹 Cleaning up old backups...")
        removed = cleanup_old_backups(config)
        print(f"\n✅ Removed {len(removed)} old backup(s)")
        return
    
    # Default: create backup
    result = create_backup(config, test_mode=args.test_mode)
    if result:
        # Cleanup old backups after successful backup
        print("\n🧹 Cleaning up old backups...")
        removed = cleanup_old_backups(config)
        if removed:
            print(f"\n✅ Removed {len(removed)} old backup(s)")
        print("\n✅ Backup complete!")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
