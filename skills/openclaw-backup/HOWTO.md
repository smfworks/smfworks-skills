# OpenClaw Backup — Quick Reference

## Install
```bash
smfw install openclaw-backup
```

## Commands
```bash
python main.py backup                       # Full OpenClaw backup
python main.py backup --dest ~/Backups     # Custom destination
python main.py list                        # List backups
python main.py restore [backup-id]          # Restore from backup
python main.py config                      # Configure backup settings
```

## Common Examples
```bash
# Backup all OpenClaw data
python main.py backup

# List available backups
python main.py list

# Restore from backup
python main.py restore OPENCLAW-20260320-143052

# Configure backup destination
python main.py config
```

## Help
```bash
python main.py --help
```
