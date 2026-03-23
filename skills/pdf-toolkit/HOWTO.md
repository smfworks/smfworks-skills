# PDF Toolkit — How-To Guide

**Prerequisites:** Setup complete (see SETUP.md). PyPDF2 installed.

---

## Table of Contents

1. [How to Merge Multiple PDFs into One](#1-how-to-merge-multiple-pdfs-into-one)
2. [How to Split a PDF into Individual Pages](#2-how-to-split-a-pdf-into-individual-pages)
3. [How to Extract a Range of Pages](#3-how-to-extract-a-range-of-pages)
4. [How to Check a PDF's Info and Page Count](#4-how-to-check-a-pdfs-info-and-page-count)
5. [How to Compress a Large PDF](#5-how-to-compress-a-large-pdf)
6. [How to Rotate a Sideways-Scanned Document](#6-how-to-rotate-a-sideways-scanned-document)
7. [Automating with Cron](#7-automating-with-cron)
8. [Combining with Other Skills](#8-combining-with-other-skills)
9. [Troubleshooting Common Issues](#9-troubleshooting-common-issues)
10. [Tips & Best Practices](#10-tips--best-practices)

---

## 1. How to Merge Multiple PDFs into One

**What this does:** Combines two or more PDF files into a single file, in the order you list them.

**When to use it:** You have quarterly reports, chapters, or sections as separate files and need one consolidated document.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/pdf-toolkit
```

**Step 2 — List your source PDFs to confirm they exist.**

```bash
ls ~/Documents/reports/
```

Example output:
```
q1-2024.pdf  q2-2024.pdf  q3-2024.pdf  q4-2024.pdf
```

**Step 3 — Run the merge command.**  
The output file comes first, then the input files in the order you want them merged.

```bash
python3 main.py merge ~/Documents/annual-2024.pdf ~/Documents/reports/q1-2024.pdf ~/Documents/reports/q2-2024.pdf ~/Documents/reports/q3-2024.pdf ~/Documents/reports/q4-2024.pdf
```

Expected output:
```
✅ Merged 4 PDFs into /home/user/Documents/annual-2024.pdf
   Output size: 1,847,296 bytes
```

**Step 4 — Verify the merged file.**

```bash
python3 main.py info ~/Documents/annual-2024.pdf
```

The page count should equal the total pages from all four source files.

**Result:** One PDF at `~/Documents/annual-2024.pdf` containing all four quarterly reports in order.

---

## 2. How to Split a PDF into Individual Pages

**What this does:** Takes a multi-page PDF and creates one separate file per page. A 10-page PDF becomes 10 one-page PDFs.

**When to use it:** You need to distribute individual pages separately, or you want to selectively share specific pages without manually picking them out.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/pdf-toolkit
```

**Step 2 — Check how many pages your PDF has.**  
This helps you know how many files to expect.

```bash
python3 main.py info ~/Downloads/presentation.pdf
```

Output:
```
📄 PDF Information:
   Title: Q3 Strategy Presentation
   Pages: 8
   Author: Marketing Team
   Subject:
   Size: 2,097,152 bytes
   Encrypted: False
```

**Step 3 — Create a directory for the output files.**  
The skill can create the directory, but it's good practice to create it first.

```bash
mkdir ~/Downloads/presentation-pages
```

**Step 4 — Run the split command.**

```bash
python3 main.py split ~/Downloads/presentation.pdf ~/Downloads/presentation-pages/
```

Expected output:
```
✅ Split 8 pages into 8 files
   Output directory: /home/user/Downloads/presentation-pages/
```

**Step 5 — Verify the output.**

```bash
ls ~/Downloads/presentation-pages/
```

```
presentation_page_1.pdf  presentation_page_3.pdf  presentation_page_5.pdf  presentation_page_7.pdf
presentation_page_2.pdf  presentation_page_4.pdf  presentation_page_6.pdf  presentation_page_8.pdf
```

**Result:** 8 individual PDF files, one per page of the original presentation.

---

## 3. How to Extract a Range of Pages

**What this does:** Pulls a contiguous block of pages from a PDF into a new, smaller PDF.

**When to use it:** You have a large report and need to send only the executive summary (pages 1–4) or a specific section (pages 15–22).

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/pdf-toolkit
```

**Step 2 — Find out how many pages the PDF has and which pages you need.**

```bash
python3 main.py info ~/Documents/full-report.pdf
```

Output:
```
📄 PDF Information:
   Title: Annual Performance Report 2024
   Pages: 48
   Author: Analytics Team
   Subject: Annual Report
   Size: 8,388,608 bytes
   Encrypted: False
```

**Step 3 — Extract the pages you need.**  
Page numbers are 1-indexed (first page = 1).

```bash
python3 main.py extract ~/Documents/full-report.pdf 1 4 ~/Documents/exec-summary.pdf
```

Expected output:
```
✅ Extracted 4 pages to /home/user/Documents/exec-summary.pdf
```

**Step 4 — Verify the extracted file.**

```bash
python3 main.py info ~/Documents/exec-summary.pdf
```

```
📄 PDF Information:
   Title: Annual Performance Report 2024
   Pages: 4
   Author: Analytics Team
   Subject: Annual Report
   Size: 524,288 bytes
   Encrypted: False
```

**Result:** A 4-page PDF containing only the executive summary, ready to email or share.

---

## 4. How to Check a PDF's Info and Page Count

**What this does:** Displays a PDF's metadata — title, author, page count, file size, and whether it's encrypted — without opening it in a PDF viewer.

**When to use it:** You received a PDF and want to know what's inside before opening it. Or you're scripting PDF operations and need page counts programmatically.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/pdf-toolkit
```

**Step 2 — Run the info command.**

```bash
python3 main.py info ~/Downloads/contract.pdf
```

**Output:**
```
📄 PDF Information:
   Title: Master Service Agreement 2024
   Pages: 22
   Author: Legal Department
   Subject: Service Contract
   Size: 716,800 bytes
   Encrypted: False
```

**Step 3 — Check for encrypted PDFs.**  
If `Encrypted: True`, you cannot use this skill to process the file until the password is removed.

**Result:** You know exactly what's in the file: 22 pages, not encrypted, authored by the Legal Department. You can now confidently run extract, split, or merge operations on it.

---

## 5. How to Compress a Large PDF

**What this does:** Rewrites a PDF, which can reduce file size by removing redundant internal structures.

**When to use it:** You have a PDF that's too large to email (most email clients limit attachments to 10–25 MB) and want to try reducing its size.

**Important note:** This compression works on internal PDF structure, not on embedded images. Heavily image-based PDFs may see minimal reduction. Results vary — always check the output size.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/pdf-toolkit
```

**Step 2 — Check the original file size.**

```bash
python3 main.py info ~/Documents/large-report.pdf
```

Output:
```
📄 PDF Information:
   Title: Technical Documentation
   Pages: 45
   Author: Engineering
   Subject:
   Size: 15,728,640 bytes
   Encrypted: False
```

**Step 3 — Run compress.**

```bash
python3 main.py compress ~/Documents/large-report.pdf ~/Documents/large-report-small.pdf
```

Output:
```
✅ Compressed PDF: 22.3% reduction
   Original: 15,728,640 bytes
   New: 12,218,956 bytes
```

**Step 4 — Check the result meets your needs.**  
If the reduction wasn't enough, the file may be dominated by embedded images. In that case, consider using Ghostscript (`gs`) for deeper compression.

**Result:** A compressed copy of your PDF at a reduced file size, with the original unchanged.

---

## 6. How to Rotate a Sideways-Scanned Document

**What this does:** Rotates every page in a PDF by 90, 180, or 270 degrees, creating a correctly-oriented copy.

**When to use it:** You scanned documents on a copier that saved them sideways, or received a PDF where all pages are rotated.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/pdf-toolkit
```

**Step 2 — Determine the rotation needed.**

- If pages are rotated 90° clockwise (tilted to the right), use `270` to correct
- If pages are rotated 90° counterclockwise (tilted to the left), use `90` to correct
- If pages are upside down, use `180`

**Step 3 — Run rotate.**

```bash
python3 main.py rotate ~/Documents/scan-sideways.pdf ~/Documents/scan-fixed.pdf 270
```

Output:
```
✅ Rotated 12 pages by 270°
   Output: /home/user/Documents/scan-fixed.pdf
```

**Step 4 — Open the output to verify orientation.**  
Use your system's PDF viewer to confirm all pages are now correctly oriented.

**Result:** A corrected PDF at the output path. Your original scan is unchanged.

---

## 7. Automating with Cron

You can schedule PDF Toolkit to run automatically — for example, merging monthly reports into a quarterly file on the first of each month.

### Open the cron editor

```bash
crontab -e
```

### Cron Expression Reference

| Expression | Meaning |
|------------|---------|
| `0 9 1 * *` | First day of each month at 9 AM |
| `0 8 * * 1` | Every Monday at 8 AM |
| `0 22 * * *` | Every day at 10 PM |
| `0 6 1 1,4,7,10 *` | First day of each quarter at 6 AM |

### Example: Merge all monthly reports on the first of each month

```bash
0 9 1 * * cd /home/yourname/smfworks-skills/skills/pdf-toolkit && python3 main.py merge /home/yourname/Reports/monthly-$(date +\%Y-\%m).pdf /home/yourname/Reports/week1.pdf /home/yourname/Reports/week2.pdf /home/yourname/Reports/week3.pdf /home/yourname/Reports/week4.pdf >> /home/yourname/logs/pdf-toolkit.log 2>&1
```

### Example: Compress a new report every night

```bash
0 22 * * * cd /home/yourname/smfworks-skills/skills/pdf-toolkit && python3 main.py compress /home/yourname/Reports/daily-report.pdf /home/yourname/Reports/daily-report-compressed.pdf >> /home/yourname/logs/pdf-toolkit.log 2>&1
```

### Create the log directory

```bash
mkdir -p ~/logs
```

### Check logs after a run

```bash
cat ~/logs/pdf-toolkit.log
```

---

## 8. Combining with Other Skills

**PDF Toolkit + File Organizer:** Use File Organizer to move all PDFs into one folder, then merge them:

```bash
# Step 1: Organize Downloads, moving PDFs to Documents subfolder
python3 ~/smfworks-skills/skills/file-organizer/main.py organize-type ~/Downloads

# Step 2: Merge all PDFs that were just organized
python3 ~/smfworks-skills/skills/pdf-toolkit/main.py merge ~/combined.pdf ~/Downloads/Documents/*.pdf
```

**PDF Toolkit + Report Generator:** Generate a report, then immediately compress it for email delivery:

```bash
# After generating a report:
python3 ~/smfworks-skills/skills/pdf-toolkit/main.py compress ~/Reports/generated-report.pdf ~/Reports/generated-report-email.pdf
```

---

## 9. Troubleshooting Common Issues

### `PyPDF2 not installed. Run: pip install PyPDF2`

The package is missing from your Python environment.  
**Fix:** `pip install PyPDF2` — or if that doesn't work: `python3 -m pip install PyPDF2`

---

### `Invalid page range. PDF has 10 pages (1-10).`

You specified a page number outside the document's actual range.  
**Fix:** Run `python3 main.py info your-file.pdf` first to check the page count, then use valid numbers.

---

### `Need at least 2 PDFs to merge`

You provided only one input file to the merge command.  
**Fix:** The merge command format is `merge output.pdf input1.pdf input2.pdf`. Make sure you have at least two input files listed after the output.

---

### `File too large: X bytes (max: 104857600)`

The input PDF is over 100 MB.  
**Fix:** Split the file with another tool first, or use Ghostscript for large file handling: `gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=smaller.pdf input.pdf`

---

### `Rotation must be one of: [90, 180, 270]`

You used a rotation value other than 90, 180, or 270.  
**Fix:** Use `270` for counterclockwise 90°. There is no `-90` option.

---

### The output PDF looks identical — compression didn't work

For image-heavy PDFs, PyPDF2-based compression has minimal effect.  
**Fix:** Use Ghostscript for deeper compression: `gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dBATCH -sOutputFile=output.pdf input.pdf`

---

## 10. Tips & Best Practices

**Always check page count with `info` before using `extract` or `split`.** Running `extract` with incorrect page numbers will fail — know your document's size first.

**For the merge command, the output file is listed FIRST.** This is different from most tools. The format is: `merge OUTPUT.pdf input1.pdf input2.pdf` — not `merge input1.pdf input2.pdf OUTPUT.pdf`.

**Keep your originals.** PDF Toolkit never modifies input files, but it's still good practice to keep originals until you've verified the output looks correct.

**Compress before emailing, not before archiving.** For long-term storage, keep the original quality PDF. Use the compressed version only for transmission. Re-compressing an already-compressed PDF yields diminishing returns and can degrade quality.

**For pages 1 through N, `extract` is easier than `split + select`.** Use `extract` when you know the range. Use `split` when you need individual pages and will pick what you need from the results.

**Test your cron jobs manually first.** Before scheduling an automated merge, run the exact command manually to verify it produces the expected output. Only then add it to crontab.

**Use absolute paths in cron.** Cron doesn't expand `~`. Always use full paths like `/home/yourname/` instead of `~/` in crontab entries.
