# Text Formatter — How-To Guide

**Prerequisites:** Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Convert Text Case](#1-how-to-convert-text-case)
2. [How to Convert a Variable Name to a Different Style](#2-how-to-convert-a-variable-name-to-a-different-style)
3. [How to Clean Up Messy Whitespace](#3-how-to-clean-up-messy-whitespace)
4. [How to Count Words in a Document](#4-how-to-count-words-in-a-document)
5. [How to Process Files with Pipes](#5-how-to-process-files-with-pipes)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Convert Text Case

**What this does:** Changes the capitalization of text using one of seven styles.

**When to use it:** You copied text that's in the wrong case, or you need to format a title, heading, or label.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/text-formatter
```

**Step 2 — Choose your case type.**

Available types: `upper`, `lower`, `title`, `sentence`, `camel`, `snake`, `kebab`

**Step 3 — Run the case command with your text.**

```bash
python3 main.py case title "the quick brown fox jumps over the lazy dog"
```

Output:
```
The Quick Brown Fox Jumps Over The Lazy Dog
```

**Step 4 — Use the output.**  
The converted text is printed to stdout. Copy it or pipe it to a file:

```bash
python3 main.py case title "the quick brown fox" > ~/title.txt
```

**Result:** The text is in Title Case, ready to use as a heading, email subject, or document title.

---

### All case types in action

```bash
python3 main.py case upper "hello world"
# Output: HELLO WORLD

python3 main.py case lower "HELLO WORLD"
# Output: hello world

python3 main.py case title "hello world"
# Output: Hello World

python3 main.py case sentence "hello world. this is great."
# Output: Hello world. This is great.

python3 main.py case camel "hello world"
# Output: helloWorld

python3 main.py case snake "hello world"
# Output: hello_world

python3 main.py case kebab "hello world"
# Output: hello-world
```

---

## 2. How to Convert a Variable Name to a Different Style

**What this does:** Translates a programming identifier from one convention to another — useful when porting code between languages or APIs.

**When to use it:** You have a Python function named `get_user_profile` and need the equivalent JavaScript name `getUserProfile`.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/text-formatter
```

**Step 2 — Convert snake_case to camelCase.**

```bash
python3 main.py case camel "get_user_profile_data"
```

Output:
```
getUserProfileData
```

**Step 3 — Convert a camelCase name to a URL slug (kebab-case).**

```bash
python3 main.py case kebab "getUserProfileData"
```

Output:
```
get-user-profile-data
```

**Step 4 — Convert to SCREAMING_SNAKE_CASE (constants).**  
First convert to snake, then to upper:

```bash
python3 main.py case snake "maxRetryCount" | python3 main.py case upper
```

Output:
```
MAX_RETRY_COUNT
```

**Result:** You've translated variable naming styles in seconds without any manual typing.

---

## 3. How to Clean Up Messy Whitespace

**What this does:** Removes extra spaces, collapses blank lines, and strips trailing whitespace.

**When to use it:** You copied text from a PDF, web page, or email that came in with inconsistent spacing or random blank lines.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/text-formatter
```

**Step 2 — Use normal clean for documents (preserves structure).**

```bash
python3 main.py clean ~/Documents/draft.txt
```

Before (in the file):
```
Hello    world.   


This   is   a    paragraph.


And   this     is    another.
```

After:
```
Hello    world.

This   is   a    paragraph.

And   this     is    another.
```

Note: Normal clean strips trailing spaces per line and collapses multiple blank lines into one, but does NOT collapse multiple spaces within a line.

**Step 3 — Use --aggressive for a flat, single-line result.**

```bash
python3 main.py clean --aggressive ~/Documents/draft.txt
```

Output:
```
Hello world. This is a paragraph. And this is another.
```

Aggressive mode collapses ALL whitespace (spaces, tabs, newlines) into single spaces. Use this when you need one continuous string.

**Step 4 — Clean clipboard text (macOS) and put it back.**

```bash
pbpaste | python3 main.py clean | pbcopy
```

Your clipboard now contains the cleaned text, ready to paste.

**Result:** Messy pasted text becomes clean and usable.

---

## 4. How to Count Words in a Document

**What this does:** Analyzes a text file or input and returns word count, character count, line count, sentence count, and estimated reading time.

**When to use it:** You're writing a blog post, article, or assignment with a required word count. Or you want to estimate how long a piece will take to read.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/text-formatter
```

**Step 2 — Run count on your document.**

```bash
python3 main.py count ~/Documents/blog-post.txt
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

**Step 3 — Interpret the output.**

- **Words:** Total word count (spaces as separators)
- **Characters:** Every character including spaces
- **Characters (no spaces):** Useful for character-limited contexts (Twitter, SMS)
- **Lines:** Total number of lines in the file
- **Sentences:** Count of `.`, `!`, `?` occurrences
- **Reading time:** Estimated at 200 words per minute (average adult reading speed)

**Step 4 — Count multiple files together.**

```bash
cat ~/Documents/chapter*.txt | python3 main.py count
```

Output:
```
Words: 12,483
Characters: 73,914
Characters (no spaces): 61,847
Lines: 482
Sentences: 624
Reading time: 62 min 24 sec
```

**Result:** You have an accurate word count and estimated reading time for your content.

---

## 5. How to Process Files with Pipes

**What this does:** Chains text-formatter with other terminal commands to build text processing pipelines.

**When to use it:** You want to combine multiple transformations or integrate with other tools.

### Steps

**Step 1 — Pipe a command's output into text-formatter.**

```bash
# Count words in all text files in a directory
cat ~/Documents/*.txt | python3 ~/smfworks-skills/skills/text-formatter/main.py count
```

**Step 2 — Chain two text-formatter commands.**

First clean the text, then convert to title case:

```bash
cat messy-draft.txt | python3 main.py clean | python3 main.py case title
```

**Step 3 — Save the output to a file.**

```bash
python3 main.py case upper "hello world" > output.txt
cat output.txt
```

Output:
```
HELLO WORLD
```

**Step 4 — Use with echo for quick conversions.**

```bash
echo "get_user_by_email" | python3 main.py case camel
```

Output:
```
getUserByEmail
```

**Result:** Text Formatter integrates cleanly into any shell pipeline, making it a versatile building block.

---

## 6. Automating with Cron

You can schedule Text Formatter to run automatically — for example, generating a weekly word count report from a folder of notes.

### Open the cron editor

```bash
crontab -e
```

### Cron Expression Reference

| Expression | Meaning |
|------------|---------|
| `0 9 * * 1` | Every Monday at 9 AM |
| `0 8 * * *` | Every day at 8 AM |
| `0 22 * * 5` | Every Friday at 10 PM |

### Example: Generate a weekly word count of all notes

```bash
0 9 * * 1 cat /home/yourname/Notes/*.txt | python3 /home/yourname/smfworks-skills/skills/text-formatter/main.py count >> /home/yourname/logs/word-count.log 2>&1
```

### Example: Auto-clean a daily export file

If another process generates a `daily-export.txt` with messy whitespace, clean it each morning:

```bash
0 7 * * * python3 /home/yourname/smfworks-skills/skills/text-formatter/main.py clean /home/yourname/exports/daily-export.txt > /home/yourname/exports/daily-clean.txt
```

### Create the log directory first

```bash
mkdir -p ~/logs
```

---

## 7. Combining with Other Skills

**Text Formatter + Markdown Converter:** Clean up text first, then convert to Markdown:

```bash
python3 ~/smfworks-skills/skills/text-formatter/main.py clean ~/raw-notes.txt | python3 ~/smfworks-skills/skills/markdown-converter/main.py convert
```

**Text Formatter + Report Generator:** Convert all report headings to title case before generating:

```bash
python3 main.py case title "my report heading" > /tmp/heading.txt
# Then pass to report generator
```

---

## 8. Troubleshooting Common Issues

### `Error: case_type must be one of: upper, lower, title, sentence, camel, snake, kebab`

You misspelled the case type.  
**Fix:** Valid values are exactly: `upper`, `lower`, `title`, `sentence`, `camel`, `snake`, `kebab` — all lowercase.

---

### `Error: input too large: X bytes (max: 10485760)`

Your input exceeds 10 MB.  
**Fix:** Split the file: `split -b 9M large-file.txt chunk_` then process each chunk.

---

### `Error: File is not valid UTF-8 text`

The file isn't plain UTF-8 text (may be Latin-1, Windows-1252, or binary).  
**Fix:** Convert encoding: `iconv -f latin1 -t utf-8 input.txt > input-utf8.txt`

---

### `Error: File is empty`

The file you pointed to has zero bytes.  
**Fix:** Verify with `ls -la your-file.txt`. If it's empty, check where the content should have come from.

---

### The count command shows unexpected sentence numbers

Sentence counting finds `.`, `!`, and `?` characters. Abbreviations like "U.S.A." or file extensions in text like "script.py" will inflate the count.  
**This is expected behavior** — the count is an approximation, not a perfect grammar parser.

---

## 9. Tips & Best Practices

**Use the `kebab` case type for URL slugs.** Blog post titles, product names, and article headers convert cleanly to URL-friendly slugs this way: `"My Amazing Blog Post"` → `my-amazing-blog-post`.

**Pipe instead of saving intermediate files.** `cat input.txt | python3 main.py clean | python3 main.py case title` is faster than saving to a temp file between commands.

**Use `count` before submitting any assignment or article.** It takes two seconds and immediately tells you if you're over or under the required word count.

**For clipboard workflows on macOS:** `pbpaste | python3 main.py case upper | pbcopy` transforms your clipboard text in place.

**`--aggressive` mode is destructive to formatting.** Only use it when you need a flat single-line string. Normal `clean` preserves paragraph structure.

**Double-quote arguments containing spaces.** `python3 main.py case upper "hello world"` works. `python3 main.py case upper hello world` may not — the shell will treat `hello` and `world` as separate arguments.
