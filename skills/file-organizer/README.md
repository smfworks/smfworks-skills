# File Organizer

> Stop drowning in a messy Downloads folder — sort any directory by date or file type in seconds, and find duplicate files eating your storage.

**Tier:** Free — no subscription required  
**Version:** 1.0  
**Category:** Productivity / File Management

---

## What It Does

File Organizer is an OpenClaw skill that automatically sorts the files in any folder into a clean, logical structure. You can organize by modification date (files land in `YYYY/MM` subfolders), by file type (Images, Documents, Videos, Audio, Code, Archives, and more), or scan a directory tree for exact duplicate files.

It handles name collisions automatically — if two files have the same name in the destination, it adds a numeric suffix rather than overwriting. It also enforces safety limits: files over 100 MB are skipped, system directories are off-limits, and path traversal tricks are blocked.

**What it does NOT do:** It does not rename files, edit file contents, recursively organize nested subfolders in a single pass (it processes one directory level at a time), or delete files — even duplicates are only reported, not removed.

---

## Prerequisites

Before installing, confirm:

- [ ] **Python 3.8 or newer** — run `python3 --version` to check
- [ ] **OpenClaw installed** — run `openclaw --version` to check
- [ ] **No subscription required** — this is a free tier skill
- [ ] **No API keys required** — works entirely offline
- [ ] **Write access to the directories you want to organize**

---

## Installation

**Step 1 — Clone the skills repository (if you haven't already):**

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

You should see:
```
Cloning into '/home/yourname/smfworks-skills'...
remote: Enumerating objects: 412, done.
Receiving objects: 100% (412/412), done.
```

**Step 2 — Navigate to the skill directory:**

```bash
cd ~/smfworks-skills/skills/file-organizer
```

**Step 3 — Verify the skill is ready:**

```bash
python3 main.py
```

You should see:
```
Usage: python main.py <command> [options]

Commands:
  organize-date <directory> [dest_directory]  - Organize by date
  organize-type <directory> [dest_directory]  - Organize by file type
  find-duplicates <directory>               - Find duplicate files

Examples:
  python main.py organize-date ~/Downloads
  python main.py organize-type ~/Documents ~/Organized
  python main.py find-duplicates ~/Pictures
```

If you see this output, the skill is installed and ready to use.

---

## Quick Start

The fastest way to get value from File Organizer: sort your Downloads folder by file type.

```bash
cd ~/smfworks-skills/skills/file-organizer
python3 main.py organize-type ~/Downloads
```

Expected output:
```
✅ Organized 47 files by type

Organized into:
  Archives: 3 files
  Code: 2 files
  Documents: 18 files
  Images: 14 files
  Other: 4 files
  Videos: 6 files
```

Your Downloads folder now has named subfolders — Documents, Images, Videos, etc. — each containing the relevant files.

---

## Command Reference

### `organize-date`

Moves every file in a directory into date-based subfolders using the file's last modification date. Subfolders are created in `YYYY/MM` format (e.g., `2024/03` for March 2024).

**Usage:**
```bash
python3 main.py organize-date <directory> [dest_directory]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `directory` | ✅ Yes | Source directory to organize | `~/Downloads` |
| `dest_directory` | ❌ No | Where to put organized folders. Defaults to `directory` if omitted. | `~/Organized` |

**Options:** None

**Example — organize in place:**
```bash
python3 main.py organize-date ~/Downloads
```

**Output:**
```
✅ Organized 23 files by date

Organized into:
  2023/11: 4 files
  2024/01: 7 files
  2024/02: 5 files
  2024/03: 7 files
```

**Example — organize into a separate destination:**
```bash
python3 main.py organize-date ~/Downloads ~/Downloads-Sorted
```

**Output:**
```
✅ Organized 23 files by date

Organized into:
  2023/11: 4 files
  2024/01: 7 files
  2024/02: 5 files
  2024/03: 7 files
```

---

### `organize-type`

Moves every file in a directory into type-based subfolders. The skill classifies files by extension into these categories:

| Category | Extensions |
|----------|------------|
| Images | .jpg .jpeg .png .gif .bmp .svg .webp .ico |
| Documents | .pdf .doc .docx .txt .rtf .odt .md |
| Spreadsheets | .xls .xlsx .csv .ods |
| Presentations | .ppt .pptx .odp .key |
| Archives | .zip .rar .7z .tar .gz .bz2 |
| Videos | .mp4 .avi .mkv .mov .wmv .flv |
| Audio | .mp3 .wav .flac .aac .ogg .m4a .wma |
| Code | .py .js .html .css .java .cpp .c .h .go .rs .rb .php |
| Data | .json .xml .yaml .yml .sql .db |
| Other | Everything else |

**Usage:**
```bash
python3 main.py organize-type <directory> [dest_directory]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `directory` | ✅ Yes | Source directory to organize | `~/Downloads` |
| `dest_directory` | ❌ No | Where to put organized folders. Defaults to `directory` if omitted. | `~/Sorted` |

**Options:** None

**Example — organize in place:**
```bash
python3 main.py organize-type ~/Desktop
```

**Output:**
```
✅ Organized 31 files by type

Organized into:
  Documents: 12 files
  Images: 9 files
  Audio: 3 files
  Code: 4 files
  Other: 3 files
```

**Example — send to a different folder:**
```bash
python3 main.py organize-type ~/Desktop ~/Desktop-Sorted
```

**Output:**
```
✅ Organized 31 files by type

Organized into:
  Documents: 12 files
  Images: 9 files
  Audio: 3 files
  Code: 4 files
  Other: 3 files
```

---

### `find-duplicates`

Scans a directory (and all subdirectories, up to 10 levels deep) for exact duplicate files. Files are compared by MD5 hash — meaning identical content is detected even if the filenames differ. Files over 100 MB and symbolic links are skipped.

**Usage:**
```bash
python3 main.py find-duplicates <directory>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `directory` | ✅ Yes | Directory to scan for duplicates | `~/Pictures` |

**Options:** None

**Example:**
```bash
python3 main.py find-duplicates ~/Pictures
```

**Output (duplicates found):**
```
🔍 Found 3 duplicate groups
   Total duplicate files: 8

Duplicate groups:

  Hash: a1b2c3d4e5f67890...
    - /home/user/Pictures/vacation/beach.jpg
    - /home/user/Pictures/backup/beach.jpg
    - /home/user/Pictures/beach_copy.jpg

  Hash: 9f8e7d6c5b4a3210...
    - /home/user/Pictures/family/christmas.png
    - /home/user/Pictures/christmas_2023.png

  Hash: 1234567890abcdef...
    - /home/user/Pictures/portrait.jpg
    - /home/user/Pictures/portrait_final.jpg
    - /home/user/Pictures/archive/portrait.jpg
```

**Output (no duplicates):**
```
🔍 Found 0 duplicate groups
   Total duplicate files: 0
```

---

## Use Cases

### 1. Tame your Downloads folder weekly

Most people's Downloads folder is a graveyard of random files. Run organize-type once a week to keep it manageable:

```bash
python3 main.py organize-type ~/Downloads
```

Result: Your Downloads folder will have clear subfolders. Finding that PDF you downloaded last Tuesday becomes trivial.

---

### 2. Archive project files by date

After finishing a project, you might have a folder full of files with no clear organization. Sort them by date to understand what was created when:

```bash
python3 main.py organize-date ~/Projects/website-redesign
```

Result: Files land in `2024/01`, `2024/02`, etc. — a clear timeline of the project.

---

### 3. Sort photos into a clean archive

A camera roll or photo dump is perfect for date-based organization:

```bash
python3 main.py organize-date ~/Photos/camera-dump ~/Photos/archive
```

Result: Photos from January 2024 go to `~/Photos/archive/2024/01`, February to `2024/02`, and so on. Your original `camera-dump` folder is emptied.

---

### 4. Find storage hogs hiding as duplicates

If a drive is getting full, scan for duplicates before buying more storage:

```bash
python3 main.py find-duplicates ~/Documents
```

Result: You'll see exactly which files are duplicated and where. Manually delete the ones you don't need.

---

### 5. Organize files to a separate destination (safe mode)

If you're nervous about moving files inside a folder you depend on, send the organized output somewhere else:

```bash
python3 main.py organize-type ~/Desktop ~/Desktop-Organized
```

Result: Your Desktop is untouched. The organized version appears in `~/Desktop-Organized`. Review it, then delete the original if satisfied.

---

## Configuration

File Organizer requires no configuration file or environment variables. All behavior is controlled by the command you run and the arguments you pass.

**Built-in limits (not configurable):**

| Setting | Value | Reason |
|---------|-------|--------|
| Max file size | 100 MB | Prevents accidental processing of large media files |
| Max duplicate counter | 1000 | Prevents infinite loops on collision handling |
| Max directory depth (find-duplicates) | 10 levels | Prevents runaway traversal |
| System directories | Blocked | Safety: cannot operate on `/bin`, `/etc`, `/usr`, etc. |

---

## Troubleshooting

### `Source directory does not exist: /path/to/folder`

**What happened:** You passed a directory path that doesn't exist on your system.  
**Fix:** Double-check the path. Use `ls ~/Downloads` to verify the folder exists. Use the full path if you're unsure: `python3 main.py organize-type /home/yourname/Downloads`

---

### `Source is not a directory: /path/to/file.txt`

**What happened:** You passed a file path instead of a folder path.  
**Fix:** You must point to a folder, not a file. Run the command on the folder that *contains* your files.

---

### `Cannot operate on system directory: /usr/local`

**What happened:** You tried to organize a protected system directory.  
**Fix:** Only organize directories you own, such as folders in your home directory (`~/`). System directories are blocked for your protection.

---

### `Destination must be within home directory or temp: /mnt/external`

**What happened:** You specified a destination outside your home directory or `/tmp`.  
**Fix:** Use a destination path inside your home directory. Example: `~/Organized` instead of `/mnt/external/Organized`.

---

### `Skipped large file report.zip: 157286400 bytes`

**What happened:** A file in your directory is larger than 100 MB and was skipped.  
**Fix:** This is expected behavior. Large files are skipped to prevent long processing times. Move oversized files manually if needed.

---

### `Error moving filename.pdf: [Errno 13] Permission denied`

**What happened:** You don't have write permission on the source directory or destination.  
**Fix:** Check permissions with `ls -la ~/YourFolder`. If the folder is owned by root, you cannot organize it without `sudo` (not recommended). Only organize folders you own.

---

### `Too many duplicates for report.pdf`

**What happened:** There are already 1000+ files named `report_1.pdf`, `report_2.pdf`, etc. in the destination, and the skill hit its safety limit.  
**Fix:** Clean up old duplicates manually in the destination folder, then re-run.

---

## FAQ

**Q: Will File Organizer delete any of my files?**  
A: No. The skill only moves files — it never deletes them. Even the `find-duplicates` command only *reports* duplicates; it does not remove them. You decide what to delete.

---

**Q: What happens if two files have the same name in the destination?**  
A: The skill adds a number suffix. If `report.pdf` already exists, the incoming file becomes `report_1.pdf`. The next becomes `report_2.pdf`, and so on — up to 1000.

---

**Q: Can I undo an organize operation?**  
A: Not automatically. The skill does not keep a log of what moved where. If you need to undo, use a destination folder (`organize-type ~/Downloads ~/Downloads-Sorted`) and only delete the source files once you're happy with the result.

---

**Q: Will it process files in subfolders?**  
A: For `organize-date` and `organize-type`, no — only the files directly in the directory you specify are processed. For `find-duplicates`, yes — it scans all subdirectories up to 10 levels deep.

---

**Q: What about files with no extension?**  
A: They go into the `Other` category when using `organize-type`.

---

**Q: Can I organize by file size?**  
A: Not in the current version. The skill supports `organize-date`, `organize-type`, and `find-duplicates` only.

---

**Q: Does it work on Windows or macOS?**  
A: The skill is written in Python and should work on macOS and Linux. Windows is not officially tested. System directory protection logic is tuned for Unix paths.

---

**Q: What if I want to organize a network drive?**  
A: Network drives mapped to paths outside your home directory may be blocked by the destination safety check. Mount the drive inside your home directory if possible.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| OpenClaw | Any version |
| Operating System | Linux, macOS |
| Subscription Tier | Free |
| External APIs | None |
| Internet Connection | Not required |
| External Python packages | None (stdlib only) |

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/file-organizer)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord Community](https://discord.gg/smfworks)
- 📧 [Support Email](mailto:support@smfworks.com)
