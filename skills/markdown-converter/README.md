# Markdown Converter

> Convert Markdown documents to HTML, plain text, or extract structure

---

## What It Does

Markdown Converter transforms Markdown files into beautiful HTML documents or clean plain text. Extract a table of contents from long documents, analyze document statistics, or batch convert files for your website.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install markdown-converter
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Convert a Markdown file to HTML:

```bash
python main.py to-html document.md
```

---

## Commands

### `to-html`

**What it does:** Convert a Markdown file to a styled HTML document.

**Usage:**
```bash
python main.py to-html [input-file] [output-file]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input-file` | ✅ Yes | Markdown source file | `README.md` |
| `output-file` | ❌ No | HTML output path (auto-generated if omitted) | `README.html` |

**Example:**
```bash
python main.py to-html README.md
python main.py to-html README.md output.html
```

**Output:**
```
✅ Converted: README.md → README.html
   Characters: 4,521
   Headers: 12
   Links: 8
```

---

### `to-text`

**What it does:** Convert Markdown to plain text (strips formatting).

**Usage:**
```bash
python main.py to-text [input-file] [output-file]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input-file` | ✅ Yes | Markdown source file | `article.md` |
| `output-file` | ❌ No | Text output path | `article.txt` |

**Example:**
```bash
python main.py to-text article.md
python main.py to-text article.md article.txt
```

---

### `toc`

**What it does:** Extract a table of contents from a Markdown document.

**Usage:**
```bash
python main.py toc [input-file]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input-file` | ✅ Yes | Markdown source file | `documentation.md` |

**Example:**
```bash
python main.py toc documentation.md
```

**Output:**
```
Table of Contents:
- Introduction
  - Getting Started
  - Installation
- Features
  - Command Line
  - Configuration
- Troubleshooting
```

---

### `stats`

**What it does:** Count words, characters, headers, links, and more.

**Usage:**
```bash
python main.py stats [input-file]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input-file` | ✅ Yes | Markdown source file | `article.md` |

**Example:**
```bash
python main.py stats article.md
```

**Output:**
```
📊 Document Statistics:
   Words: 1,234
   Lines: 89
   Headers: 12
   Code blocks: 3
   Links: 8
   Images: 2
```

---

## Use Cases

- **Website publishing:** Convert Markdown blog posts to HTML
- **Documentation:** Transform Markdown docs into web-ready HTML
- **Email:** Convert Markdown to plain text for email bodies
- **Analysis:** Check document length and structure before publishing
- **Navigation:** Extract TOC to understand document structure

---

## Tips & Tricks

- Omit output path to auto-generate filename with `.html` extension
- Generated HTML is self-contained with inline styles
- Works without the markdown library (falls back to regex parsing)
- Great for static site generators

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "markdown not installed" | Run `pip install markdown` for full conversion |
| "File not found" | Check the path to your Markdown file |
| Output looks wrong | Ensure your Markdown file uses standard syntax |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- (Optional) `markdown` library for full HTML conversion (`pip install markdown`)

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/markdown-converter)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
