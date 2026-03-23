# Markdown Converter — Quick Reference

## Install
```bash
smfw install markdown-converter
```

## Commands
```bash
python main.py to-html input.md                    # Convert to HTML
python main.py to-html input.md output.html       # With output path
python main.py to-text input.md                    # Convert to plain text
python main.py toc input.md                        # Extract table of contents
python main.py stats input.md                      # Count words, headers, etc.
```

## Common Examples
```bash
# Convert Markdown to HTML
python main.py to-html README.md

# Convert with custom output path
python main.py to-html README.md README.html

# Extract plain text (no HTML)
python main.py to-text article.md

# Get table of contents
python main.py toc documentation.md

# Count document statistics
python main.py stats article.md
```

## Help
```bash
python main.py --help
```
