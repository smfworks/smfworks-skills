# PDF Toolkit

A comprehensive PDF manipulation skill for OpenClaw. Merge, split, extract, rotate, compress, and analyze PDF files.

## Features

- **Merge**: Combine multiple PDFs into one
- **Split**: Extract individual pages or page ranges
- **Extract**: Get a specific range of pages from a PDF
- **Rotate**: Rotate all pages by 90°, 180°, or 270°
- **Compress**: Basic PDF compression
- **Info**: Display PDF metadata and properties

## Installation

```bash
# Install PyPDF2 dependency
pip install PyPDF2
```

## Usage

### Merge PDFs
```bash
python main.py merge output.pdf input1.pdf input2.pdf [input3.pdf...]
```

### Split PDF into Pages
```bash
python main.py split input.pdf ./output_directory/
```
Creates individual PDF files for each page: `input_page_1.pdf`, `input_page_2.pdf`, etc.

### Extract Page Range
```bash
python main.py extract input.pdf 1 5 output.pdf
```
Extracts pages 1-5 (1-indexed) from input.pdf to output.pdf.

### Get PDF Information
```bash
python main.py info document.pdf
```
Displays: pages, size, author, title, subject, encryption status.

### Compress PDF
```bash
python main.py compress input.pdf output.pdf
```

### Rotate PDF
```bash
python main.py rotate input.pdf output.pdf 90
```
Valid rotations: 90, 180, 270 degrees.

## Input Validation Limits

| Parameter | Limit |
|-----------|-------|
| Maximum file size | 100 MB |
| Maximum pages per PDF | 10,000 |
| Maximum files to merge | 100 |
| Maximum pages to extract | 100 |
| Allowed extensions | `.pdf` only |

## Security Considerations

- **Path Traversal Protection**: Blocks `..` in paths to prevent directory escape
- **Extension Validation**: Only `.pdf` files allowed (case-insensitive)
- **Double Extension Detection**: Rejects files like `file.pdf.exe`
- **Size Limits**: Prevents processing of oversized files
- **SSRF Protection**: Validates all file paths before operations

## Error Handling

The tool provides categorized error messages:
- `PermissionError`: File access denied
- `OSError`: System-level errors
- `ValueError`: Invalid input parameters
- `ImportError`: Missing PyPDF2 dependency

## Known Limitations

- Compression uses basic PyPDF2 methods; results may vary
- Encrypted PDFs require manual decryption before processing
- Page extraction preserves content only (interactive elements may be lost)
- Output files are automatically renamed to end with `.pdf`

## Page Indexing

- **CLI input**: 1-indexed (user-friendly)
- **Internal API**: 0-indexed (Python standard)
- The CLI automatically converts 1-indexed user input to 0-indexed for internal processing
