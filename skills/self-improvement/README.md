# Self-Improvement Skill

Log errors, learnings, and insights for continuous improvement. Coding agents can process these into fixes, and important items get promoted to project memory.

## Features

- ✅ **Error Logging** — Capture errors with context, severity, and resolution
- ✅ **Learning Logging** — Document insights, patterns, and best practices
- ✅ **Insight Logging** — General observations and improvements
- ✅ **Searchable Database** — Find past errors and solutions
- ✅ **Promotion to Memory** — Important items become project knowledge
- ✅ **Statistics** — Track improvement over time
- ✅ **Markdown Export** — Human-readable logs for review

## Installation

```bash
# Install SMF CLI (if not already)
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash

# Login (Pro skill requires subscription)
smf login

# Install the skill
smf install self-improvement
```

## Quick Start

### Log an Error

```bash
# Interactive
smf run self-improvement log-error

# Quick log
smf run self-improvement log-error "File not found" \
  --context "Reading config.json during startup" \
  --severity high \
  --tags "file-io,config" \
  --resolution "Added file existence check" \
  --prevention "Always validate file paths before reading"
```

### Log a Learning

```bash
# Interactive
smf run self-improvement log-learning

# Quick log
smf run self-improvement log-learning "Always validate JSON before parsing" \
  --category best-practice \
  --context "Crashed on malformed config" \
  --tags "json,validation"
```

### View and Search

```bash
# List all items
smf run self-improvement list

# List only errors
smf run self-improvement list --type error

# List by category
smf run self-improvement list --category best-practice

# Search
smf run self-improvement search "config"

# Show details
smf run self-improvement show ERR-20260320-ABC123
```

### Promote to Memory

```bash
# Promote important learning to project memory
smf run self-improvement promote LRN-20260320-DEF456 \
  --notes "Critical for all file operations"
```

## Usage

### Error Logging

**When to log:**
- When you fix a bug
- When you encounter a new error type
- When you spend > 30 min debugging something

**Structure:**
```
Description: What went wrong
Context: What were you doing
Severity: low/medium/high/critical
Resolution: How you fixed it
Prevention: How to prevent in future
Tags: Categories for search
```

**Example workflow:**
```bash
# Encounter error
cat config.json | jq
# Error: parse error: Invalid numeric literal

# Log it
smf run self-improvement log-error "JSON parse error" \
  --context "Reading user config" \
  --severity medium \
  --tags "json,config" \
  --resolution "Added try/except around json.loads" \
  --prevention "Validate JSON with linter before deployment"

# Later, find similar errors
smf run self-improvement search "json"
```

### Learning Logging

**When to log:**
- When you discover a better way to do something
- When you identify a pattern
- When you learn from a mistake

**Categories:**
- `best-practice` — Recommended approaches
- `pattern` — Recurring solutions
- `anti-pattern` — Things to avoid
- `optimization` — Performance improvements
- `architecture` — Design decisions

**Example:**
```bash
smf run self-improvement log-learning "Use pathlib instead of os.path" \
  --category best-practice \
  --context "Path operations cleaner with pathlib" \
  --tags "python,file-io"
```

### Searching the Knowledge Base

```bash
# Search all items
smf run self-improvement search "config"

# Search only errors
smf run self-improvement search "database" --type error

# Search only learnings
smf run self-improvement search "optimization" --type learning
```

### Statistics

```bash
smf run self-improvement stats
```

Output:
```
📊 Self-Improvement Statistics
==================================================

📈 Totals:
   Errors: 47 (12 open, 35 resolved)
   Learnings: 23
   Insights: 8

📅 This Week:
   New errors: 3
   New learnings: 5

🔥 Errors by Severity:
   🔴 critical: 2
   🟠 high: 8
   🟡 medium: 25
   🟢 low: 12

💡 Learnings by Category:
   • best-practice: 12
   • pattern: 5
   • optimization: 4
   • architecture: 2
```

## File Structure

```
~/.smf/improvement/
├── errors/
│   ├── ERR-20260320-ABC123.json
│   ├── errors-2026-03-20.md
│   └── ...
├── learnings/
│   ├── LRN-20260320-DEF456.json
│   ├── learnings-2026-03-20.md
│   └── ...
├── insights/
│   ├── INS-20260320-GHI789.json
│   └── ...
└── promoted.md  # Project memory file
```

### JSON Format (for agents)

**Error:**
```json
{
  "id": "ERR-20260320-ABC123",
  "type": "error",
  "description": "File not found",
  "context": "Reading config.json",
  "severity": "high",
  "tags": ["file-io", "config"],
  "resolution": "Added file existence check",
  "prevention": "Always validate paths",
  "status": "resolved",
  "occurrences": 1,
  "created_at": "2026-03-20T14:30:00",
  "updated_at": "2026-03-20T15:00:00",
  "resolved_at": "2026-03-20T15:00:00"
}
```

**Learning:**
```json
{
  "id": "LRN-20260320-DEF456",
  "type": "learning",
  "insight": "Use pathlib instead of os.path",
  "category": "best-practice",
  "context": "Path operations",
  "tags": ["python", "file-io"],
  "related_errors": ["ERR-20260320-ABC123"],
  "promoted": true,
  "created_at": "2026-03-20T14:30:00"
}
```

### Markdown Format (for humans)

**Daily error log:**
```markdown
## ERR-20260320-ABC123

**Error:** File not found

**Context:** Reading config.json during startup

**Severity:** high

**Tags:** file-io, config

**Timestamp:** 2026-03-20T14:30:00

---
```

## Promotion to Memory

**When to promote:**
- Error pattern affects multiple areas
- Learning is fundamental to project
- Insight changes how team works

**Memory file format:**
```markdown
## ERR-20260320-ABC123 - Error Pattern

**Error:** File not found

**Context:** Reading config.json

**Resolution:** Added file existence check

**Prevention:** Always validate file paths before reading

**Tags:** file-io, config

**Promoted:** 2026-03-20T16:00:00
**Notes:** Critical for all file operations

---
```

## Integration with Coding Agents

### For Agent Prompts

```
Before coding, search for relevant errors:
smf run self-improvement search "database"
smf run self-improvement search "api"

After fixing an error, log it:
smf run self-improvement log-error "..."

After learning something, log it:
smf run self-improvement log-learning "..."
```

### Processing with Scripts

```bash
# Find all unresolved critical errors
smf run self-improvement list --type error --status open | grep critical

# Find learnings related to specific error
smf run self-improvement list --type learning | grep "ERR-20260320-ABC123"

# Generate report
smf run self-improvement stats > improvement-report.txt
```

## Workflows

### Daily Workflow

```bash
# Morning - check for patterns
smf run self-improvement stats

# During work - log errors as they happen
smf run self-improvement log-error "..."

# End of day - log learnings
smf run self-improvement log-learning "..."
```

### Weekly Review

```bash
# Review new items
smf run self-improvement list --type error | head -10
smf run self-improvement list --type learning | head -10

# Promote important items
smf run self-improvement promote ERR-...
smf run self-improvement promote LRN-...

# Check promoted memory
cat ~/.smf/improvement/promoted.md
```

### Sprint Retrospective

```bash
# Error analysis
smf run self-improvement stats

# Pattern identification
smf run self-improvement list --category anti-pattern

# Best practice adoption
smf run self-improvement list --category best-practice
```

## Best Practices

### Error Logging

1. **Log immediately** — While context is fresh
2. **Be specific** — "File not found" vs "Error"
3. **Include context** — What were you doing?
4. **Document resolution** — How did you fix it?
5. **Add prevention** — How to avoid in future?

### Learning Logging

1. **Log insights** — Don't let them fade
2. **Connect to errors** — Link learnings to causes
3. **Categorize** — Helps with retrieval
4. **Be actionable** — Clear what to do differently

### Search

1. **Use tags** — Consistent taxonomy
2. **Check before coding** — Avoid repeat errors
3. **Review weekly** — Stay aware of patterns

### Promotion

1. **Be selective** — Only promote important items
2. **Add context** — Notes about why it matters
3. **Review memory** — Monthly cleanup

## Tags Taxonomy

### Error Tags

- `file-io` — File operations
- `network` — Network requests
- `config` — Configuration issues
- `logic` — Business logic errors
- `syntax` — Syntax mistakes
- `runtime` — Runtime exceptions
- `database` — Database issues
- `api` — API/integration errors

### Learning Tags

- `python` — Python-specific
- `javascript` — JS-specific
- `architecture` — System design
- `testing` — Test strategies
- `performance` — Optimization
- `security` — Security practices
- `devops` — Deployment/infrastructure

## Pricing

**Self-Improvement Skill is a premium SMF Works skill.**

This is a paid skill that is part of the SMF Works subscription service. One monthly fee for unlimited access to the growing library of premium SMF Skills and applications.

- **Price:** $19.99/month (locked forever at signup rate)
- **Includes:** All premium skills, updates, priority support
- **Free alternative:** Manual notes in text files

Subscribe at https://smf.works/subscribe

## See Also

- [SETUP.md](./SETUP.md) — Complete setup guide
- `smf help` — CLI documentation
- `smf status` — Check subscription

## License

SMF Works Pro Skill — See SMF Works Terms of Service
