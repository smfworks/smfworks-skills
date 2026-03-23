# PDF Toolkit

> Merge, split, extract, rotate, compress, and analyze PDF files

---

## What It Does

PDF Toolkit handles all your PDF manipulation needs — combine multiple PDFs, split a large PDF into individual pages, extract specific page ranges, rotate pages, compress file sizes, and get detailed PDF information.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install pdf-toolkit
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Merge multiple PDFs into one:

```bash
python main.py merge output.pdf chapter1.pdf chapter2.pdf
```

---

## Commands

### `merge`

**What it does:** Combine multiple PDF files into one.

**Usage:**
```bash
python main.py merge [output.pdf] [input1.pdf] [input2.pdf] ...
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `output.pdf` | ✅ Yes | Output file name | `combined.pdf` |
| `input1.pdf` | ✅ Yes | First PDF to merge | `chapter1.pdf` |
| `input2.pdf` | ✅ Yes | Additional PDFs | `chapter2.pdf` |

**Example:**
```bash
python main.py merge combined.pdf chapter1.pdf chapter2.pdf chapter3.pdf
```

---

### `split`

**What it does:** Split a PDF into individual page files.

**Usage:**
```bash
python main.py split [input.pdf] [output-dir]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.pdf` | ✅ Yes | PDF to split | `big.pdf` |
| `output-dir` | ✅ Yes | Output directory | `./pages/` |

**Example:**
```bash
python main.py split report.pdf ./pages/
```

---

### `extract`

**What it does:** Extract a range of pages from a PDF.

**Usage:**
```bash
python main.py extract [input.pdf] [start-page] [end-page] [output.pdf]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.pdf` | ✅ Yes | Source PDF | `report.pdf` |
| `start-page` | ✅ Yes | First page (1-indexed) | `1` |
| `end-page` | ✅ Yes | Last page (1-indexed) | `5` |
| `output.pdf` | ✅ Yes | Output file | `extracted.pdf` |

**Example:**
```bash
python main.py extract report.pdf 1 5 extracted.pdf
python main.py extract report.pdf 10 15 chapter3.pdf
```

---

### `info`

**What it does:** Display PDF metadata and properties.

**Usage:**
```bash
python main.py info [input.pdf]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.pdf` | ✅ Yes | PDF file to inspect | `document.pdf` |

**Example:**
```bash
python main.py info document.pdf
```

**Output:**
```
📄 PDF Info: document.pdf
   Pages: 24
   Size: 2.4 MB
   Title: Q1 Sales Report
   Author: John Smith
   Subject: Sales
   Encrypted: No
```

---

### `compress`

**What it does:** Reduce PDF file size.

**Usage:**
```bash
python main.py compress [input.pdf] [output.pdf]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.pdf` | ✅ Yes | PDF to compress | `large.pdf` |
| `output.pdf` | ✅ Yes | Compressed output | `small.pdf` |

**Example:**
```bash
python main.py compress report.pdf compressed.pdf
```

---

### `rotate`

**What it does:** Rotate all pages in a PDF.

**Usage:**
```bash
python main.py rotate [input.pdf] [output.pdf] [degrees]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.pdf` | ✅ Yes | PDF to rotate | `scanned.pdf` |
| `output.pdf` | ✅ Yes | Rotated output | `fixed.pdf` |
| `degrees` | ✅ Yes | Rotation (90, 180, or 270) | `90` |

**Example:**
```bash
python main.py rotate scanned.pdf fixed.pdf 90
```

---

## Use Cases

- **Merging documents:** Combine scanned chapters into one book
- **Splitting handouts:** Extract specific pages from a large PDF
- **Extracting chapters:** Pull out specific sections for sharing
- **Fixing scans:** Rotate misaligned scanned pages
- **Compressing:** Reduce file size for email attachment

---

## Tips & Tricks

- Use page extraction for specific chapters instead of splitting everything
- Compress after merging to reduce overall file size
- Split creates files named: `input_page_1.pdf`, `input_page_2.pdf`, etc.
- Rotation is always applied to ALL pages

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "PyPDF2 not installed" | Run `pip install PyPDF2` |
| "Invalid PDF" | Ensure the file is a valid PDF |
| "Permission denied" | Check file/directory permissions |
| "Page out of range" | Verify page numbers exist in the PDF |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- PyPDF2 library (`pip install PyPDF2`)

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/pdf-toolkit)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
