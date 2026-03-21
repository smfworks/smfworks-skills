# SMF Works Skills

A collection of free OpenClaw skills for small businesses.

## Skills

1. **File Organizer** - Organize files by date, type, and find duplicates
2. **PDF Toolkit** - Merge, split, extract, and compress PDFs
3. **Text Formatter** - Convert case, clean whitespace, count words

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills.git
cd smfworks-skills
```

## Usage

Each skill is in its own directory with a `main.py` file.

### File Organizer
```bash
python skills/file-organizer/main.py organize-date ~/Downloads
python skills/file-organizer/main.py organize-type ~/Documents
python skills/file-organizer/main.py find-duplicates ~/Pictures
```

### PDF Toolkit
```bash
python skills/pdf-toolkit/main.py merge output.pdf doc1.pdf doc2.pdf
python skills/pdf-toolkit/main.py split document.pdf ./pages/
python skills/pdf-toolkit/main.py info contract.pdf
```

### Text Formatter
```bash
python skills/text-formatter/main.py case upper "hello world"
python skills/text-formatter/main.py clean document.txt
python skills/text-formatter/main.py count article.txt
```

## Free Forever

These skills are free and open source. No subscription required.

## Pro Skills Coming Soon

Advanced business apps with subscription:
- Lead Capture System
- Simple CRM
- Email Campaign Manager
- Social Media Scheduler
- And more...

## License

MIT License - See LICENSE file
