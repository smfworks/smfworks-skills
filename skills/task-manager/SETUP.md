# Task/Project Manager - Setup & Configuration Guide

Complete setup instructions for installing, configuring, and using the Task/Project Manager skill.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Authentication Setup](#authentication-setup)
4. [Quick Start](#quick-start)
5. [Project Configuration](#project-configuration)
6. [Task Management](#task-management)
7. [Workflows](#workflows)
8. [Automation](#automation)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## Prerequisites

### System Requirements
- **OS:** Linux, macOS, or Windows with Python
- **Python:** 3.8 or higher
- **Storage:** Minimal (~1MB per 100 tasks)

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

### Step 3: Install Task Manager

```bash
smf install task-manager
```

### Step 4: Verify Installation

```bash
smf run task-manager --help
```

---

## Quick Start

### Your First Project

```bash
# Create project
smf run task-manager project add "My First Project" "Learning the task manager"

# Add tasks
smf run task-manager task add "Learn the commands" --project "My First Project" --priority high
smf run task-manager task add "Create more tasks" --project "My First Project" --priority medium

# View board
smf run task-manager board --project "My First Project"
```

### Basic Workflow

```bash
# 1. Create project
smf run task-manager project add "Website"

# 2. Add tasks to backlog
smf run task-manager task add "Design homepage" --project Website --priority high
smf run task-manager task add "Write content" --project Website --priority medium

# 3. View board
smf run task-manager board --project Website

# 4. Move task to in-progress
smf run task-manager task move TASK-ABC123 --to in-progress

# 5. Complete task
smf run task-manager task move TASK-ABC123 --to done

# 6. Check stats
smf run task-manager stats --project Website
```

---

## Project Configuration

### Creating Projects

**Interactive:**
```bash
smf run task-manager project add
# Enter name and description when prompted
```

**Command line:**
```bash
smf run task-manager project add "Project Name" "Description"
```

### Project Best Practices

**Naming:**
- ✅ "Website Redesign 2026"
- ✅ "Q1 Marketing Campaign"
- ✅ "Product Launch - March"
- ❌ "Project 1"
- ❌ "New stuff"

**When to Create New Projects:**
- Major initiatives (> 2 weeks)
- Different teams
- Different clients
- Different quarters

**When to Use Same Project:**
- Related tasks
- Same team
- Same timeline

---

## Task Management

### Creating Tasks

**Interactive (recommended for new users):**
```bash
smf run task-manager task add
```

You'll be prompted for:
- Project (select or create)
- Title (required)
- Description (optional)
- Priority (low/medium/high/critical)
- Due date (optional)
- Assignee (optional)
- Tags (optional)

**Quick add (for power users):**
```bash
smf run task-manager task add "Title" \
  --project "Project Name" \
  --priority high \
  --due 2026-03-25 \
  --assignee "John" \
  --tags "bug,urgent"
```

### Task Priorities

| Priority | When to Use | Emoji |
|----------|-------------|-------|
| **Critical** | Blockers, production issues | 🔴 |
| **High** | Important deadlines | 🟠 |
| **Medium** | Normal work | 🟡 |
| **Low** | Nice-to-have, backlog | 🟢 |

**Priority Guidelines:**
- 10% of tasks should be critical
- 30% high
- 50% medium
- 10% low

### Moving Tasks

**Status workflow:**
```
Backlog → Todo → In-Progress → Review → Done → Archived
```

**Commands:**
```bash
# To backlog (ideas)
smf run task-manager task move TASK-ABC123 --to backlog

# Ready to start
smf run task-manager task move TASK-ABC123 --to todo

# Working on it
smf run task-manager task move TASK-ABC123 --to in-progress

# Needs review
smf run task-manager task move TASK-ABC123 --to review

# Complete
smf run task-manager task move TASK-ABC123 --to done

# Hide/close
smmf run task-manager task move TASK-ABC123 --to archived
```

### Due Dates

**Format:** YYYY-MM-DD

**Examples:**
```bash
--due 2026-03-25      # March 25, 2026
--due 2026-12-31      # End of year
--due 2027-01-15      # Next year
```

**Relative dates (shell):**
```bash
# Due tomorrow
smf run task-manager task add "Task" --due $(date -d "tomorrow" +%Y-%m-%d)

# Due in 3 days
smf run task-manager task add "Task" --due $(date -d "+3 days" +%Y-%m-%d)

# Due next Friday
smf run task-manager task add "Task" --due $(date -d "next Friday" +%Y-%m-%d)
```

### Tags

**Usage:**
```bash
--tags "bug,frontend,urgent"
--tags "feature,mobile"
--tags "documentation"
```

**Common tag categories:**
- Type: `bug`, `feature`, `docs`, `test`
- Area: `frontend`, `backend`, `database`, `api`
- Effort: `quick`, `medium`, `large`
- Blocker: `blocked`, `waiting`, `review-needed`

---

## Workflows

### Personal Workflow (GTD-style)

**Daily:**
```bash
# Morning - review board
smf run task-manager board

# Pick 3 tasks for today
smf run task-manager task move TASK-1 --to in-progress
smf run task-manager task move TASK-2 --to in-progress
smf run task-manager task move TASK-3 --to in-progress

# Evening - complete done tasks
smf run task-manager task move TASK-1 --to done
smf run task-manager stats
```

**Weekly:**
```bash
# Review backlog
smf run task-manager list --status backlog

# Plan next week
smf run task-manager task move TASK-NEW --to todo

# Check stats
smf run task-manager stats
```

### Team Workflow (Agile/Scrum)

**Sprint Planning:**
```bash
# Review backlog
smf run task-manager list --status backlog --project "Sprint 5"

# Move to todo (sprint commitment)
smf run task-manager task move TASK-1 --to todo
smf run task-manager task move TASK-2 --to todo
# ...
```

**Daily Standup:**
```bash
# What's in progress?
smf run task-manager list --status in-progress

# What's blocked?
smf run task-manager list | grep "blocked"

# What did I complete yesterday?
smf run task-manager list --status done | head -5
```

**Sprint Review:**
```bash
# Completion rate
smf run task-manager stats --project "Sprint 5"

# Demo ready items
smf run task-manager list --status done
```

### Client Project Workflow

**Structure:**
```
Project: Client - ABC Corp Website
├── Task 1: Discovery (backlog)
├── Task 2: Wireframes (todo)
├── Task 3: Design (in-progress)
├── Task 4: Development (backlog)
└── Task 5: Launch (backlog)
```

**Client updates:**
```bash
# Show progress
smf run task-manager stats --project "ABC Corp Website"

# Export for client report
smf run task-manager list --project "ABC Corp Website" > status-report.txt
```

---

## Automation

### Daily Standup Script

Create `~/standup.sh`:
```bash
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"

echo "=== Daily Standup $(date) ==="
echo ""

echo "✅ Yesterday (completed):"
smf run task-manager list --status done | tail -3

echo ""
echo "🔄 Today (in progress):"
smf run task-manager list --status in-progress

echo ""
echo "📝 Next (todo):"
smf run task-manager list --status todo | head -3

echo ""
echo "⚠️  Blockers:"
smf run task-manager list | grep -i "blocked\|critical" || echo "None"
```

Make executable:
```bash
chmod +x ~/standup.sh
```

Run daily:
```bash
~/standup.sh
```

### Weekly Planning Script

Create `~/weekly-planning.sh`:
```bash
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"

echo "📊 Weekly Review"
echo "================"

# Show stats for all projects
smf run task-manager stats

echo ""
echo "⚠️  Overdue Tasks:"
smf run task-manager list | grep "$(date +%Y-%m-%d)" || echo "None"

echo ""
echo "📋 Backlog to Review:"
smf run task-manager list --status backlog | head -10
```

### Backup Script

```bash
#!/bin/bash
# Backup tasks daily

cp -r ~/.smf/tasks ~/backups/tasks-$(date +%Y%m%d)

# Keep only last 30 days
find ~/backups -name "tasks-*" -mtime +30 -delete
```

Add to cron:
```bash
0 2 * * * ~/backup-tasks.sh
```

### Due Date Reminders

```bash
#!/bin/bash
# Check for tasks due today or tomorrow

export PATH="$HOME/.local/bin:$PATH"

echo "⏰ Due Soon:"
smf run task-manager stats | grep "Due Soon"
```

---

## Troubleshooting

### "Project not found"

**Problem:** Wrong project name

**Solution:**
```bash
# List projects
smf run task-manager project list

# Use exact name or project ID
smf run task-manager board --project "Exact Project Name"
```

### "Task not found"

**Problem:** Wrong task ID

**Solution:**
```bash
# List all tasks to get ID
smf run task-manager list

# ID format: TASK-XXXXXXXX (8 characters)
```

### "No projects exist"

**Solution:**
```bash
# Create your first project
smf run task-manager project add "My Project"
```

### Board is empty

**Check:**
```bash
# Are there tasks?
smf run task-manager list

# Are they assigned to the project?
smf run task-manager list --project "Your Project"

# Try without project filter
smf run task-manager board
```

### Too many tasks in list

**Filter by status:**
```bash
# Show only todo
smf run task-manager list --status todo

# Show only in-progress
smf run task-manager list --status in-progress
```

### Can't move task

**Valid statuses:**
- `backlog`
- `todo`
- `in-progress`
- `review`
- `done`
- `archived`

**Check spelling:**
```bash
# Wrong
smf run task-manager task move TASK-123 --to "in progress"

# Correct
smf run task-manager task move TASK-123 --to in-progress
```

### Data storage issues

**Check permissions:**
```bash
ls -la ~/.smf/tasks/

# Should show your user owns files
# If not:
chown -R $USER:$USER ~/.smf/tasks/
chmod 700 ~/.smf/tasks/
```

### Corrupted data

**Check JSON files:**
```bash
# Validate a task file
python3 -m json.tool ~/.smf/tasks/task-TASK-XXXX.json

# If corrupted, you may need to delete and recreate
```

---

## Best Practices

### 1. Keep Task Titles Short

**Good:**
- "Fix login redirect bug"
- "Add password reset"
- "Update footer copyright"

**Bad:**
- "Fix the bug where users can't login and get redirected to the wrong page sometimes"
- "Task 1"

### 2. Use Descriptions for Details

```bash
smf run task-manager task add "Fix login bug"
# Then edit to add description
```

Or include in interactive mode.

### 3. Set Realistic Due Dates

**Don't:**
- Set everything to today
- Set vague "ASAP" dates
- Forget to update when delayed

**Do:**
- Set specific dates
- Update when scope changes
- Review weekly

### 4. Prioritize Ruthlessly

**Rule:** If everything is high priority, nothing is.

**Distribution:**
- Critical: 10% (emergencies only)
- High: 30%
- Medium: 50%
- Low: 10%

### 5. Review Backlog Weekly

```bash
# Every Monday morning
smf run task-manager list --status backlog

# Archive old ideas
smf run task-manager task move TASK-OLD --to archived
```

### 6. Limit Work in Progress

**Rule:** Max 3 tasks in "in-progress"

**Why:** Focus on completing, not starting

### 7. Move Tasks Promptly

- When you start working → `in-progress`
- When ready for review → `review`
- When complete → `done`
- Don't leave in wrong columns

### 8. Use Tags Consistently

**Pick a tagging scheme:**

**Option A - By type:**
- `bug`, `feature`, `docs`, `test`

**Option B - By area:**
- `frontend`, `backend`, `database`, `infrastructure`

**Option C - Combined:**
- `bug-frontend`, `feature-backend`

**Stick to one approach.**

### 9. Regular Cleanup

**Weekly:**
- Archive done tasks older than 2 weeks
- Review stalled tasks (> 1 week in-progress)

**Monthly:**
- Review backlog, remove outdated items
- Update priorities

### 10. Backup Your Data

```bash
# Before major changes
cp -r ~/.smf/tasks ~/.smf/tasks-backup-$(date +%Y%m%d)

# Weekly automated backup
rsync -av ~/.smf/tasks/ ~/Dropbox/tasks-backup/
```

---

## Next Steps

1. **Create first project** — Get familiar
2. **Add 5-10 tasks** — Build your backlog
3. **Try the board view** — Visual workflow
4. **Move tasks through statuses** — Complete a workflow
5. **Check statistics** — See your productivity
6. **Set up automation** — Daily standup script

---

## Support

- **Documentation:** https://github.com/smfworks/smfworks-skills
- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **Email:** support@smf.works

---

*Last updated: March 20, 2026*
