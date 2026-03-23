# PDF Toolkit — Setup Guide

**Estimated setup time:** 5–10 minutes  
**Difficulty:** Easy  
**Tier:** Free — no subscription, no API keys required

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| Python 3.8+ | Built into macOS 12+; `python3` on Linux | Free |
| pip | Python package manager (comes with Python) | Free |
| PyPDF2 | Python library for PDF manipulation | Free |
| smfworks-skills repository | Cloned via git | Free |
| A PDF file | For testing during setup | Free |

---

## Step 1 — Verify Python Is Installed

```bash
python3 --version
```

Expected output:
```
Python 3.11.4
```

Any version 3.8 or newer works. If Python is missing, download it from [python.org](https://python.org) or use your system's package manager.

---

## Step 2 — Verify pip Is Available

```bash
pip --version
```

Expected output:
```
pip 23.1.2 from /usr/local/lib/python3.11/site-packages/pip (python 3.11)
```

If pip is missing, install it with:
```bash
python3 -m ensurepip --upgrade
```

---

## Step 3 — Install PyPDF2

This is the only external dependency PDF Toolkit needs.

```bash
pip install PyPDF2
```

Expected output:
```
Collecting PyPDF2
  Downloading PyPDF2-3.0.1-py3-none-any.whl (232 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 232.7/232.7 kB 2.4 MB/s eta 0:00:00
Installing collected packages: PyPDF2
Successfully installed PyPDF2-3.0.1
```

If you see `Successfully installed`, PyPDF2 is ready.

---

## Step 4 — Get the Skills Repository

If you haven't already cloned the smfworks-skills repository:

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

If you already have it, update:

```bash
cd ~/smfworks-skills && git pull
```

---

## Step 5 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/pdf-toolkit
```

List the files:

```bash
ls
```

You should see:
```
HOWTO.md   README.md   SETUP.md   main.py
```

---

## Step 6 — Run the Skill to Verify

```bash
python3 main.py
```

Expected output:
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

If you see this, setup is complete.

---

## Verify Your Setup

Run a real test with any PDF on your system. If you don't have one handy, create a minimal test using any PDF from your Downloads folder.

```bash
python3 main.py info ~/Downloads/any-file.pdf
```

Expected output (values will vary by file):
```
📄 PDF Information:
   Title: Sample Document
   Pages: 4
   Author: Unknown
   Subject:
   Size: 123,456 bytes
   Encrypted: False
```

If you see page count and file size, everything is working correctly.

---

## Configuration Options

PDF Toolkit requires no configuration file or environment variables. All options are passed as command-line arguments at runtime. There is nothing to configure after installation.

---

## Troubleshooting Setup Issues

**`pip: command not found`**  
Use `pip3` instead of `pip`, or run `python3 -m pip install PyPDF2`.

**`PyPDF2 not installed. Run: pip install PyPDF2`**  
The package wasn't installed in the Python environment you're running. If you use virtual environments or conda, activate your environment first, then run `pip install PyPDF2`.

**`No such file or directory: main.py`**  
You're not in the skill directory. Run `cd ~/smfworks-skills/skills/pdf-toolkit` first.

**`ModuleNotFoundError: No module named 'PyPDF2'`**  
Same as above — pip and python3 may be pointing to different installations. Try `python3 -m pip install PyPDF2` to be sure they're linked correctly.

**`Permission denied` when installing PyPDF2**  
Try `pip install --user PyPDF2` to install it into your user directory instead of system-wide.

---

## Next Steps

Setup is complete. Head to **HOWTO.md** for walkthroughs:

- How to merge PDFs
- How to split a PDF into individual pages
- How to extract specific pages
- How to check PDF metadata
- How to automate PDF tasks with cron

```bash
cat HOWTO.md
```
