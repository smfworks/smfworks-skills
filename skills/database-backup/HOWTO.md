# Database Backup — Quick Reference

## Install
```bash
smfw install database-backup
```

## Commands
```bash
python main.py backup              # Interactive backup wizard
python main.py list                # List all backups
python main.py stats               # Show backup statistics
python main.py restore [file]       # Restore from backup
python main.py cleanup [days]       # Remove old backups
```

## Common Examples
```bash
# Start interactive backup
python main.py backup

# List existing backups
python main.py list

# Show backup statistics
python main.py stats

# Restore a backup (SQLite)
python main.py restore ~/backups/myapp-20260320-143052.sqlite.sql.gz

# Clean up backups older than 30 days
python main.py cleanup 30
```

## Help
```bash
python main.py --help
```
