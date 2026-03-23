# System Monitor — Quick Reference

## Install
```bash
smfw install system-monitor
```

## Commands
```bash
python main.py disk                       # Check disk usage
python main.py disk /home               # Check specific path
python main.py memory                     # Check memory usage
python main.py cpu                        # Check CPU usage
python main.py info                       # System information
python main.py health                     # Overall health check
python main.py large-files               # Find large files
python main.py large-files ~/Downloads 20  # Find 20 largest files
```

## Common Examples
```bash
# Check system health
python main.py health

# Check disk space
python main.py disk

# Check specific directory
python main.py disk /home

# Find large files
python main.py large-files ~/Downloads 20

# Get full system info
python main.py info
```

## Help
```bash
python main.py --help
```
