# File Organizer — Quick Reference

## Install
```bash
smfw install file-organizer
```

## Commands
```bash
python main.py organize ~/Downloads                              # Auto-organize folder
python main.py organize ~/Downloads --by type                  # By file type
python main.py organize ~/Downloads --by date                   # By date
python main.py organize ~/Downloads --dry-run                   # Preview changes
python main.py rules                                           # Show current rules
```

## Common Examples
```bash
# Auto-organize Downloads folder
python main.py organize ~/Downloads

# Preview what would happen
python main.py organize ~/Downloads --dry-run

# Organize by file type (Images, Documents, etc.)
python main.py organize ~/Downloads --by type

# Organize by modification date
python main.py organize ~/Downloads --by date
```

## Help
```bash
python main.py --help
python main.py organize --help
```
