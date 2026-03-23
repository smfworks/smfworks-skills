# Markdown Converter

> Convert Markdown files to HTML or plain text, extract a table of contents, and count words and document stats.

**Tier:** Free — no subscription required  
**Version:** 1.0  
**Category:** Productivity / Writing

---

## What It Does

Markdown Converter is an OpenClaw skill for transforming Markdown files. Convert `.md` files to styled HTML (with a clean browser-ready template including code block styling), strip Markdown formatting to plain text, extract a structured table of contents from headers, or get a word/character/link count summary.

The `to-html` command wraps output in a minimal CSS template — code blocks have a grey background, tables have borders, and blockquotes are styled. The output is ready to open in any browser.

**What it does NOT do:** It does not convert HTML back to Markdown, convert to PDF, process Markdown with embedded HTML, handle custom themes, or process files outside the current working directory.

---

## Prerequisites

- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed**
- [ ] **markdown Python package** — required for `to-html` and `to-text` (installed during setup)
- [ ] **No subscription required** — free tier skill
- [ ] **No API keys required**

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/markdown-converter
pip install markdown
python3 main.py
```

Expected output:
```
Usage: python main.py <command> [options]
Commands:
  to-html <input.md> [output.html]    - Convert to HTML
  to-text <input.md> [output.txt]     - Convert to plain text
  toc <input.md>                       - Extract table of contents
  stats <input.md>                     - Count stats
```

---

## Quick Start

Convert a Markdown file to HTML:

```bash
python3 main.py to-html ~/Documents/notes.md
```

Output:
```
✅ Success: {'success': True, 'input': '/home/user/Documents/notes.md', 'output': '/home/user/Documents/notes.html', 'characters': 4823}
```

Open `notes.html` in your browser to see the result.

---

## Command Reference

### `to-html`

Converts a Markdown file to a full HTML page. Supports tables, fenced code blocks, and table of contents generation. Output is wrapped in a minimal CSS template.

**Usage:**
```bash
python3 main.py to-html <input.md> [output.html]
```

**Arguments:**

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `input.md` | ✅ Yes | Markdown file to convert | — |
| `output.html` | ❌ No | Output HTML file. Defaults to same name as input with `.html` extension. | Same path, `.html` extension |

**Example — default output name:**
```bash
python3 main.py to-html ~/Documents/readme.md
```
Creates `~/Documents/readme.html`.

**Output:**
```
✅ Success: {'success': True, 'input': '/home/user/Documents/readme.md', 'output': '/home/user/Documents/readme.html', 'characters': 4823}
```

**Example — custom output name:**
```bash
python3 main.py to-html ~/docs/guide.md ~/public/guide.html
```

---

### `to-text`

Strips all Markdown formatting and saves plain text. Uses the `markdown` library to convert to HTML first, then strips HTML tags — producing cleaner results than regex-only stripping.

**Usage:**
```bash
python3 main.py to-text <input.md> [output.txt]
```

**Arguments:**

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `input.md` | ✅ Yes | Markdown file to convert | — |
| `output.txt` | ❌ No | Output text file. Defaults to same name with `.txt` extension. | Same path, `.txt` extension |

**Example:**
```bash
python3 main.py to-text ~/Documents/blog-post.md
```

Output:
```
✅ Success: {'success': True, 'input': '/home/user/Documents/blog-post.md', 'output': '/home/user/Documents/blog-post.txt', 'characters': 3201}
```

---

### `toc`

Extracts all headers (H1–H6) from a Markdown file and prints a nested table of contents with GitHub-style anchor links.

**Usage:**
```bash
python3 main.py toc <input.md>
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `input.md` | ✅ Yes | Markdown file to extract TOC from |

**Example:**
```bash
python3 main.py toc ~/Documents/technical-doc.md
```

**Output:**
```
Table of Contents:
- Introduction
- Getting Started
  - Prerequisites
  - Installation
- Usage
  - Basic Commands
  - Advanced Options
- Troubleshooting
- FAQ
```

---

### `stats`

Counts words, characters, lines, headers, code blocks, links, and images in a Markdown file.

**Usage:**
```bash
python3 main.py stats <input.md>
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `input.md` | ✅ Yes | Markdown file to analyze |

**Example:**
```bash
python3 main.py stats ~/Documents/api-docs.md
```

**Output:**
```
Words: 3,842
Lines: 218
Headers: 14
Code blocks: 8
Links: 22
Images: 6
```

---

## Use Cases

### 1. Convert documentation to share on a web page

```bash
python3 main.py to-html ~/Projects/myproject/README.md ~/public/index.html
```

---

### 2. Strip formatting for pasting into plain text fields

```bash
python3 main.py to-text ~/docs/announcement.md ~/docs/announcement.txt
```

---

### 3. Check how long your document is before publishing

```bash
python3 main.py stats ~/blog/article.md
```

---

### 4. Extract TOC to understand a large document's structure

```bash
python3 main.py toc ~/docs/architecture.md
```

---

### 5. Batch convert all Markdown files to HTML

```bash
for f in ~/docs/*.md; do python3 main.py to-html "$f"; done
```

---

## Configuration

No configuration file or environment variables needed.

**Security note:** The skill only processes files in the current working directory or its subdirectories. You cannot process files from a different directory with a path like `../../other-folder/file.md`.

---

## Troubleshooting

### `markdown not installed. Run: pip install markdown`
**Fix:** `pip install markdown`

### `Input file not found: notes.md`
**Fix:** Either use an absolute path (`~/Documents/notes.md`) or `cd` to the directory containing the file first.

### `Path outside allowed directory: /etc/passwd`
The skill blocks access to files outside the current working directory.  
**Fix:** Run the skill from the same directory as your Markdown file: `cd ~/Documents && python3 ~/smfworks-skills/skills/markdown-converter/main.py to-html notes.md`

### `Permission denied: /protected/file.md`
You don't have read access to the file.  
**Fix:** Check permissions: `ls -la /protected/file.md`

### HTML output has no styling
The skill's built-in CSS is minimal.  
**Fix:** The output is a valid HTML file. You can add your own `<link>` tag pointing to a CSS file after generation.

---

## FAQ

**Q: Does to-html support all Markdown features?**  
A: It uses the Python `markdown` library with `tables`, `fenced_code`, and `toc` extensions. Most common Markdown syntax is supported. Custom extensions or non-standard syntax may not render correctly.

**Q: Does to-text remove all formatting?**  
A: It strips HTML tags after converting Markdown to HTML. Most formatting is removed. Some edge cases (nested HTML, custom Markdown syntax) may leave residual markup.

**Q: What's in the HTML template?**  
A: A clean, minimal CSS reset with `max-width: 800px`, system font stack, code block styling (grey background, rounded corners), blockquote left border, and basic table borders.

**Q: Can I convert a file in a different directory?**  
A: Yes, but you need to either use an absolute path AND run from an allowed directory, or `cd` to the directory containing the file. The skill restricts access to the current working directory and its subdirectories.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| markdown | 3.0 or newer |
| OpenClaw | Any version |
| Subscription Tier | Free |
| External APIs | None |
| Internet Connection | Not required |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/markdown-converter)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
