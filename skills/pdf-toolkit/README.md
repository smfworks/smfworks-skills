# PDF Toolkit

> Merge, split, extract pages, compress, and rotate PDF files — all from the command line, no paid software required.

**Tier:** Free — no subscription required  
**Version:** 1.0  
**Category:** Productivity / Document Management

---

## What It Does

PDF Toolkit is an OpenClaw skill that gives you complete control over PDF files without needing Adobe Acrobat or any subscription software. You can merge multiple PDFs into one, split a PDF into individual pages, extract a specific range of pages, check a file's metadata and page count, attempt basic compression, and rotate all pages.

The skill is built on PyPDF2 and works entirely on your local machine — your PDF files never leave your computer and no internet connection is required.

**What it does NOT do:** It does not perform OCR (convert scanned images to searchable text), edit text inside PDFs, add or remove passwords, annotate or sign documents, or convert PDFs to or from other formats like Word or images.

---

## Prerequisites

Before installing, confirm:

- [ ] **Python 3.8 or newer** — run `python3 --version` to check
- [ ] **OpenClaw installed** — run `openclaw --version` to check
- [ ] **PyPDF2 Python package** — installed during setup
- [ ] **No subscription required** — this is a free tier skill
- [ ] **No API keys required** — works entirely offline

---

## Installation

**Step 1 — Clone the skills repository (if you haven't already):**

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

**Step 2 — Navigate to the skill directory:**

```bash
cd ~/smfworks-skills/skills/pdf-toolkit
```

**Step 3 — Install the required Python package:**

```bash
pip install PyPDF2
```

Expected output:
```
Collecting PyPDF2
  Downloading PyPDF2-3.0.1-py3-none-any.whl (232 kB)
Installing collected packages: PyPDF2
Successfully installed PyPDF2-3.0.1
```

**Step 4 — Verify the skill is ready:**

```bash
python3 main.py
```

You should see:
```
Usage: python main.py <command> [options]

Commands:
  merge <output.pdf> <input1.pdf> <input2.pdf> ...   - Merge PDFs
  split <input.pdf> <output_dir>                    - Split all pages
  extract <input.pdf> <start> <end> <output.pdf>  - Extract page range
  info <input.pdf>                                   - Show PDF info
  compress <input.pdf> <output.pdf>                - Compress PDF
  rotate <input.pdf> <output.pdf> <degrees>        - Rotate PDF

Examples:
  python main.py merge combined.pdf doc1.pdf doc2.pdf
  python main.py split document.pdf ./pages/
  python main.py extract report.pdf 1 5 summary.pdf
  python main.py info contract.pdf
```

---

## Quick Start

Check a PDF's info in seconds:

```bash
cd ~/smfworks-skills/skills/pdf-toolkit
python3 main.py info ~/Downloads/contract.pdf
```

Expected output:
```
📄 PDF Information:
   Title: Q1 Service Agreement
   Pages: 12
   Author: Legal Department
   Subject: Service Contract 2024
   Size: 284,672 bytes
   Encrypted: False
```

---

## Command Reference

### `merge`

Combines two or more PDF files into a single PDF. Files are merged in the order you list them. Up to 100 files can be merged at once. Each input file must be under 100 MB.

**Usage:**
```bash
python3 main.py merge <output.pdf> <input1.pdf> <input2.pdf> [more files...]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `output.pdf` | ✅ Yes | Name/path of the merged output file | `combined.pdf` |
| `input1.pdf` | ✅ Yes | First PDF to merge | `chapter1.pdf` |
| `input2.pdf` | ✅ Yes | Second PDF to merge | `chapter2.pdf` |
| additional files | ❌ No | More PDFs (up to 100 total) | `chapter3.pdf` |

**Example:**
```bash
python3 main.py merge ~/Documents/annual-report.pdf ~/Documents/q1.pdf ~/Documents/q2.pdf ~/Documents/q3.pdf ~/Documents/q4.pdf
```

**Output:**
```
✅ Merged 4 PDFs into /home/user/Documents/annual-report.pdf
   Output size: 1,847,296 bytes
```

---

### `split`

Splits every page of a PDF into a separate file. A 12-page PDF becomes 12 individual one-page PDFs. Output files are named `<original_stem>_page_1.pdf`, `_page_2.pdf`, etc.

**Usage:**
```bash
python3 main.py split <input.pdf> <output_dir>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.pdf` | ✅ Yes | PDF to split | `presentation.pdf` |
| `output_dir` | ✅ Yes | Directory to receive the individual page files | `./pages/` |

**Example:**
```bash
python3 main.py split ~/Downloads/presentation.pdf ~/Downloads/presentation-pages/
```

**Output:**
```
✅ Split 8 pages into 8 files
   Output directory: /home/user/Downloads/presentation-pages/
```

The output directory will contain:
```
presentation_page_1.pdf
presentation_page_2.pdf
presentation_page_3.pdf
...
presentation_page_8.pdf
```

---

### `extract`

Extracts a contiguous range of pages from a PDF into a new file. Page numbers are 1-indexed (the first page is page 1). Up to 100 pages can be extracted at once.

**Usage:**
```bash
python3 main.py extract <input.pdf> <start_page> <end_page> <output.pdf>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.pdf` | ✅ Yes | Source PDF | `full-report.pdf` |
| `start_page` | ✅ Yes | First page to extract (1 = first page) | `3` |
| `end_page` | ✅ Yes | Last page to extract (inclusive) | `7` |
| `output.pdf` | ✅ Yes | Output file for extracted pages | `summary.pdf` |

**Example:**
```bash
python3 main.py extract ~/Documents/full-report.pdf 5 10 ~/Documents/section-two.pdf
```

**Output:**
```
✅ Extracted 6 pages to /home/user/Documents/section-two.pdf
```

---

### `info`

Displays metadata and basic information about a PDF: title, author, subject, page count, file size, and whether it's encrypted.

**Usage:**
```bash
python3 main.py info <input.pdf>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.pdf` | ✅ Yes | PDF to inspect | `contract.pdf` |

**Example:**
```bash
python3 main.py info ~/Documents/contract.pdf
```

**Output:**
```
📄 PDF Information:
   Title: Service Agreement 2024
   Pages: 12
   Author: Jane Smith
   Subject: Annual Service Contract
   Size: 284,672 bytes
   Encrypted: False
```

---

### `compress`

Rewrites a PDF using PyPDF2's writer, which can reduce file size by stripping redundant internal structures. Note: for heavily-optimized PDFs, the output may be the same size or slightly larger — this is a basic text/structure compression, not image downsampling.

**Usage:**
```bash
python3 main.py compress <input.pdf> <output.pdf>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.pdf` | ✅ Yes | PDF to compress | `large-report.pdf` |
| `output.pdf` | ✅ Yes | Output file for compressed PDF | `report-small.pdf` |

**Example:**
```bash
python3 main.py compress ~/Documents/large-report.pdf ~/Documents/report-compressed.pdf
```

**Output:**
```
✅ Compressed PDF: 18.4% reduction
   Original: 3,145,728 bytes
   New: 2,566,914 bytes
```

---

### `rotate`

Rotates all pages in a PDF by 90, 180, or 270 degrees clockwise. Useful for correcting scanned documents that were scanned sideways.

**Usage:**
```bash
python3 main.py rotate <input.pdf> <output.pdf> <degrees>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.pdf` | ✅ Yes | PDF to rotate | `scan.pdf` |
| `output.pdf` | ✅ Yes | Output file for rotated PDF | `scan-fixed.pdf` |
| `degrees` | ✅ Yes | Rotation: must be `90`, `180`, or `270` | `90` |

**Example:**
```bash
python3 main.py rotate ~/Downloads/scan.pdf ~/Downloads/scan-rotated.pdf 90
```

**Output:**
```
✅ Rotated 5 pages by 90°
   Output: /home/user/Downloads/scan-rotated.pdf
```

---

## Use Cases

### 1. Combine monthly reports into one annual document

```bash
python3 main.py merge ~/Reports/annual-2024.pdf ~/Reports/jan.pdf ~/Reports/feb.pdf ~/Reports/mar.pdf ~/Reports/apr.pdf ~/Reports/may.pdf ~/Reports/jun.pdf ~/Reports/jul.pdf ~/Reports/aug.pdf ~/Reports/sep.pdf ~/Reports/oct.pdf ~/Reports/nov.pdf ~/Reports/dec.pdf
```

Result: One consolidated PDF with all twelve monthly reports in order.

---

### 2. Extract just the executive summary from a report

Your 80-page report has the executive summary on pages 1–4:

```bash
python3 main.py extract ~/Reports/annual-report.pdf 1 4 ~/Reports/exec-summary.pdf
```

Result: A 4-page PDF ready to email to stakeholders who don't need the full report.

---

### 3. Check if a downloaded PDF is corrupt

If a PDF fails to open, `info` will tell you quickly:

```bash
python3 main.py info ~/Downloads/suspicious-download.pdf
```

If you see file size and page count, the file is a valid PDF. An error message indicates corruption.

---

### 4. Fix a sideways-scanned document

Scanned on a printer that captured everything rotated 90 degrees:

```bash
python3 main.py rotate ~/Documents/scan.pdf ~/Documents/scan-fixed.pdf 270
```

Result: All pages are now oriented correctly.

---

### 5. Archive split pages for individual review

Split a long contract so each clause can be reviewed separately:

```bash
python3 main.py split ~/Documents/contract.pdf ~/Documents/contract-pages/
```

Result: Each page is its own PDF file, easy to share, annotate individually, or store selectively.

---

## Configuration

PDF Toolkit requires no configuration file or environment variables. All behavior is controlled by the command and arguments you pass.

**Built-in limits (not configurable):**

| Setting | Value | Reason |
|---------|-------|--------|
| Max input file size | 100 MB | Prevents long processing times |
| Max files to merge | 100 | Prevents excessive memory use |
| Max pages to extract | 100 at once | Keeps operations predictable |
| Max pages in a PDF | 10,000 | Safety cap on scan/traversal |
| Valid rotation values | 90, 180, 270 | Only valid PDF rotations |

---

## Troubleshooting

### `PyPDF2 not installed. Run: pip install PyPDF2`

**What happened:** The required Python package is missing.  
**Fix:** Run `pip install PyPDF2` and try again.

---

### `File not found: /path/to/file.pdf`

**What happened:** The path you provided doesn't exist.  
**Fix:** Check the exact path with `ls ~/Downloads` or use tab-completion when typing the path.

---

### `Not a PDF file: /path/to/document.doc`

**What happened:** You passed a non-PDF file. The skill only accepts files with a `.pdf` extension.  
**Fix:** Ensure your input files are actually PDFs. For other formats, convert them to PDF first.

---

### `File too large: 157286400 bytes (max: 104857600)`

**What happened:** Your input PDF exceeds the 100 MB size limit.  
**Fix:** Try splitting the PDF elsewhere (e.g., using an online tool) to reduce its size before processing with this skill.

---

### `Need at least 2 PDFs to merge`

**What happened:** You ran `merge` with only one input file.  
**Fix:** Provide at least two PDF files after the output filename: `python3 main.py merge output.pdf file1.pdf file2.pdf`

---

### `Invalid page range. PDF has 10 pages (1-10).`

**What happened:** You specified a start or end page outside the document's actual range.  
**Fix:** First run `info` to find out how many pages the PDF has, then use valid page numbers.

---

### `Rotation must be one of: [90, 180, 270]`

**What happened:** You used an unsupported rotation value.  
**Fix:** Only 90, 180, and 270 are valid. Use `270` instead of `-90` for counterclockwise rotation.

---

### `Permission denied`

**What happened:** The skill cannot read the input file or write to the output location.  
**Fix:** Check that you have read access to the input file (`ls -la ~/file.pdf`) and write access to the output directory.

---

### `File is empty: /path/to/file.pdf`

**What happened:** The PDF file exists but has zero bytes — likely a failed download.  
**Fix:** Re-download or re-export the PDF.

---

## FAQ

**Q: Does this skill require an internet connection?**  
A: No. All operations are performed locally on your machine. Your PDFs are never uploaded anywhere.

---

**Q: Will it modify my original PDF?**  
A: No. Every command requires you to specify a separate output file. Your input PDF is never modified.

---

**Q: What's the difference between split and extract?**  
A: `split` breaks a PDF into *all* its individual pages (one file per page). `extract` pulls a specific range of pages (pages 5–10, for example) into a single new PDF.

---

**Q: The compress command didn't reduce my file size much — is that normal?**  
A: Yes. The `compress` command uses basic PyPDF2 rewriting. If your PDF is already optimized, or if most of its size comes from embedded images, the reduction will be minimal. For aggressive image-based compression, consider dedicated tools like Ghostscript (`gs`) or an online compressor.

---

**Q: Can I merge PDFs that are password-protected?**  
A: No. The skill cannot open encrypted PDFs. You'll need to remove the password first using another tool.

---

**Q: Why does `rotate` rotate ALL pages? I only want to rotate one.**  
A: The current implementation rotates all pages in the PDF. To rotate a single page: (1) split the PDF, (2) rotate just that page, (3) merge everything back together.

---

**Q: Does it preserve hyperlinks and form fields when merging?**  
A: PyPDF2 attempts to preserve content, but complex interactive elements (forms, hyperlinks) may not survive a merge/split operation perfectly. Test with a copy before depending on it for important documents.

---

**Q: Can I use this in a script or pipeline?**  
A: Yes. The skill exits with code 0 on success and code 1 on failure, making it suitable for shell scripts and automation. See HOWTO.md for cron examples.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| PyPDF2 | 3.0.0 or newer |
| OpenClaw | Any version |
| Operating System | Linux, macOS |
| Subscription Tier | Free |
| External APIs | None |
| Internet Connection | Not required |

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/pdf-toolkit)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord Community](https://discord.gg/smfworks)
- 📧 [Support Email](mailto:support@smfworks.com)
