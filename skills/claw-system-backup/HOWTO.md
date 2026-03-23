# Claw System Backup — Quick Reference

## Install
```bash
smfw install claw-system-backup
```

## Commands
```bash
python main.py backup                   # Full system backup
python main.py backup --dest ~/Backups  # Custom destination
python main.py list                     # List existing backups
python main.py restore [backup-id]       # Restore from backup
python main.py status                   # Current backup status
python main.py schedule "0 2 * * *"     # Set cron schedule
```

## Common Examples
```bash
# Backup everything now
python main.py backup

# List available backups
python main.py list

# Restore from a backup
python main.py restore BACKUP-20260320-120000

# Check what would be backed up
python main.py status
```

## Help
```bash
python main.py --help
python main.py backup --help
```
