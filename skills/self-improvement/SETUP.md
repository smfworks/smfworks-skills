# Self-Improvement Skill - Setup & Configuration Guide

Complete setup instructions for installing, configuring, and using the Self-Improvement skill for continuous learning.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Authentication Setup](#authentication-setup)
4. [Quick Start](#quick-start)
5. [Logging Workflows](#logging-workflows)
6. [Integration with Coding Agents](#integration-with-coding-agents)
7. [Memory Management](#memory-management)
8. [Automation](#automation)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## Prerequisites

### System Requirements
- **OS:** Linux, macOS, or Windows with Python
- **Python:** 3.8 or higher
- **Storage:** Minimal (~10KB per item)

### SMF Works Subscription
- **Required:** SMF Works Pro subscription ($19.99/mo)
- **Sign up:** https://smf.works/subscribe

---

## Installation

### Step 1: Install SMF CLI

```bash
# One-liner install
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash

# Reload PATH
source ~/.bashrc  # or ~/.zshrc
```

### Step 2: Authenticate

```bash
# Login with your subscription
smf login

# Verify
smf status
```

### Step 3: Install Self-Improvement Skill

```bash
smf install self-improvement
```

### Step 4: Verify Installation

```bash
smf run self-improvement --help
```

---

## Quick Start

### Your First Error Log

```bash
# Interactive mode
smf run self-improvement log-error

# Follow prompts:
# Error description: File not found
# Context: Reading config during startup
# Severity: high
# Tags: file-io, config
# Resolution: Added existence check
# Prevention: Always validate paths
```

### Your First Learning Log

```bash
# Interactive mode
smf run self-improvement log-learning

# Follow prompts:
# What did you learn: Always validate JSON before parsing
# Category: best-practice
# Context: Prevents crashes on malformed input
# Tags: json, validation
```

### View Your Logs

```bash
# List all items
smf run self-improvement list

# List errors only
smf run self-improvement list --type error

# List learnings
smf run self-improvement list --type learning

# Show statistics
smf run self-improvement stats
```

---

## Logging Workflows

### Error Logging Workflow

**Step 1: Encounter Error**
```bash
# Something goes wrong...
python3 myapp.py
# Error: FileNotFoundError: config.json not found
```

**Step 2: Log Immediately**
```bash
smf run self-improvement log-error \
  "FileNotFoundError: config.json" \
  --context "Starting application, config missing" \
  --severity high \
  --tags "file-io,config"
```

**Step 3: Fix the Error**
```bash
# Add file check to code...
vim myapp.py
# Add: if not os.path.exists('config.json'): create_default()
```

**Step 4: Update with Resolution**
```bash
smf run self-improvement update ERR-20260320-ABC123 \
  --status resolved \
  --resolution "Added file existence check with default creation" \
  --prevention "Always check file exists before reading, use try/except"
```

**Step 5: Log the Learning**
```bash
smf run self-improvement log-learning \
  "Always validate file existence before reading" \
  --category best-practice \
  --context "Prevents FileNotFoundError crashes" \
  --tags "file-io,python"
```

### Daily Logging Routine

**Morning:**
```bash
# Check yesterday's stats
smf run self-improvement stats
```

**During Coding:**
```bash
# When you hit an error
smf run self-improvement log-error "..."

# When you figure something out
smf run self-improvement log-learning "..."
```

**Evening:**
```bash
# Review and promote important items
smf run self-improvement list --type learning
smf run self-improvement promote LRN-...
```

---

## Integration with Coding Agents

### Agent System Prompt

Add to your coding agent's system prompt:

```
## Self-Improvement Integration

Before starting work:
1. Search for relevant errors:
   smf run self-improvement search "database"
   smf run self-improvement search "api"

2. Check promoted memory:
   cat ~/.smf/improvement/promoted.md

After completing work:
1. Log any errors encountered:
   smf run self-improvement log-error "..."

2. Log any learnings:
   smf run self-improvement log-learning "..."
```

### Pre-Flight Check Script

Create `~/preflight.sh`:
```bash
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"

echo "🔍 Checking for relevant past errors..."

# Search for errors related to common areas
smf run self-improvement search "file" --type error
smf run self-improvement search "config" --type error
smf run self-improvement search "database" --type error

echo ""
echo "💡 Relevant learnings:"
smf run self-improvement search "best-practice" --type learning | head -5

echo ""
echo "📚 Project memory:"
head -50 ~/.smf/improvement/promoted.md
```

Make executable:
```bash
chmod +x ~/preflight.sh
```

### Post-Work Logging Script

Create `~/postflight.sh`:
```bash
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"

# Ask what was learned
echo "What did you learn from this session?"
read learning

if [ -n "$learning" ]; then
    smf run self-improvement log-learning "$learning"
fi

# Ask about errors
echo "Any errors encountered? (y/n)"
read had_errors

if [ "$had_errors" = "y" ]; then
    smf run self-improvement log-error
fi

echo "✅ Session logged"
```

### Processing for Fixes

**Agent can query:**
```bash
# Find open critical errors
smf run self-improvement list --type error --status open | grep critical

# Find patterns
smf run self-improvement list --category anti-pattern

# Find common tags
smf run self-improvement stats
```

### Automated Memory Building

**Weekly memory review:**
```bash
#!/bin/bash
# weekly-memory-review.sh

export PATH="$HOME/.local/bin:$PATH"

# Get high-value learnings
smf run self-improvement list --type learning | grep -E "(critical|high)" | head -5

# Promote important ones
for item in $(smf run self-improvement list --type learning | grep "important" | awk '{print $1}'); do
    smf run self-improvement promote $item --notes "From weekly review"
done
```

---

## Memory Management

### Understanding the Memory File

**Location:** `~/.smf/improvement/promoted.md`

**Structure:**
```markdown
## ERR-20260320-ABC123 - Error Pattern

**Error:** File not found

**Context:** Reading config

**Resolution:** Added existence check

**Prevention:** Always validate paths

**Tags:** file-io, config

**Promoted:** 2026-03-20T16:00:00
**Notes:** Critical for all file operations

---

## LRN-20260320-DEF456 - Learning

**Insight:** Use pathlib instead of os.path

**Category:** best-practice

**Context:** Path operations

**Tags:** python, file-io

**Promoted:** 2026-03-20T17:00:00

---
```

### When to Promote

**Promote when:**
- ✅ Error affects multiple areas of codebase
- ✅ Learning is fundamental to project architecture
- ✅ Pattern occurs repeatedly
- ✅ Knowledge saves > 30 min of debugging

**Don't promote:**
- ❌ One-off errors with simple fixes
- ❌ Project-specific quirks
- ❌ Already well-documented elsewhere
- ❌ Personal preferences

### Memory Maintenance

**Monthly review:**
```bash
# View memory
cat ~/.smf/improvement/promoted.md

# Check for duplicates
smf run self-improvement search "pattern" --type learning

# Archive outdated items
# (Edit promoted.md directly)
```

**Clean up:**
```bash
# Find duplicate patterns
smf run self-improvement list --type learning | sort | uniq -d

# Consolidate similar learnings
# (Manual edit of promoted.md)
```

---

## Automation

### Daily Logging Reminder

**Cron:**
```bash
# Remind to log daily learnings
0 18 * * * echo "🧠 Time to log today's learnings! Run: smf run self-improvement log-learning"
```

### Weekly Statistics Email

**Script:**
```bash
#!/bin/bash
# weekly-improvement-report.sh

export PATH="$HOME/.local/bin:$PATH"

# Generate stats
smf run self-improvement stats > /tmp/stats.txt

# Email it
mail -s "Weekly Improvement Report" you@example.com < /tmp/stats.txt
```

**Cron:**
```bash
# Every Friday at 5 PM
0 17 * * 5 ~/weekly-improvement-report.sh
```

### Error Alert

**Script:**
```bash
#!/bin/bash
# check-critical-errors.sh

export PATH="$HOME/.local/bin:$PATH"

# Count critical errors
CRITICAL_COUNT=$(smf run self-improvement list --type error | grep -c critical)

if [ "$CRITICAL_COUNT" -gt 0 ]; then
    echo "⚠️  $CRITICAL_COUNT critical errors need attention!"
    smf run self-improvement list --type error | grep critical
fi
```

### Backup Logs

**Script:**
```bash
#!/bin/bash
# backup-improvement-logs.sh

DATE=$(date +%Y%m%d)
BACKUP_DIR="$HOME/backups/improvement"

mkdir -p "$BACKUP_DIR"

# Backup all logs
tar -czf "$BACKUP_DIR/improvement-$DATE.tar.gz" ~/.smf/improvement/

# Keep only last 30 days
find "$BACKUP_DIR" -name "improvement-*.tar.gz" -mtime +30 -delete

echo "✅ Logs backed up to $BACKUP_DIR/improvement-$DATE.tar.gz"
```

**Cron:**
```bash
# Daily backup at 2 AM
0 2 * * * ~/backup-improvement-logs.sh
```

---

## Troubleshooting

### "Item not found"

**Problem:** Wrong item ID

**Solution:**
```bash
# List to find correct ID
smf run self-improvement list --type error

# ID format: ERR-YYYYMMDD-XXXXXX
```

### "No items found"

**Check:**
```bash
# Verify directories exist
ls -la ~/.smf/improvement/

# Check permissions
ls -la ~/.smf/improvement/errors/
```

### Search returns no results

**Try:**
```bash
# Broader search
smf run self-improvement search "file"

# Check all items
smf run self-improvement list

# Verify files exist
ls ~/.smf/improvement/errors/
ls ~/.smf/improvement/learnings/
```

### Promotion fails

**Check:**
```bash
# Verify item exists
smf run self-improvement show ITEM-ID

# Check permissions on memory file
ls -la ~/.smf/improvement/promoted.md

# Create file if missing
touch ~/.smf/improvement/promoted.md
```

### Memory file too large

**Archive old entries:**
```bash
# Rotate memory file
cp ~/.smf/improvement/promoted.md ~/.smf/improvement/promoted-$(date +%Y%m).md

# Start fresh
echo "# Project Memory" > ~/.smf/improvement/promoted.md
```

---

## Best Practices

### 1. Log Immediately

**Don't:**
- Wait until end of day
- Think "I'll remember this"

**Do:**
- Log while context is fresh
- Use quick syntax: `smf run self-improvement log-error "..."`

### 2. Be Specific

**Bad:**
- "Got an error"
- "Something broke"

**Good:**
- "FileNotFoundError: config.json in startup sequence"
- "API timeout after 30s on user endpoint"

### 3. Include Context

**Always document:**
- What you were doing
- What you expected
- What actually happened
- How you fixed it

### 4. Use Consistent Tags

**Pick a taxonomy:**
- By layer: frontend, backend, database, api
- By type: bug, feature, config, architecture
- By language: python, javascript, sql

**Stick to it.**

### 5. Review Regularly

**Weekly:**
- Review new learnings
- Look for patterns
- Promote important items

**Monthly:**
- Review promoted memory
- Archive outdated items
- Consolidate duplicates

### 6. Connect Learnings to Errors

**Reference related errors:**
```bash
smf run self-improvement log-learning "..." \
  --context "Learned from ERR-20260320-ABC123"
```

### 7. Update as You Learn More

**Don't:**
- Leave errors as "open" when fixed
- Skip prevention strategies

**Do:**
- Update with resolution
- Document prevention
- Mark status appropriately

### 8. Make It a Habit

**Integration:**
- Hook into your editor
- Add to git pre-commit
- Set daily reminders

---

## Next Steps

1. **Log your first error** — Get familiar with the format
2. **Log a learning** — Capture something you just learned
3. **Review weekly** — Make it part of your routine
4. **Promote to memory** — Build project knowledge
5. **Share with team** — Use promoted.md as onboarding

---

## Support

- **Documentation:** https://github.com/smfworks/smfworks-skills
- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **Email:** support@smf.works

---

*Last updated: March 20, 2026*
