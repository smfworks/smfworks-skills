# Text Formatter

> Convert text case, clean up messy whitespace, and count words — all from the terminal in seconds.

**Tier:** Free — no subscription required  
**Version:** 1.0  
**Category:** Productivity / Text Processing

---

## What It Does

Text Formatter is an OpenClaw skill for quick text transformations. Pass text directly as an argument or pipe a file's contents in, and the skill converts case (UPPER, lower, Title Case, camelCase, snake_case, kebab-case, Sentence case), strips excessive whitespace, or produces a full word/character/reading-time count.

It accepts input from three sources: a literal string on the command line, a file path, or standard input via a pipe. This makes it easy to chain with other tools.

**What it does NOT do:** It does not translate between languages, spell-check, grammar-check, replace words, or perform find-and-replace operations. Files larger than 10 MB are rejected.

---

## Prerequisites

- [ ] **Python 3.8 or newer** — run `python3 --version` to check
- [ ] **OpenClaw installed** — run `openclaw --version` to check
- [ ] **No subscription required** — free tier skill
- [ ] **No external Python packages** — stdlib only

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/text-formatter
python3 main.py
```

Expected output:
```
Usage: python main.py <command> [options]
Commands: case, clean, count

Examples:
  python main.py case upper "hello world"
  python main.py case camel "hello world"
  python main.py clean < input.txt
  python main.py clean --aggressive < messy.txt
  python main.py count < document.txt
```

---

## Quick Start

Convert text to UPPER case:

```bash
python3 main.py case upper "hello world"
```

Output:
```
HELLO WORLD
```

Count words in a file:

```bash
python3 main.py count < ~/Documents/essay.txt
```

Output:
```
Words: 1,842
Characters: 10,847
Characters (no spaces): 9,121
Lines: 74
Sentences: 92
Reading time: 9 min 12 sec
```

---

## Command Reference

### `case`

Converts the case of input text. Accepts text as a literal argument, a file path, or via stdin pipe.

**Usage:**
```bash
python3 main.py case <case_type> [text_or_file]
# or via pipe:
echo "hello world" | python3 main.py case <case_type>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `case_type` | ✅ Yes | One of: `upper`, `lower`, `title`, `sentence`, `camel`, `snake`, `kebab` | `camel` |
| `text_or_file` | ❌ No | Text string or path to a .txt file. If omitted, reads from stdin. | `"hello world"` |

**Case type reference:**

| Case Type | Input | Output |
|-----------|-------|--------|
| `upper` | `hello world` | `HELLO WORLD` |
| `lower` | `HELLO WORLD` | `hello world` |
| `title` | `hello world` | `Hello World` |
| `sentence` | `hello world. yes please.` | `Hello world. Yes please.` |
| `camel` | `hello world` | `helloWorld` |
| `snake` | `hello world` | `hello_world` |
| `kebab` | `hello world` | `hello-world` |

**Examples:**

```bash
python3 main.py case upper "make this loud"
```
```
MAKE THIS LOUD
```

```bash
python3 main.py case snake "My Variable Name"
```
```
my_variable_name
```

```bash
python3 main.py case camel "get user profile"
```
```
getUserProfile
```

```bash
cat ~/Documents/draft.txt | python3 main.py case title
```
```
The Quick Brown Fox Jumps Over The Lazy Dog
```

---

### `clean`

Removes extra whitespace from text. Without `--aggressive`, it strips trailing spaces from each line and collapses consecutive blank lines into one. With `--aggressive`, it collapses ALL whitespace (including tabs and multiple spaces) into single spaces.

**Usage:**
```bash
python3 main.py clean [--aggressive] [text_or_file]
# or:
cat messy.txt | python3 main.py clean
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `--aggressive` | ❌ No | Collapses ALL whitespace to single spaces — produces one long line |
| `text_or_file` | ❌ No | Text or file path. If omitted, reads from stdin. |

**Example — normal clean:**
```bash
echo "  hello   world  
  
  this   is   text  " | python3 main.py clean
```
```
hello   world

this   is   text
```

**Example — aggressive clean:**
```bash
echo "  hello   world  
  
  this   is   text  " | python3 main.py clean --aggressive
```
```
hello world this is text
```

---

### `count`

Counts words, characters, lines, and sentences. Also calculates estimated reading time at 200 words per minute.

**Usage:**
```bash
python3 main.py count [text_or_file]
# or:
cat document.txt | python3 main.py count
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `text_or_file` | ❌ No | Text or file path. If omitted, reads from stdin. |

**Example:**
```bash
python3 main.py count ~/Documents/article.txt
```

**Output:**
```
Words: 3,218
Characters: 18,934
Characters (no spaces): 15,826
Lines: 128
Sentences: 161
Reading time: 16 min 5 sec
```

---

## Use Cases

### 1. Convert variable names between coding styles

Going from Python (snake_case) to JavaScript (camelCase):

```bash
python3 main.py case camel "get_user_profile_data"
```
```
getUserProfileData
```

---

### 2. Normalize a messy copied document

When you paste text from a PDF or web page and get extra spaces everywhere:

```bash
pbpaste | python3 main.py clean --aggressive > ~/cleaned.txt
```

---

### 3. Count words before submitting

Check your article hits the minimum word count:

```bash
python3 main.py count ~/Documents/submission.txt
```

---

### 4. Convert a title to URL-friendly slug

```bash
python3 main.py case kebab "How to Build a Great Product"
```
```
how-to-build-a-great-product
```

---

### 5. Batch process with pipes

Combine with other tools:
```bash
cat ~/Notes/*.txt | python3 main.py count
cat input.txt | python3 main.py clean | python3 main.py case title
```

---

## Configuration

No configuration file or environment variables required. All behavior is controlled by command and arguments.

**Built-in limits:**

| Setting | Value |
|---------|-------|
| Max input size | 10 MB |
| Max output size | 50 MB |
| Max word count | 10,000,000 words |

---

## Troubleshooting

### `Error: case requires case_type`
**Fix:** Provide a case type: `python3 main.py case upper "text"`

### `Error: case_type must be one of: upper, lower, title, sentence, camel, snake, kebab`
**Fix:** Check spelling. Valid types are exactly: `upper`, `lower`, `title`, `sentence`, `camel`, `snake`, `kebab`

### `Error: input too large: X bytes (max: 10485760)`
**Fix:** The input file or text exceeds 10 MB. Split the file first.

### `Error: File is not valid UTF-8 text: /path/to/file`
**Fix:** The file contains binary data or is encoded in a format other than UTF-8 (e.g., Latin-1). Convert it with: `iconv -f latin1 -t utf-8 input.txt > output.txt`

### `Error: File is empty: /path/to/file`
**Fix:** The file exists but has no content. Check that you're pointing at the right file.

### `Error: Path traversal detected`
**Fix:** Don't use `..` in paths. Use absolute paths or paths relative to your home directory.

### `Error: Too many words: X (max: 10000000)`
**Fix:** The document has more than 10 million words. Split the file into smaller chunks.

---

## FAQ

**Q: Can I process multiple files at once?**  
A: Not directly with a single command. Use a shell loop:
```bash
for f in ~/Documents/*.txt; do python3 main.py count "$f"; done
```

**Q: What's the difference between `title` and `sentence` case?**  
A: `title` capitalizes every word. `sentence` capitalizes only the first word of each sentence (after `.`, `!`, `?`).

**Q: Can I pipe the output to a file?**  
A: Yes: `python3 main.py case upper "text" > output.txt`

**Q: Does `camel` work with multi-word phrases?**  
A: Yes. `"hello world goodbye"` becomes `helloWorldGoodbye`. Non-alphanumeric characters are treated as word separators.

**Q: Does it preserve accented characters?**  
A: The `upper` and `lower` commands use Python's built-in case conversion which handles most Unicode characters correctly. `camel`, `snake`, and `kebab` strip non-alphanumeric characters.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| OpenClaw | Any version |
| Operating System | Linux, macOS |
| Subscription Tier | Free |
| External APIs | None |
| External Packages | None (stdlib only) |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/text-formatter)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
