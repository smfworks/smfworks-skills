# Markdown Converter — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Free — no subscription, no API keys required

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| pip | Python package manager | Free |
| markdown | Python Markdown library | Free |
| smfworks-skills repository | Cloned via git | Free |
| A .md file | For testing | Free |

---

## Step 1 — Verify Python

```bash
python3 --version
```

Expected: `Python 3.9.x` or newer.

---

## Step 2 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 3 — Install the markdown Package

```bash
pip install markdown
```

Expected:
```
Collecting markdown
  Downloading Markdown-3.5.2-py3-none-any.whl (103 kB)
Installing collected packages: markdown
Successfully installed Markdown-3.5.2
```

---

## Step 4 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/markdown-converter
```

---

## Step 5 — Verify

```bash
python3 main.py
```

Expected:
```
Usage: python main.py <command> [options]
Commands:
  to-html <input.md> [output.html]    - Convert to HTML
  to-text <input.md> [output.txt]     - Convert to plain text
  toc <input.md>                       - Extract table of contents
  stats <input.md>                     - Count stats
```

---

## Verify Your Setup

Create a test Markdown file and convert it:

```bash
echo "# Test\n\nHello **world**!" > /tmp/test.md
cd /tmp
python3 ~/smfworks-skills/skills/markdown-converter/main.py to-html test.md
```

Expected:
```
✅ Success: {'success': True, 'input': '/tmp/test.md', 'output': '/tmp/test.html', 'characters': 25}
```

Check the output:
```bash
cat /tmp/test.html | grep -A5 "<body>"
```

You should see the HTML content. Setup is complete.

Clean up:
```bash
rm /tmp/test.md /tmp/test.html
```

---

## Configuration Options

No configuration file or environment variables needed.

**Important:** The skill only processes files in your current working directory. Before converting, `cd` to the folder containing your `.md` file, or use absolute paths.

---

## Troubleshooting

**`markdown not installed`** — Run `pip install markdown`.

**`Path outside allowed directory`** — The skill restricts access to files in the current working directory. `cd` to the directory containing your file before running.

**`Input file not found`** — Use the full path: `~/Documents/myfile.md`

---

## Next Steps

Setup complete. See **HOWTO.md** for walkthroughs on HTML conversion, plain text conversion, TOC extraction, stats, and batch processing.
