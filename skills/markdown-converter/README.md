# Markdown Converter

A document conversion skill for OpenClaw. Convert Markdown to HTML and other formats.

## Features

- **Markdown → HTML**: Convert to styled HTML documents
- **Markdown → Text**: Extract plain text (removes formatting)
- **Table of Contents**: Extract document structure
- **Document Stats**: Count words, headers, links, etc.

## Installation

```bash
pip install markdown
```

## Usage

### Convert to HTML
```bash
python main.py to-html input.md
python main.py to-html input.md output.html
```

Creates a standalone HTML file with:
- Responsive styling
- Syntax highlighting support
- Table formatting
- Blockquote styling

### Convert to Plain Text
```bash
python main.py to-text input.md
python main.py to-text input.md output.txt
```

### Extract Table of Contents
```bash
python main.py toc document.md
```

Outputs a hierarchical list of headers.

### Document Statistics
```bash
python main.py stats document.md
```

Shows:
- Word count
- Character count
- Number of headers
- Code blocks
- Links and images

## Input Validation Limits

| Parameter | Limit |
|-----------|-------|
| File size | Limited by available memory |
| Path validation | Working directory only |
| File encoding | UTF-8 |

## Security Considerations

- **Path Traversal Protection**: Restricts access to working directory only
- **HTML Escaping**: Escapes HTML in document titles
- **Safe Output**: Generates self-contained HTML without external dependencies

## Error Handling

Errors are categorized:
- **FileNotFoundError**: Input file doesn't exist
- **PermissionError**: Insufficient file permissions
- **ImportError**: Markdown library not installed
- **ValueError**: Invalid file path

## Known Limitations

- Requires markdown library for full HTML conversion
- Text extraction is regex-based if markdown library unavailable
- Limited to UTF-8 encoded files
- Tables in plain text mode may lose formatting

## Examples

```bash
# Create HTML from markdown
python main.py to-html README.md README.html

# Extract plain text for processing
python main.py to-text report.md report.txt

# See document structure
python main.py toc documentation.md

# Get word count
python main.py stats article.md
```
