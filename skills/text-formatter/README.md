# Text Formatter

> Format, clean, and transform text — convert case, clean whitespace, count words

---

## What It Does

Text Formatter handles all your text transformation needs. Convert between cases (upper, lower, title, camel, snake, kebab), clean up messy whitespace, and count words and characters. Works on files or piped input.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install text-formatter
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Convert text to uppercase:

```bash
python main.py case upper "hello world"
```

---

## Commands

### `case`

**What it does:** Convert text between different case formats.

**Usage:**
```bash
python main.py case [case-type] [text-or-file]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `case-type` | ✅ Yes | Type of conversion | `upper`, `lower`, `title`, `sentence`, `camel`, `snake`, `kebab` |
| `text-or-file` | ❌ No | Text to convert or file path | `hello world` or `input.txt` |

**Case Types:**

| Type | Example Input | Example Output |
|------|---------------|----------------|
| `upper` | hello | HELLO |
| `lower` | HELLO | hello |
| `title` | hello world | Hello World |
| `sentence` | hello. world | Hello. world |
| `camel` | hello world | helloWorld |
| `snake` | hello world | hello_world |
| `kebab` | hello world | hello-world |

**Example:**
```bash
python main.py case upper "hello world"
python main.py case camel "hello world"
python main.py case snake "HelloWorld"
```

---

### `clean`

**What it does:** Clean up whitespace in text.

**Usage:**
```bash
python main.py clean [file]
```

**Options:**

| Option | Required | Description |
|--------|----------|-------------|
| `--aggressive` | ❌ No | Collapse all whitespace to single spaces |

**Example:**
```bash
python main.py clean messy.txt
python main.py clean --aggressive < input.txt
```

---

### `count`

**What it does:** Count words, characters, lines, and sentences.

**Usage:**
```bash
python main.py count [file]
```

**Example:**
```bash
python main.py count document.txt
```

**Output:**
```
Words: 1,234
Characters: 6,789
Characters (no spaces): 5,432
Lines: 89
Sentences: 45
Reading time: 6 min 10 sec
```

---

## Use Cases

- **Code formatting:** Convert variable names between camelCase and snake_case
- **Data cleaning:** Clean up messy text with extra whitespace
- **Word count:** Check document length before submission
- **Text preparation:** Normalize text before processing

---

## Tips & Tricks

- Pipe text directly: `echo "HELLO" | python main.py case lower`
- Works with file paths or raw text
- Use `--aggressive` for maximum whitespace cleanup
- Reading time estimate assumes 200 words/minute

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Too many words" | Text exceeds 10 million word limit |
| Empty output | Ensure input has content |
| Wrong case | Check case type spelling |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- No external dependencies

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/text-formatter)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
