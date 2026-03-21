#!/usr/bin/env python3
"""
Claw System Backup - SMF Works Pro Skill
Weekly full Linux system backup with compression and verification.

Requires: SMF Works Pro Subscription + root/sudo access
"""

import os
import sys
import json
import argparse
import subprocess
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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
    "backup_dir": "~/.smf/system-backups",
    "retention_weeks": 2,
    "backup_type": "incremental",  # full, incremental, or home-only
    "exclude_paths": [
        "/proc",
        "/sys",
        "/dev",
        "/run",
        "/tmp",
        "/mnt",
        "/media",
        "/lost+found",
        "/var/cache",
        "/var/tmp"
    ],
    "include_home": True,
    "include_etc": True,
    "compression": "gzip",  # gzip, bzip2, xz, or none
    "verify": True,
    "notify_on_complete": True
}


def load_config():
    config_path = os.path.expanduser("~/.config/smf/skills/claw-system-backup/config.json")
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
    config_path = os.path.expanduser("~/.config/smf/skills/claw-system-backup/config.json")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    os.chmod(config_path, 0o600)


def check_root():
    """Check if running as root."""
    return os.geteuid() == 0


def check_disk_space(path, required_gb=1):
    """Check if sufficient disk space is available."""
    try:
        stat = os.statvfs(path)
        available_gb = (stat.f_frsize * stat.f_bavail) / (1024 ** 3)
        return available_gb >= required_gb, available_gb
    except Exception as e:
        print(f"⚠️  Could not check disk space: {e}", file=sys.stderr)
        return True, 0  # Assume OK if we can't check


def get_disk_usage(path):
    """Get disk usage for a path."""
    try:
        result = subprocess.run(
            ['du', '-sb', path],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            size = int(result.stdout.split()[0])
            return size
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, ValueError):
        pass
    return 0


def format_size(size_bytes):
    """Format bytes to human readable."""
    if size_bytes == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def create_backup(config, test_mode=False):
    """Create system backup."""
    if not test_mode and not require_subscription():
        return None
    
    # Check root status
    if not check_root():
        print("⚠️  Warning: Not running as root. Some files may not be accessible.")
        print("   For full system backup, run with: sudo smf run claw-system-backup")
        print()
        # Don't proceed without root for system backup
        response = input("Continue anyway? Files may be inaccessible (yes/no): ").strip().lower()
        if response != 'yes':
            print("❌ Backup cancelled - root access required")
            return None
    
    backup_dir = os.path.expanduser(config.get('backup_dir', '~/.smf/system-backups'))
    
    # Check disk space before starting
    has_space, available = check_disk_space(backup_dir, required_gb=5)
    if not has_space:
        print(f"❌ Insufficient disk space: {format_size(available * 1024 ** 3)} available")
        print("   At least 5 GB recommended for system backup")
        return None
    
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    try:
        result = subprocess.run(['hostname'], capture_output=True, text=True, timeout=5)
        hostname = result.stdout.strip() or 'system'
    except Exception:
        hostname = 'system'
    
    backup_type = config.get('backup_type', 'incremental')
    compression = config.get('compression', 'gzip')
    
    # Determine archive name
    ext_map = {'gzip': '.tar.gz', 'bzip2': '.tar.bz2', 'xz': '.tar.xz', 'none': '.tar'}
    ext = ext_map.get(compression, '.tar.gz')
    backup_name = f"{hostname}_{backup_type}_{timestamp}{ext}"
    backup_path = os.path.join(backup_dir, backup_name)
    
    print(f"💾 Claw System Backup")
    print(f"   Type: {backup_type}")
    print(f"   Destination: {backup_path}")
    print(f"   Available space: {format_size(available * 1024 ** 3) if available else 'unknown'}")
    print()
    
    # Build tar command
    tar_cmd = ['tar']
    
    # Compression
    if compression == 'gzip':
        tar_cmd.append('-czf')
    elif compression == 'bzip2':
        tar_cmd.append('-cjf')
    elif compression == 'xz':
        tar_cmd.append('-cJf')
    else:
        tar_cmd.append('-cf')
    
    tar_cmd.append(backup_path)
    
    # Exclude patterns
    for exclude in config.get('exclude_paths', []):
        tar_cmd.extend(['--exclude', exclude])
    
    # Additional excludes
    tar_cmd.extend(['--exclude', backup_dir])  # Don't backup the backups
    tar_cmd.extend(['--exclude', '*/.cache/*'])
    tar_cmd.extend(['--exclude', '*/__pycache__/*'])
    
    # What to backup based on type
    if backup_type == 'home-only':
        backup_sources = ['/home']
    elif backup_type == 'incremental':
        # Key system files + home
        backup_sources = []
        if config.get('include_etc', True):
            backup_sources.append('/etc')
        if config.get('include_home', True):
            backup_sources.append('/home')
        # Add other important directories
        for path in ['/root', '/boot', '/var/lib/dpkg', '/var/lib/apt']:
            if os.path.exists(path):
                backup_sources.append(path)
    else:  # full
        backup_sources = ['/']
        # Excludes handled above
    
    # Only include existing sources
    backup_sources = [s for s in backup_sources if os.path.exists(s)]
    
    if not backup_sources:
        print("❌ No valid backup sources found!")
        return None
    
    print(f"   Sources: {', '.join(backup_sources)}")
    print(f"   Compression: {compression}")
    print()
    
    try:
        # Run tar with progress
        tar_cmd.extend(backup_sources)
        
        print("📦 Creating backup (this may take several minutes)...")
        print("   (Progress shown as files are processed)")
        
        # Use verbose mode to show progress
        result = subprocess.run(
            tar_cmd,
            capture_output=False,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        if result.returncode != 0:
            if result.stderr:
                print(f"❌ Backup failed: {result.stderr}", file=sys.stderr)
            else:
                print("❌ Backup failed with unknown error", file=sys.stderr)
            return None
        
        # Get backup size
        if os.path.exists(backup_path):
            size = os.path.getsize(backup_path)
            
            print(f"\n✅ Backup complete!")
            print(f"   File: {backup_name}")
            print(f"   Size: {format_size(size)}")
            print(f"   Location: {backup_path}")
            
            # Verify backup if enabled
            if config.get('verify', True):
                print("\n🔍 Verifying backup integrity...")
                verify_result = verify_backup(backup_path, compression)
                if verify_result['success']:
                    print(f"   ✓ Verified: {verify_result.get('files', 'unknown')} files/directories")
                else:
                    print(f"   ⚠️  Verification warning: {verify_result.get('error')}")
            
            # Create info file
            info_path = backup_path + '.info'
            try:
                with open(info_path, 'w') as f:
                    f.write(f"Backup: {backup_name}\n")
                    f.write(f"Type: {backup_type}\n")
                    f.write(f"Created: {datetime.now().isoformat()}\n")
                    f.write(f"Size: {format_size(size)}\n")
                    f.write(f"Sources: {', '.join(backup_sources)}\n")
                    if not check_root():
                        f.write(f"Note: Backup created without root access\n")
            except IOError as e:
                print(f"⚠️  Could not create info file: {e}")
            
            return {
                'name': backup_name,
                'path': backup_path,
                'size': size,
                'type': backup_type,
                'timestamp': datetime.now().isoformat()
            }
    
    except subprocess.TimeoutExpired:
        print("\n❌ Backup timed out (exceeded 1 hour)", file=sys.stderr)
        return None
    except Exception as e:
        print(f"\n❌ Backup failed: {e}", file=sys.stderr)
        return None


def verify_backup(backup_path, compression):
    """Verify backup integrity."""
    try:
        # Determine test flag based on compression
        if compression == 'gzip':
            test_cmd = ['tar', '-tzf', backup_path]
        elif compression == 'bzip2':
            test_cmd = ['tar', '-tjf', backup_path]
        elif compression == 'xz':
            test_cmd = ['tar', '-tJf', backup_path]
        else:
            test_cmd = ['tar', '-tf', backup_path]
        
        result = subprocess.run(
            test_cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            file_count = len([l for l in result.stdout.split('\n') if l.strip()])
            return {
                "success": True,
                "files": file_count,
                "message": "Backup verified"
            }
        else:
            return {"success": False, "error": result.stderr or "Unknown verification error"}
    
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Verification timed out"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_backups(config):
    """List all system backups."""
    backup_dir = os.path.expanduser(config.get('backup_dir', '~/.smf/system-backups'))
    
    if not os.path.exists(backup_dir):
        print("No backups found.")
        return []
    
    backups = []
    for item in os.listdir(backup_dir):
        if item.endswith(('.tar', '.tar.gz', '.tar.bz2', '.tar.xz')):
            path = os.path.join(backup_dir, item)
            try:
                stat = os.stat(path)
                
                backups.append({
                    'name': item,
                    'path': path,
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_mtime)
                })
            except OSError as e:
                print(f"⚠️  Could not read {item}: {e}")
    
    backups.sort(key=lambda x: x['created'], reverse=True)
    return backups


def cleanup_old_backups(config):
    """Remove backups older than retention period."""
    retention_weeks = config.get('retention_weeks', 2)
    cutoff = datetime.now() - timedelta(weeks=retention_weeks)
    
    backups = list_backups(config)
    removed = []
    
    for backup in backups:
        if backup['created'] < cutoff:
            try:
                os.remove(backup['path'])
                info_path = backup['path'] + '.info'
                if os.path.exists(info_path):
                    os.remove(info_path)
                removed.append(backup['name'])
                print(f"   🗑️  Removed old backup: {backup['name']}")
            except Exception as e:
                print(f"   ⚠️  Failed to remove {backup['name']}: {e}", file=sys.stderr)
    
    return removed


def restore_backup(backup_path, target_dir=None, test_mode=False):
    """Restore from system backup."""
    if not test_mode and not require_subscription():
        return False
    
    if not os.path.exists(backup_path):
        print(f"❌ Backup not found: {backup_path}")
        return False
    
    if target_dir is None:
        target_dir = '/'
    
    print(f"⚠️  RESTORE OPERATION")
    print(f"   Source: {os.path.basename(backup_path)}")
    print(f"   Target: {target_dir}")
    print()
    print("⚠️  WARNING: This will overwrite files in the target directory!")
    print("⚠️  For system restore, boot from live USB and run from there.")
    print()
    
    confirm = input("Type 'RESTORE' to proceed: ")
    if confirm != 'RESTORE':
        print("❌ Restore cancelled.")
        return False
    
    try:
        # Determine compression and use appropriate extract flag
        if backup_path.endswith('.gz'):
            tar_cmd = ['tar', '-xzf', backup_path, '-C', target_dir]
        elif backup_path.endswith('.bz2'):
            tar_cmd = ['tar', '-xjf', backup_path, '-C', target_dir]
        elif backup_path.endswith('.xz'):
            tar_cmd = ['tar', '-xJf', backup_path, '-C', target_dir]
        else:
            tar_cmd = ['tar', '-xf', backup_path, '-C', target_dir]
        
        print("📦 Extracting backup...")
        result = subprocess.run(tar_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"\n✅ Restore complete!")
            print(f"   Files restored to: {target_dir}")
            return True
        else:
            print(f"\n❌ Restore failed: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"\n❌ Restore error: {e}")
        return False


def configure():
    """Interactive configuration wizard."""
    print("💾 Claw System Backup - Configuration")
    print("=" * 50)
    print()
    
    config = load_config()
    
    if not check_root():
        print("⚠️  Note: Configuration can be done without root,")
        print("   but backups must be run with sudo/root.")
        print()
    
    print("Step 1: Backup Location")
    current = config.get('backup_dir', '~/.smf/system-backups')
    path = input(f"Backup directory [{current}]: ").strip()
    if path:
        config['backup_dir'] = path
    
    # Check disk space for chosen directory
    expanded_path = os.path.expanduser(config['backup_dir'])
    has_space, available = check_disk_space(expanded_path, required_gb=1)
    print(f"   Available space: {format_size(available * 1024 ** 3)}")
    if not has_space:
        print("⚠️  Warning: Low disk space available")
    
    print("\nStep 2: Backup Type")
    print("  full        - Complete system backup (requires root)")
    print("  incremental - Key system files + home (recommended)")
    print("  home-only   - Just /home directory")
    current = config.get('backup_type', 'incremental')
    btype = input(f"Backup type [{current}]: ").strip()
    if btype in ['full', 'incremental', 'home-only']:
        config['backup_type'] = btype
    
    print("\nStep 3: Retention")
    current = config.get('retention_weeks', 2)
    weeks = input(f"Keep backups for how many weeks? [{current}]: ").strip()
    if weeks.isdigit():
        config['retention_weeks'] = int(weeks)
    
    print("\nStep 4: Compression")
    print("  gzip  - Fast, good compression (recommended)")
    print("  bzip2 - Slower, better compression")
    print("  xz    - Slowest, best compression")
    print("  none  - No compression")
    current = config.get('compression', 'gzip')
    comp = input(f"Compression [{current}]: ").strip()
    if comp in ['gzip', 'bzip2', 'xz', 'none']:
        config['compression'] = comp
    
    print("\nStep 5: Schedule")
    print("Recommended: Run weekly on Sundays at 2:00 AM")
    print("Command: openclaw cron add --name 'claw-system-backup' --schedule '0 2 * * 0' --command 'sudo smf run claw-system-backup'")
    
    save_config(config)
    print(f"\n✅ Configuration saved!")
    print(f"\nRun 'sudo smf run claw-system-backup' to create your first backup.")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Claw System Backup - Weekly full Linux system backup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo smf run claw-system-backup        # Create backup (requires root)
  smf run claw-system-backup --list      # List all backups
  smf run claw-system-backup --verify    # Verify backup integrity
  smf run claw-system-backup --configure # Configure settings

Note: Full system backups require root/sudo access.
        """
    )
    
    parser.add_argument('--configure', '-c', action='store_true', help='Configure settings')
    parser.add_argument('--list', '-l', action='store_true', help='List backups')
    parser.add_argument('--verify', '-v', metavar='BACKUP', help='Verify backup integrity')
    parser.add_argument('--restore', '-r', metavar='BACKUP', help='Restore from backup')
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
            print(f"\n💾 System Backups ({len(backups)} total):\n")
            total_size = 0
            for i, b in enumerate(backups, 1):
                print(f"{i}. {b['name']}")
                print(f"   Created: {b['created'].strftime('%Y-%m-%d %H:%M')}")
                print(f"   Size: {format_size(b['size'])}")
                print(f"   Path: {b['path']}")
                print()
                total_size += b['size']
            print(f"Total size: {format_size(total_size)}")
        else:
            print("\nNo backups found.")
            print(f"Run 'sudo smf run claw-system-backup' to create your first backup.")
        return
    
    if args.verify:
        compression = config.get('compression', 'gzip')
        result = verify_backup(args.verify, compression)
        if result['success']:
            print(f"✅ Verification passed: {result.get('files', 'N/A')} items")
        else:
            print(f"❌ Verification failed: {result.get('error')}")
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
    if not check_root():
        print("⚠️  This skill requires root access for system backup.")
        print("   Run with: sudo smf run claw-system-backup")
        print()
        proceed = input("Continue anyway? (files may be inaccessible) [y/N]: ").strip().lower()
        if proceed != 'y':
            sys.exit(1)
    
    result = create_backup(config, test_mode=args.test_mode)
    if result:
        print("\n🧹 Cleaning up old backups...")
        cleanup_old_backups(config)
        print("\n✅ Backup complete!")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
