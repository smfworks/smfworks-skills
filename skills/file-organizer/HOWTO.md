# File Organizer — How-To Guide

**Prerequisites:** Setup complete (see SETUP.md)

---

## Table of Contents

1. [How to Clean Up Your Downloads Folder](#1-how-to-clean-up-your-downloads-folder)
2. [How to Organize Files by Date](#2-how-to-organize-files-by-date)
3. [How to Sort a Photo Archive](#3-how-to-sort-a-photo-archive)
4. [How to Find Duplicate Files](#4-how-to-find-duplicate-files)
5. [How to Safely Organize Without Moving Originals](#5-how-to-safely-organize-without-moving-originals)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Clean Up Your Downloads Folder

**What this does:** Sorts all files in your Downloads folder into named subfolders by file type — Documents, Images, Videos, Audio, Code, etc.

**When to use it:** Your Downloads folder has hundreds of mixed files with no obvious structure and you want to find things quickly.

### Steps

**Step 1 — Navigate to the skill directory.**  
This is where the skill's Python file lives.

```bash
cd ~/smfworks-skills/skills/file-organizer
```

**Step 2 — Check what's currently in your Downloads folder.**  
This helps you understand what the skill is about to process.

```bash
ls ~/Downloads | head -20
```

You might see output like:
```
invoice-2024-03.pdf
photo_beach.jpg
zoom_installer.pkg
presentation_q4.pptx
script.py
vacation_video.mp4
resume_draft.docx
```

**Step 3 — Run organize-type on your Downloads folder.**  
This moves every file into a named subfolder based on its extension.

```bash
python3 main.py organize-type ~/Downloads
```

You should see:
```
✅ Organized 47 files by type

Organized into:
  Archives: 3 files
  Audio: 5 files
  Code: 2 files
  Documents: 18 files
  Images: 11 files
  Other: 2 files
  Presentations: 3 files
  Videos: 3 files
```

**Step 4 — Verify the result.**

```bash
ls ~/Downloads
```

You should see:
```
Archives  Audio  Code  Documents  Images  Other  Presentations  Videos
```

**Result:** Your Downloads folder now has clear named subfolders. Finding any file takes seconds — just browse to the right type folder.

---

## 2. How to Organize Files by Date

**What this does:** Moves files into `YYYY/MM` subfolders based on when each file was last modified. January 2024 files go to `2024/01`, March 2025 files go to `2025/03`, and so on.

**When to use it:** You have a folder full of documents, receipts, or exports from various dates and want a chronological archive.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/file-organizer
```

**Step 2 — Identify a folder with date-mixed files.**  
Folders of invoices, receipts, exports, or project files work well here.

```bash
ls ~/Documents/receipts | head -10
```

Example contents:
```
receipt_amazon_jan.pdf
receipt_grocery_feb.pdf
invoice_march.pdf
statement_q1.pdf
```

**Step 3 — Run organize-date.**  
Files will be moved into subfolders named by year and month.

```bash
python3 main.py organize-date ~/Documents/receipts
```

Output:
```
✅ Organized 24 files by date

Organized into:
  2023/10: 3 files
  2023/11: 5 files
  2024/01: 7 files
  2024/02: 5 files
  2024/03: 4 files
```

**Step 4 — Browse the result.**

```bash
ls ~/Documents/receipts/
```

```
2023  2024
```

```bash
ls ~/Documents/receipts/2024/
```

```
01  02  03
```

**Result:** Every file is in a year/month folder matching when it was created. You can now quickly navigate to "all files from February 2024" with a single folder click.

---

## 3. How to Sort a Photo Archive

**What this does:** Takes a folder of raw camera photos and sorts them into dated subfolders, sending the results to a separate archive location so the original folder is left empty.

**When to use it:** You dumped photos from a camera or phone into one folder and want to build a clean, browsable archive without losing anything.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/file-organizer
```

**Step 2 — Create your archive destination folder.**  
This is where the organized photos will go. Creating it first makes the output predictable.

```bash
mkdir -p ~/Photos/archive
```

**Step 3 — Run organize-date with a destination.**  
Specifying a destination means the source folder `camera-dump` will be cleared while the archive grows.

```bash
python3 main.py organize-date ~/Photos/camera-dump ~/Photos/archive
```

Output:
```
✅ Organized 312 files by date

Organized into:
  2023/12: 48 files
  2024/01: 87 files
  2024/02: 103 files
  2024/03: 74 files
```

**Step 4 — Verify the archive.**

```bash
ls ~/Photos/archive/2024/01/ | head -5
```

```
IMG_0142.jpg
IMG_0143.jpg
IMG_0144.jpg
IMG_0145.jpg
IMG_0146.jpg
```

**Step 5 — Verify camera-dump is now empty.**

```bash
ls ~/Photos/camera-dump
```

The folder should be empty (or show only the now-empty subdirectories if any existed).

**Result:** Your `~/Photos/archive` now has a clean `YYYY/MM` structure with every photo in its correct date folder. Future dumps can be run through the same command to extend the archive.

---

## 4. How to Find Duplicate Files

**What this does:** Scans a directory (and all its subfolders) looking for files with identical contents. It uses MD5 hashing, so it catches duplicates even when the filenames differ.

**When to use it:** Your drive is getting full and you suspect you have duplicate files scattered across folders. Or you merged two folders and want to clean up redundancy.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/file-organizer
```

**Step 2 — Run find-duplicates on your target folder.**  
Scanning a large folder may take a minute if there are many files.

```bash
python3 main.py find-duplicates ~/Documents
```

Output (if duplicates exist):
```
🔍 Found 4 duplicate groups
   Total duplicate files: 11

Duplicate groups:

  Hash: a1b2c3d4e5f67890...
    - /home/user/Documents/reports/q1_report.pdf
    - /home/user/Documents/archive/q1_report.pdf
    - /home/user/Documents/backup/q1_report.pdf

  Hash: 9f8e7d6c5b4a3210...
    - /home/user/Documents/contracts/vendor_agreement.docx
    - /home/user/Documents/vendor_agreement_copy.docx

  Hash: 1234567890abcdef...
    - /home/user/Documents/photos/headshot.jpg
    - /home/user/Documents/headshot_final.jpg
    - /home/user/Documents/headshot_v2.jpg

  Hash: fedcba9876543210...
    - /home/user/Documents/data/export.csv
    - /home/user/Documents/export_old.csv
```

**Step 3 — Review the duplicate groups.**  
For each group, keep the copy you want and delete the rest manually.

```bash
# Example: remove an extra copy you don't need
rm ~/Documents/backup/q1_report.pdf
rm ~/Documents/vendor_agreement_copy.pdf
```

**Step 4 — Re-run to confirm duplicates are resolved.**

```bash
python3 main.py find-duplicates ~/Documents
```

Output:
```
🔍 Found 0 duplicate groups
   Total duplicate files: 0
```

**Result:** You've identified every duplicate file in your Documents folder. Manually reviewing and deleting the extras frees up storage and reduces confusion.

---

## 5. How to Safely Organize Without Moving Originals

**What this does:** Uses a destination directory so the original folder is left untouched. The organized copy lands elsewhere, letting you review it before committing.

**When to use it:** You're uncertain about the outcome and want to preview an organized version before making permanent changes to a folder you depend on.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/file-organizer
```

**Step 2 — Create a destination folder.**

```bash
mkdir ~/Desktop-organized
```

**Step 3 — Run with a destination specified.**  
Note: the source directory files will still be moved. The destination just controls *where* they go. Using a different destination effectively empties the source into the organized structure.

```bash
python3 main.py organize-type ~/Desktop ~/Desktop-organized
```

Output:
```
✅ Organized 22 files by type

Organized into:
  Documents: 9 files
  Images: 7 files
  Code: 4 files
  Other: 2 files
```

**Step 4 — Review the organized destination before removing anything.**

```bash
ls ~/Desktop-organized/
```

```
Code  Documents  Images  Other
```

**Step 5 — If satisfied, your original Desktop is now clear.**  
If you're not happy, you can move files back manually since they're all in predictable named folders.

**Result:** You have a clean organized copy at `~/Desktop-organized` and your Desktop is emptied into the organized structure. Review, adjust manually if needed, then you're done.

---

## 6. Automating with Cron

You can schedule File Organizer to run automatically on a recurring basis — for example, every Sunday night to keep your Downloads folder clean without any manual effort.

### How to Open crontab

```bash
crontab -e
```

This opens the cron editor. If asked which editor to use, choose `nano` (easiest for beginners).

### Cron Expression Reference

| Expression | Meaning |
|------------|---------|
| `0 23 * * 0` | Every Sunday at 11 PM |
| `0 2 * * 1` | Every Monday at 2 AM |
| `0 9 1 * *` | First day of every month at 9 AM |
| `0 22 * * *` | Every day at 10 PM |
| `30 18 * * 5` | Every Friday at 6:30 PM |

### Example: Organize Downloads by Type Every Sunday Night

Add this line to your crontab:

```bash
0 23 * * 0 cd /home/yourname/smfworks-skills/skills/file-organizer && python3 main.py organize-type /home/yourname/Downloads >> /home/yourname/logs/file-organizer.log 2>&1
```

**Important:** Replace `yourname` with your actual username. Use the full path — cron does not expand `~`.

### Example: Organize a Photo Dump Every Monday at 2 AM

```bash
0 2 * * 1 cd /home/yourname/smfworks-skills/skills/file-organizer && python3 main.py organize-date /home/yourname/Photos/camera-dump /home/yourname/Photos/archive >> /home/yourname/logs/photo-archive.log 2>&1
```

### Creating the Log Directory

Before your first scheduled run, create the log directory:

```bash
mkdir -p ~/logs
```

### Checking Cron Output

View the log after a scheduled run:

```bash
cat ~/logs/file-organizer.log
```

You should see the usual success output:
```
✅ Organized 12 files by type

Organized into:
  Documents: 5 files
  Images: 4 files
  Other: 3 files
```

---

## 7. Combining with Other Skills

**File Organizer + PDF Toolkit:** Use File Organizer to move all PDFs into a Documents folder, then run PDF Toolkit to merge them into a single document.

```bash
# Step 1: Move PDFs into Documents folder
python3 ~/smfworks-skills/skills/file-organizer/main.py organize-type ~/Downloads

# Step 2: Merge all PDFs in Documents folder
python3 ~/smfworks-skills/skills/pdf-toolkit/main.py merge ~/Downloads/Documents/
```

**File Organizer + System Monitor:** Schedule both to run together — organize files while checking system health.

---

## 8. Troubleshooting Common Issues

### Files didn't move — the organized folders appear empty

**Likely cause:** You specified a destination that doesn't exist and the skill couldn't create it.  
**Fix:** Create the destination first with `mkdir -p ~/destination-folder`, then re-run.

---

### `Source directory does not exist`

**Likely cause:** Typo in the directory path.  
**Fix:** Run `ls ~/YourFolder` to verify the path exists, then copy-paste it exactly into the command.

---

### Some files didn't move and appeared in errors

**Likely cause:** Those files are over 100 MB (the skill's size limit) or you don't have read permission on them.  
**Fix:** Check the error message — it will say `Skipped large file filename: X bytes` or `Permission denied`. Move oversized files manually; fix permissions with `ls -la`.

---

### `Destination must be within home directory or temp`

**Likely cause:** You specified a destination on an external drive or mount point outside your home directory.  
**Fix:** Use a path inside your home directory (`~/`) or `/tmp`. For external drives, consider mounting them inside your home directory.

---

### The same file appears as a duplicate of itself

**Likely cause:** The file was already copied to a subfolder in a previous run, and `find-duplicates` is scanning both the parent and child.  
**Fix:** Be aware that after running `organize-type` or `organize-date`, the organized subfolders are inside the original directory. Running `find-duplicates` on the same folder afterward may flag the just-organized files if any originals remain. Always clean up properly after each run.

---

## 9. Tips & Best Practices

**Always verify your path before running.** Run `ls ~/YourFolder` before running the skill on it. A typo can accidentally empty the wrong folder.

**Use a destination folder for folders you depend on.** If you organize `~/Documents` in place and something goes wrong, finding your files requires navigating into subfolders. Using a destination (`~/Documents-sorted`) means you can review first.

**The organize commands move files from the top level only.** Files inside subfolders of the source directory are not touched. If you want to organize a folder that has many subfolders, run the command once per subfolder, or flatten the structure first.

**find-duplicates is read-only — it never deletes anything.** Use it freely even on important directories. Review the output and manually delete duplicates you're confident you don't need.

**For photo archives, date-based organization is the gold standard.** `organize-date` mirrors how most photo management software (Apple Photos, Google Photos) organizes internally — by year and month. This makes it easy to sync with other tools.

**Log your cron runs.** Always add `>> ~/logs/file-organizer.log 2>&1` to cron entries so you can review what happened after each automatic run. Without logging, silent failures are invisible.

**Run find-duplicates before a large organize operation.** If you have duplicates, an organize operation will move them all to the same subfolder, making them easier to spot and delete. Running find-duplicates first gives you a clean view.
