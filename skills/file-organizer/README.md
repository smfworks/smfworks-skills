# File Organizer

> Automatically organize messy folders into a clean structure by type, date, or custom rules

---

## What It Does

File Organizer automatically sorts the files in any folder into a clean, organized structure. Choose to organize by file type (Images, Documents, Videos), by date (Year > Month), or use custom rules you define. It handles duplicates, creates folders as needed, and can preview changes before making them.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install file-organizer
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Organize your Downloads folder in seconds:

```bash
python main.py organize ~/Downloads
```

---

## Commands

### `organize`

**What it does:** Sort files in a folder into an organized structure.

**Usage:**
```bash
python main.py organize [folder-path] [options]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `folder-path` | ✅ Yes | Folder to organize | `~/Downloads` |

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--by` | ❌ No | Organization method: `type`, `date`, or `size` | `--by type` |
| `--dry-run` | ❌ No | Preview changes without moving files | `--dry-run` |
| `--recursive` | ❌ No | Include subfolders | `--recursive` |

**Example:**
```bash
python main.py organize ~/Downloads
python main.py organize ~/Downloads --by type
python main.py organize ~/Downloads --by date
python main.py organize ~/Downloads --dry-run
```

**Output:**
```
📁 Organizing: ~/Downloads

Before:
  Downloads/
    report.pdf
    photo.jpg
    document.docx
    vacation.png
    data.xlsx

After (by type):
  Downloads/
    Documents/
      report.pdf
      document.docx
      data.xlsx
    Images/
      photo.jpg
      vacation.png

✅ Organized 5 files into 2 folders
```

---

### `rules`

**What it does:** Display the current organization rules being used.

**Usage:**
```bash
python main.py rules
```

**Example:**
```bash
python main.py rules
```

**Output:**
```
📋 File Organization Rules:
------------------------------------------------------------
By Type:
   📄 Documents → Documents/
   🖼️ Images   → Images/
   🎬 Videos   → Videos/
   🎵 Audio    → Audio/
   📦 Archives → Archives/

By Date:
   📅 Year/Month → YYYY/YYYY-MM/

By Size:
   📊 Large/Medium/Small → by file size thresholds
```

---

## Use Cases

- **Clean up Downloads:** Organize that ever-growing Downloads folder
- **Photo management:** Sort photos by year and month automatically
- **Project cleanup:** Organize messy project folders before archiving
- **Document归档:** Sort invoices, receipts, and contracts by date
- **Desktop cleanup:** Restore order to a cluttered desktop

---

## Tips & Tricks

- Always use `--dry-run` first to preview what will happen
- Organize by date works great for receipts and financial documents
- Combine with cron to organize folders automatically each week
- Use `--recursive` to include nested subfolders

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Files not moving | Check that `--dry-run` isn't set |
| Wrong organization | Use `--by type` or `--by date` to change method |
| Permission denied | Ensure you have write access to the folder |
| Duplicate files | Files with same name get a number suffix added |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- No external dependencies

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/file-organizer)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
