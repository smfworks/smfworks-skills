# Markdown Converter — How-To Guide

**Prerequisites:** Setup complete (see SETUP.md). markdown package installed.

---

## Table of Contents

1. [How to Convert Markdown to HTML](#1-how-to-convert-markdown-to-html)
2. [How to Convert Markdown to Plain Text](#2-how-to-convert-markdown-to-plain-text)
3. [How to Extract a Table of Contents](#3-how-to-extract-a-table-of-contents)
4. [How to Count Words and Document Stats](#4-how-to-count-words-and-document-stats)
5. [How to Batch Convert Multiple Files](#5-how-to-batch-convert-multiple-files)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Convert Markdown to HTML

**What this does:** Converts a `.md` file into a complete HTML page with a clean, minimal CSS template — ready to open in a browser or embed in a website.

**When to use it:** Publishing documentation, converting a README to a web page, sharing a report or article as HTML rather than Markdown.

### Steps

**Step 1 — Navigate to the directory containing your Markdown file.**

This step is important: the skill only processes files in the current working directory.

```bash
cd ~/Documents
```

**Step 2 — Run the to-html command.**

```bash
python3 ~/smfworks-skills/skills/markdown-converter/main.py to-html blog-post.md
```

Output:
```
✅ Success: {'success': True, 'input': '/home/user/Documents/blog-post.md', 'output': '/home/user/Documents/blog-post.html', 'characters': 4823}
```

**Step 3 — Open the HTML file in your browser.**

```bash
# On macOS:
open blog-post.html

# On Linux:
xdg-open blog-post.html
```

**Step 4 — Optionally specify a different output location.**

```bash
python3 ~/smfworks-skills/skills/markdown-converter/main.py to-html blog-post.md ~/Desktop/blog-post.html
```

**Result:** A styled HTML file that renders your Markdown with working code blocks, tables, and lists — ready to share or deploy.

---

## 2. How to Convert Markdown to Plain Text

**What this does:** Strips all Markdown formatting (`**bold**`, `# Headers`, `` `code` ``, `[links](url)`) and saves a clean plain text version.

**When to use it:** Pasting content into a system that doesn't render Markdown (email body, CMS plain text fields, some forms).

### Steps

**Step 1 — Navigate to the directory containing your file.**

```bash
cd ~/Documents
```

**Step 2 — Convert to plain text.**

```bash
python3 ~/smfworks-skills/skills/markdown-converter/main.py to-text announcement.md
```

Output:
```
✅ Success: {'success': True, 'input': '/home/user/Documents/announcement.md', 'output': '/home/user/Documents/announcement.txt', 'characters': 1247}
```

**Step 3 — Verify the result.**

```bash
cat announcement.txt | head -20
```

The text should be free of `#`, `*`, `[`, and other Markdown syntax.

**Result:** A clean plain text file ready to paste into any system.

---

## 3. How to Extract a Table of Contents

**What this does:** Reads all `#` headers in the Markdown file and prints a nested, indented list — showing the document's structure at a glance.

**When to use it:** Reviewing a large document before editing. Checking if your document has a logical hierarchy. Generating a TOC to paste into the document itself.

### Steps

**Step 1 — Navigate to the directory containing your file.**

```bash
cd ~/Documents
```

**Step 2 — Extract the TOC.**

```bash
python3 ~/smfworks-skills/skills/markdown-converter/main.py toc architecture.md
```

Output:
```
Table of Contents:
- Overview
- Architecture
  - Components
  - Data Flow
  - Security
- Installation
  - Prerequisites
  - Configuration
  - First Run
- API Reference
  - Endpoints
  - Authentication
- Troubleshooting
- FAQ
```

**Step 3 — Use the TOC.**

You can copy this into the top of your Markdown file as a navigation reference, or share it as a quick summary of the document's structure.

**Result:** A clear outline of your document's structure in seconds.

---

## 4. How to Count Words and Document Stats

**What this does:** Analyzes a Markdown file and counts words, lines, headers, code blocks, links, and images.

**When to use it:** Checking if an article meets a word count requirement. Understanding the composition of technical documentation.

### Steps

**Step 1 — Navigate to the directory containing your file.**

```bash
cd ~/Documents
```

**Step 2 — Run stats.**

```bash
python3 ~/smfworks-skills/skills/markdown-converter/main.py stats technical-guide.md
```

Output:
```
Words: 4,218
Lines: 287
Headers: 18
Code blocks: 12
Links: 34
Images: 8
```

**Step 3 — Interpret the results.**

| Stat | Meaning |
|------|---------|
| Words | Total word count |
| Lines | Total line count (including blank lines) |
| Headers | Number of `#` headings (any level) |
| Code blocks | Fenced code blocks (` ``` ` pairs) |
| Links | `[text](url)` style links |
| Images | `![alt](url)` style images |

**Result:** You have a full profile of the document — words, structure, and richness of content.

---

## 5. How to Batch Convert Multiple Files

**What this does:** Converts every `.md` file in a directory to HTML (or text) using a shell loop.

**When to use it:** You have a folder of Markdown files and need all of them as HTML for a website or documentation system.

### Steps

**Step 1 — Navigate to the directory containing your Markdown files.**

```bash
cd ~/docs
```

**Step 2 — Convert all .md files to HTML.**

```bash
for f in *.md; do
  python3 ~/smfworks-skills/skills/markdown-converter/main.py to-html "$f"
done
```

Output for each file:
```
✅ Success: {'success': True, 'input': '/home/user/docs/intro.md', 'output': '/home/user/docs/intro.html', 'characters': 1204}
✅ Success: {'success': True, 'input': '/home/user/docs/guide.md', 'output': '/home/user/docs/guide.html', 'characters': 8472}
...
```

**Step 3 — Verify all HTML files were created.**

```bash
ls *.html
```

**Result:** Every Markdown file in the directory now has a corresponding HTML file.

---

## 6. Automating with Cron

Schedule automatic Markdown conversion — for example, converting your daily notes to HTML every evening.

### Open the cron editor

```bash
crontab -e
```

### Example: Convert today's notes to HTML every evening at 6 PM

```bash
0 18 * * * cd /home/yourname/Notes && python3 /home/yourname/smfworks-skills/skills/markdown-converter/main.py to-html today.md >> /home/yourname/logs/markdown-converter.log 2>&1
```

### Example: Convert all docs on Sunday at 9 AM

```bash
0 9 * * 0 cd /home/yourname/docs && for f in *.md; do python3 /home/yourname/smfworks-skills/skills/markdown-converter/main.py to-html "$f"; done >> /home/yourname/logs/markdown-converter.log 2>&1
```

### Cron Expression Reference

| Expression | Meaning |
|------------|---------|
| `0 18 * * *` | Every day at 6 PM |
| `0 9 * * 0` | Every Sunday at 9 AM |
| `0 22 * * 5` | Every Friday at 10 PM |

### Create the log directory

```bash
mkdir -p ~/logs
```

---

## 7. Combining with Other Skills

**Markdown Converter + Text Formatter:** Clean up a Markdown file's text content before converting:

```bash
# Get word count first
python3 ~/smfworks-skills/skills/markdown-converter/main.py stats ~/blog/article.md

# Convert to HTML for publishing
cd ~/blog && python3 ~/smfworks-skills/skills/markdown-converter/main.py to-html article.md ~/public/article.html
```

**Markdown Converter + File Organizer:** Batch convert then organize:

```bash
cd ~/docs
for f in *.md; do python3 ~/smfworks-skills/skills/markdown-converter/main.py to-html "$f"; done
python3 ~/smfworks-skills/skills/file-organizer/main.py organize-type ~/docs/
```

---

## 8. Troubleshooting Common Issues

### `Path outside allowed directory`

The skill restricts access to the current working directory.  
**Fix:** Run `cd ~/Documents` (or wherever your file is) before running the skill, then use relative filenames.

---

### `Input file not found: notes.md`

The file doesn't exist in the current directory.  
**Fix:** Run `ls` to check what's in the current directory. Use the exact filename including extension.

---

### `markdown not installed. Run: pip install markdown`

**Fix:** `pip install markdown`

---

### HTML output looks unstyled

This is normal if you open the HTML as a local file and your browser blocks local CSS.  
**Fix:** The CSS is inline in the `<style>` tag — it should render. If you're seeing raw HTML, right-click → Open With → choose your browser.

---

### Stats shows unexpected code block count

Code block counting looks for fenced ` ``` ` pairs. If you have unclosed or odd-numbered fences, the count may be off.  
**Fix:** This is expected behavior — ensure your code blocks are properly closed.

---

## 9. Tips & Best Practices

**Always `cd` to your file's directory first.** The skill only processes files within the current working directory. This is a safety restriction — get in the habit of `cd`ing first.

**Use `stats` before and after editing.** It's a quick way to track your word count progress on articles, documentation, or reports.

**Use `toc` to review document structure.** Before publishing, run `toc` to see if your heading hierarchy makes sense. Too many H2s without H3 structure, or inconsistent nesting, becomes obvious immediately.

**The HTML template is minimal by design.** The output is clean and readable but not a full design. For polished output, add your own `<link rel="stylesheet">` tag pointing to a CSS file after generating.

**For batch conversion in cron, always use absolute paths.** Cron doesn't set `$HOME` or other env vars reliably. Use `/home/yourname/` everywhere in cron entries.

**`to-text` is useful for input to other tools.** Plain text output from Markdown works great as input to `text-formatter count`, email body text, or pasting into CMS fields.
