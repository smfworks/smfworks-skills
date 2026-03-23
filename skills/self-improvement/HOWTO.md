# Self Improvement — How-To Guide

**Prerequisites:** SMF Works Pro subscription active. Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Log an Error](#1-how-to-log-an-error)
2. [How to Log a Learning or Best Practice](#2-how-to-log-a-learning-or-best-practice)
3. [How to Search Your Knowledge Base](#3-how-to-search-your-knowledge-base)
4. [How to Promote Learnings to Agent Memory](#4-how-to-promote-learnings-to-agent-memory)
5. [How to Review Your Progress with Stats](#5-how-to-review-your-progress-with-stats)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Log an Error

**What this does:** Records an error you encountered with context, severity, and resolution — so you never repeat the same mistake.

**When to use it:** Right after fixing a significant bug, resolving a configuration issue, or recovering from any failure.

### Steps

**Step 1 — Navigate to the skill.**

```bash
cd ~/smfworks-skills/skills/self-improvement
```

**Step 2 — Log the error immediately.**

Log while the details are fresh:

```bash
python3 main.py log-error "API call returned 429 Too Many Requests" \
  --context "Batch processing 500 items in a tight loop" \
  --severity high \
  --resolution "Added 1-second delay between API calls" \
  --prevention "Always implement rate limiting for external API calls" \
  --tags api,rate-limiting,python
```

Output:
```
✅ Error logged: ERR-20240315-A1B2C3
   Severity: high
   Tags: api, rate-limiting, python
```

**Step 3 — Verify it was saved.**

```bash
python3 main.py show ERR-20240315-A1B2C3
```

**Result:** A permanent record of the error, its cause, and how to prevent it in future.

---

## 2. How to Log a Learning or Best Practice

**What this does:** Captures knowledge, techniques, and best practices as you discover them.

### Steps

**Step 1 — Log a learning.**

```bash
python3 main.py log-learning "Use pathlib.Path instead of os.path for file operations" \
  --category best-practice \
  --context "Discovered while refactoring file handling code" \
  --tags python,files,refactoring
```

Output:
```
✅ Learning logged: LRN-20240315-D4E5F6
   Category: best-practice
   Tags: python, files, refactoring
```

**Step 2 — Log an insight.**

For broader architectural or strategic observations:

```bash
python3 main.py log-insight "Separation of concerns reduces test complexity significantly" \
  --category architecture \
  --tags testing,architecture,design
```

**Result:** Your knowledge base grows with each work session.

---

## 3. How to Search Your Knowledge Base

**What this does:** Finds logged items matching a search query in their content or tags.

### Steps

**Step 1 — Search for a topic.**

```bash
python3 main.py search "API"
```

Output:
```
🔍 Search results for "API" (4 items):

ERR-20240315-A1B2 [error] API call returned 429 — api, rate-limiting, python
LRN-20240310-B3C4 [learning] Always set API timeout — api, network
LRN-20240308-C5D6 [learning] Use exponential backoff for API retries — api, resilience
INS-20240305-E7F8 [insight] REST API versioning with /v1, /v2 paths — api, design
```

**Step 2 — View the full details of a result.**

```bash
python3 main.py show ERR-20240315-A1B2
```

**Result:** Quickly find relevant knowledge when you encounter a familiar problem.

---

## 4. How to Promote Learnings to Agent Memory

**What this does:** Copies selected items to `~/.smf/improvement/promoted.md` — a Markdown file your OpenClaw agent can reference for context-aware assistance.

### Steps

**Step 1 — List recent learnings.**

```bash
python3 main.py list --category learnings
```

**Step 2 — Identify the most valuable ones.**

Look for items that:
- Apply broadly across many projects
- Capture hard-won insights
- Would help your agent give better advice

**Step 3 — Promote them.**

```bash
python3 main.py promote LRN-20240315-D4E5F6
```

Output:
```
✅ Promoted to memory: LRN-20240315-D4E5F6
   Written to: ~/.smf/improvement/promoted.md
```

**Step 4 — Review the promoted file.**

```bash
cat ~/.smf/improvement/promoted.md
```

**Result:** Your hard-won learnings are now in a format your agent can access.

---

## 5. How to Review Your Progress with Stats

**When to use it:** Weekly review to understand your error patterns and growth areas.

```bash
python3 main.py stats
```

Output:
```
📊 Self Improvement Statistics

Total items: 47
  Errors: 18  |  Learnings: 21  |  Insights: 8

By severity (errors):
  Critical: 2  |  High: 7  |  Medium: 6  |  Low: 3

Top tags: python (12), database (8), config (7), api (5)
Promoted: 9 items
This week: 8 new items
This month: 23 new items
```

Use the top tags to identify where your most common issues are. If `config` appears frequently, invest time in better configuration management.

---

## 6. Automating with Cron

### Example: Weekly review prompt

```bash
0 9 * * 1 python3 /home/yourname/smfworks-skills/skills/self-improvement/main.py stats >> /home/yourname/logs/self-improvement.log 2>&1
```

---

## 7. Combining with Other Skills

**Self Improvement + Task Manager:** When completing tasks, log what you learned:

```bash
python3 ~/smfworks-skills/skills/task-manager/main.py task move TASK-ABC --to done
python3 ~/smfworks-skills/skills/self-improvement/main.py log-learning "Learned X from completing this task" --tags project
```

**Self Improvement + OpenClaw Backup:** Back up your improvement log regularly:

```bash
python3 ~/smfworks-skills/skills/openclaw-backup/main.py
# Your ~/.smf/improvement/ directory is included in the workspace backup
```

---

## 8. Troubleshooting Common Issues

### `Item not found: LRN-XYZ`

**Fix:** IDs are case-sensitive. Run `python3 main.py list` to find the exact ID.

### `promoted.md is very large and slowing down agent context`

**Fix:** Edit `~/.smf/improvement/promoted.md` directly and remove stale entries. Keep only timeless, broadly applicable learnings.

### Items aren't appearing in search

**Fix:** Search is full-text. Try different keywords. Tags are also searchable: `python3 main.py search "api"`

---

## 9. Tips & Best Practices

**Log errors immediately.** The most valuable time to log an error is right after fixing it — before you forget the context. Make it a habit to run `log-error` as part of your bug-fix workflow.

**Be specific in descriptions.** "File not found error" is less useful than "FileNotFoundError when reading config.json if ENVIRONMENT env var is not set." Specificity makes search results actionable.

**Promote sparingly.** Only promote learnings that are broadly applicable and timeless. `promoted.md` should be curated, not a dump of everything.

**Review your top tags monthly.** If `database` or `authentication` keeps appearing, that's signal to invest in learning that area more deeply.

**Use consistent tags.** `python` and `py` are different tags. Pick one convention and stick to it. Consistent tags make `search` and `stats` far more useful.
