# Self Improvement

> Log errors, learnings, and insights from your work — then search, review, and promote the most valuable lessons to your agent's long-term memory.

**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo at [smfworks.com/subscribe](https://smfworks.com/subscribe))  
**Version:** 1.0  
**Category:** Productivity / Knowledge Management

---

## What It Does

Self Improvement is an OpenClaw Pro skill for building a personal knowledge base from your work. Log errors you made and how you resolved them, document learnings and best practices, record insights. Search your log, view statistics, and promote the most valuable items to your agent's `promoted.md` memory file for long-term retention.

This is particularly powerful combined with OpenClaw — your logged learnings can become part of your agent's memory.

**What it does NOT do:** It does not automatically analyze your work, integrate with IDEs or error monitoring tools, or sync to external knowledge bases.

---

## Prerequisites

- [ ] **SMF Works Pro subscription** — [smfworks.com/subscribe](https://smfworks.com/subscribe)
- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed and authenticated**

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/self-improvement
python3 main.py help
```

---

## Quick Start

Log a learning from today's work:

```bash
python3 main.py log-learning "Always validate JSON config files before loading" --tags config,python
```

Output:
```
✅ Learning logged: LRN-20240315-A1B2C3
   Category: best-practice
   Tags: config, python
```

---

## Command Reference

### `log-error "description"`

Logs an error you encountered, with optional context, severity, and resolution.

```bash
python3 main.py log-error "File not found" --context "Reading config file" --severity high --resolution "Added file existence check" --tags config,file-io
```

Output:
```
✅ Error logged: ERR-20240315-A1B2C3
   Context: Reading config file
   Severity: high
   Resolution: Added file existence check
```

**Severity levels:** `low`, `medium`, `high`, `critical`

---

### `log-learning "insight"`

Logs a learning, best practice, or technique you discovered.

```bash
python3 main.py log-learning "Use pathlib instead of os.path for file operations in Python 3" --category best-practice --tags python,files
```

---

### `log-insight "title"`

Logs a broader insight or architectural observation.

```bash
python3 main.py log-insight "Database indexes should always be created before bulk inserts" --category optimization --tags database,performance
```

---

### `list`

Lists all logged items, optionally filtered by category.

```bash
python3 main.py list
python3 main.py list --category errors
python3 main.py list --category learnings
```

Output:
```
📋 Self Improvement Log (24 items)

ERR-20240315-A1B2 [high] File not found — config, file-io
ERR-20240314-B3C4 [medium] Import error — python, dependencies
LRN-20240315-C5D6 [best-practice] Use pathlib — python, files
LRN-20240313-E7F8 [pattern] Early return reduces nesting — python, style
```

---

### `search "query"`

Searches all logged items by content.

```bash
python3 main.py search "config"
python3 main.py search "database"
```

---

### `show ITEM-ID`

Shows full details for a logged item.

```bash
python3 main.py show ERR-20240315-A1B2C3
```

Output:
```
📋 Error: ERR-20240315-A1B2C3

Description: File not found when reading config
Context: Reading config file at startup
Severity: high
Resolution: Added file existence check before open()
Prevention: Validate config path in __init__
Tags: config, file-io
Logged: 2024-03-15 09:42
```

---

### `promote ITEM-ID`

Promotes a high-value item to `~/.smf/improvement/promoted.md` — your persistent learning file that can be loaded by your agent.

```bash
python3 main.py promote LRN-20240315-C5D6
```

Output:
```
✅ Promoted to memory: LRN-20240315-C5D6
   Written to: ~/.smf/improvement/promoted.md
```

---

### `stats`

Shows statistics on your improvement log.

```bash
python3 main.py stats
```

Output:
```
📊 Self Improvement Statistics

Total items: 47
  Errors: 18
  Learnings: 21
  Insights: 8

By severity (errors):
  Critical: 2
  High: 7
  Medium: 6
  Low: 3

Top tags: python (12), database (8), config (7), api (5)
Promoted: 9 items
```

---

## Use Cases

### 1. Daily error journal

Log every significant error you hit during a work session with context and resolution.

### 2. Best practices capture

When you discover a better way to do something, log it immediately: `log-learning`

### 3. Build agent memory from experience

Promote your best learnings to `promoted.md`, then reference this file from your OpenClaw agent for context-aware assistance.

### 4. Weekly review

Run `stats` and `list` to review your week's errors and learnings — identify patterns and areas for growth.

---

## Storage Structure

```
~/.smf/improvement/
├── errors/        — Logged errors (one JSON per item)
├── learnings/     — Logged learnings
├── insights/      — Logged insights
└── promoted.md    — Promoted items in Markdown format
```

---

## Troubleshooting

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

### `Item not found: ERR-XYZ`
**Fix:** IDs are case-sensitive. Use `python3 main.py list` to find the exact ID.

### `promoted.md is getting very large`
**Fix:** Review and curate `promoted.md` periodically. Remove items that are no longer relevant.

---

## FAQ

**Q: What's the difference between `log-error`, `log-learning`, and `log-insight`?**  
A: Errors are mistakes or failures you encountered. Learnings are new knowledge or techniques you acquired. Insights are broader observations about systems, architecture, or strategy.

**Q: What does "promote" do?**  
A: Promoted items are written to `~/.smf/improvement/promoted.md` in Markdown format. This file can be loaded by your OpenClaw agent as part of its context, making your learnings available to AI assistance.

**Q: Are there limits on how much I can log?**  
A: Yes — there are configurable maximum counts per category to prevent excessive storage use. Check the source code for the current limits.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| SMF Works Pro | Required ($19.99/mo) |
| External APIs | None |
| Internet | For subscription check only |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/self-improvement)
- 🔑 [Subscribe](https://smfworks.com/subscribe)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
