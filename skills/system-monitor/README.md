# System Monitor

A system health monitoring skill for OpenClaw. Monitor disk, memory, CPU, and find large files.

## Features

- **Disk Usage**: Monitor disk space usage
- **Memory Info**: Check RAM utilization
- **CPU Monitor**: View CPU usage and frequency
- **System Info**: Get platform information
- **Health Check**: Overall system health status
- **Large Files**: Find space-consuming files

## Installation

```bash
pip install psutil
```

## Usage

### Check Disk Usage
```bash
python main.py disk
python main.py disk /home
```

### Check Memory
```bash
python main.py memory
```

### Check CPU
```bash
python main.py cpu
```

### System Information
```bash
python main.py info
```

### System Health
```bash
python main.py health
```

Shows overall status with thresholds:
- **Good**: < 80% usage
- **Warning**: 80-90% usage
- **Critical**: > 90% usage

### Find Large Files
```bash
python main.py large-files
python main.py large-files ~/Downloads 20
```

## Input Validation Limits

| Parameter | Limit |
|-----------|-------|
| Rate limit | 30 calls per 60 seconds |
| Large file scan depth | 10 directory levels |
| Max files to check | 10,000 |
| Results limit | 100 files |
| Path validation | Home directory, /tmp, /var/tmp only |

## Security Considerations

- **Path Traversal Protection**: Blocks `..` sequences in paths
- **Directory Restrictions**: Only scans allowed directories
- **Rate Limiting**: Prevents excessive system calls
- **Path Disclosure Prevention**: Shows relative paths, not absolute
- **Safe Path Resolution**: Validates all paths before access

## Error Handling

Errors are categorized:
- **Rate Limit**: Too many requests
- **ImportError**: psutil not installed
- **PermissionError**: Insufficient system access
- **OSError**: System call failures

## Known Limitations

- Requires psutil for memory and CPU info
- Rate limited to 30 calls per minute
- Large file scan limited to 10,000 files
- CPU usage measurement requires 1-second delay
- Some metrics require root/admin access

## Examples

```bash
# Check system health
python main.py health

# Monitor disk space
python main.py disk /

# Find large files in Downloads
python main.py large-files ~/Downloads 10

# Get full system info
python main.py info
```
