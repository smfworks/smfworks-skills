# File Organizer

A file management skill for OpenClaw. Organize files by date, type, or find duplicates.

## Features

- **Organize by Date**: Sort files into YYYY/MM directory structure
- **Organize by Type**: Group files into category folders (Images, Documents, etc.)
- **Find Duplicates**: Identify duplicate files by MD5 hash

## Usage

### Organize by Date
```bash
python main.py organize-date ~/Downloads
python main.py organize-date ~/Downloads ~/Organized
```

Creates directory structure like:
```
2024/
  03/
    file1.pdf
    file2.jpg
  04/
    file3.docx
```

### Organize by Type
```bash
python main.py organize-type ~/Documents
```

Organizes into categories:
- Images (.jpg, .png, .gif, etc.)
- Documents (.pdf, .doc, .txt, etc.)
- Spreadsheets (.xls, .csv, etc.)
- Videos (.mp4, .avi, etc.)
- Audio (.mp3, .wav, etc.)
- Code (.py, .js, .html, etc.)
- Archives (.zip, .rar, etc.)
- Other

### Find Duplicates
```bash
python main.py find-duplicates ~/Pictures
```

## Input Validation Limits

| Parameter | Limit |
|-----------|-------|
| Maximum file size | 100 MB per file |
| Maximum duplicate counter | 1000 iterations |
| Maximum scan depth | 10 directory levels |
| Maximum files in batch | 10,000 files checked |

## Security Considerations

- **System Directory Protection**: Cannot operate on system directories (/bin, /etc, /usr, etc.)
- **Path Traversal Protection**: Blocks `..` sequences in paths
- **Destination Validation**: Ensures destination paths don't escape allowed directories
- **Symbolic Link Handling**: Skips symlinks to prevent cycles
- **Safe Path Verification**: Validates target paths remain within allowed boundaries

## Error Handling

Errors are categorized:
- **PermissionError**: Insufficient permissions
- **OSError**: File system errors
- **ValueError**: Invalid paths or parameters
- **Security Error**: Path traversal or system directory access attempt

## Known Limitations

- Maximum file size of 100MB (larger files are skipped)
- Duplicate detection limited to MD5 hash (not content-aware)
- Symbolic links are skipped
- Directory scan depth limited to 10 levels
- Duplicate handling limited to 1000 iterations

## Examples

```bash
# Organize Downloads folder by date
python main.py organize-date ~/Downloads

# Organize with custom destination
python main.py organize-type ~/Downloads ~/Organized/ByType

# Find duplicate photos
python main.py find-duplicates ~/Pictures
```
