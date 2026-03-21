# Text Formatter

A text manipulation skill for OpenClaw. Convert case, clean whitespace, and analyze text statistics.

## Features

- **Case Conversion**: Convert between upper, lower, title, sentence, camelCase, snake_case, and kebab-case
- **Whitespace Cleaning**: Clean up extra whitespace, with optional aggressive mode
- **Word Count**: Analyze text statistics (words, characters, lines, sentences, reading time)

## Usage

### Case Conversion
```bash
# Convert to uppercase
python main.py case upper "hello world"
# Output: HELLO WORLD

# Convert to camelCase
python main.py case camel "hello world"
# Output: helloWorld

# Convert to snake_case
python main.py case snake "hello world"
# Output: hello_world
```

**Supported case types:**
- `upper` - UPPERCASE
- `lower` - lowercase
- `title` - Title Case
- `sentence` - Sentence case
- `camel` - camelCase
- `snake` - snake_case
- `kebab` - kebab-case

### Clean Whitespace
```bash
# Basic cleaning (preserves paragraph structure)
python main.py clean < input.txt

# Aggressive cleaning (collapses all whitespace)
python main.py clean --aggressive < messy.txt
```

### Word Count Statistics
```bash
python main.py count < document.txt
```

Output:
```
Words: 523
Characters: 3214
Characters (no spaces): 2851
Lines: 45
Sentences: 32
Reading time: 2 min 36 sec
```

## Input Methods

1. **Command argument**: `python main.py case upper "hello world"`
2. **File input**: `python main.py case upper < file.txt`
3. **File path**: `python main.py case upper ./input.txt`

## Input Validation Limits

| Parameter | Limit |
|-----------|-------|
| Maximum input size | 10 MB |
| Maximum output size | 50 MB |
| Maximum words to process | 10 million |
| File encoding | UTF-8 only |

## Security Considerations

- **Path Traversal Protection**: Blocks `..` in file paths
- **File Size Limits**: Prevents processing of oversized files
- **Encoding Validation**: Only accepts valid UTF-8 text files
- **Empty File Check**: Rejects empty input files
- **Memory Protection**: Hard limits on word count and file size

## Error Handling

The tool provides specific error categories:
- **OSError**: File system errors
- **UnicodeDecodeError**: Invalid file encoding
- **ValueError**: Invalid input parameters
- **Resource Limits**: Exceeded word count or file size

## Known Limitations

- Binary files are rejected (UTF-8 text only)
- Very long single-line files may impact performance
- Reading time estimation assumes 200 WPM average
- Sentence detection is basic (looks for `.!?` characters)

## Examples

```bash
# Convert file to uppercase and save
python main.py case upper < input.txt > output.txt

# Clean whitespace in a file
python main.py clean < messy.txt > clean.txt

# Get statistics
python main.py count < report.txt
```
