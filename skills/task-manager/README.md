# Task/Project Manager

Kanban-style task and project management for individuals and teams. Create projects, manage tasks through stages, track progress.

## Features

- ✅ **Projects** — Create and organize multiple projects
- ✅ **Kanban Board** — Visual task management (backlog, todo, in-progress, review, done)
- ✅ **Task Priorities** — Low, medium, high, critical
- ✅ **Due Dates** — Track deadlines and get overdue alerts
- ✅ **Assignments** — Assign tasks to team members
- ✅ **Tags** — Categorize and filter tasks
- ✅ **Statistics** — Completion rates, workload analysis
- ✅ **Local Storage** — All data stays on your machine

## Installation

```bash
# Install SMF CLI (if not already)
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash

# Login (Pro skill requires subscription)
smf login

# Install the skill
smf install task-manager
```

## Quick Start

### 1. Create a Project

```bash
smf run task-manager project add "Website Redesign" "Complete redesign of company website"
```

### 2. Add Tasks

```bash
# Interactive mode
smf run task-manager task add

# Or specify details
smf run task-manager task add "Fix navigation bug" \
  --project "Website Redesign" \
  --priority high \
  --due 2026-03-25 \
  --assignee "John"
```

### 3. View Kanban Board

```bash
smf run task-manager board --project "Website Redesign"
```

Output:
```
📋 Kanban Board
================================================================================
Project: Website Redesign

📥 BACKLOG (2)
------------------------------------------------------------------------------
   🟡 TASK-A1B2C3D4: Research competitor websites...
   🟢 TASK-E5F6G7H8: Draft content outline

📝 TODO (3)
------------------------------------------------------------------------------
   🔴 TASK-I9J0K1L2: Fix navigation bug 📅 2026-03-25
   🟠 TASK-M3N4O5P6: Update hero section
   🟡 TASK-Q7R8S9T0: Optimize images

🔄 IN-PROGRESS (1)
------------------------------------------------------------------------------
   🟠 TASK-U1V2W3X4: Redesign footer

👀 REVIEW (0)
------------------------------------------------------------------------------
   (empty)

✅ DONE (2)
------------------------------------------------------------------------------
   ✅ TASK-Y5Z6A7B8: Create color palette
   ✅ TASK-C9D0E1F2: Set up project
```

### 4. Move Tasks

```bash
smf run task-manager task move TASK-I9J0K1L2 --to in-progress
smf run task-manager task move TASK-I9J0K1L2 --to done
```

### 5. Check Statistics

```bash
smf run task-manager stats --project "Website Redesign"
```

## Usage

### Project Commands

**Create project:**
```bash
smf run task-manager project add "Project Name" "Description"
```

**List projects:**
```bash
smf run task-manager project list
```

### Task Commands

**Add task (interactive):**
```bash
smf run task-manager task add
```

**Add task (quick):**
```bash
smf run task-manager task add "Task title" \
  --project "Website" \
  --priority high \
  --due 2026-03-25 \
  --assignee "John" \
  --tags "bug,urgent"
```

**Show task details:**
```bash
smf run task-manager task show TASK-ABC123
```

**Move task:**
```bash
smf run task-manager task move TASK-ABC123 --to in-progress
```

Valid statuses: `backlog`, `todo`, `in-progress`, `review`, `done`, `archived`

**Archive task:**
```bash
smf run task-manager task delete TASK-ABC123
```

### Board View

**Show all projects:**
```bash
smf run task-manager board
```

**Show specific project:**
```bash
smf run task-manager board --project "Website Redesign"
```

### List View

**List all tasks:**
```bash
smf run task-manager list
```

**List by status:**
```bash
smf run task-manager list --status todo
smf run task-manager list --status in-progress
```

### Statistics

**All projects:**
```bash
smf run task-manager stats
```

**Specific project:**
```bash
smf run task-manager stats --project "Website Redesign"
```

Output:
```
📊 Task Statistics
========================================
Project: Website Redesign

Total Tasks: 15
Completed: 7 (46.7%)
Due Soon (≤3 days): 3
⚠️  Overdue: 1

By Status:
  backlog: 3
  todo: 4
  in-progress: 1
  done: 7

By Priority:
  critical: 2
  high: 5
  medium: 6
  low: 2
```

## Workflow

### Personal Task Management

1. **Capture** — Add tasks to backlog
2. **Prioritize** — Move high priority to todo
3. **Focus** — Work on in-progress tasks
4. **Complete** — Move to done when finished
5. **Review** — Weekly stats review

### Team Collaboration

1. **Project Setup** — Create project, invite team
2. **Assignment** — Assign tasks by expertise
3. **Tracking** — Daily standup using board view
4. **Review** — Code review/QA in review column
5. **Ship** — Complete and archive

## Priority Levels

| Level | Icon | Use For |
|-------|------|---------|
| Critical | 🔴 | Blockers, emergencies |
| High | 🟠 | Important deadlines |
| Medium | 🟡 | Normal tasks |
| Low | 🟢 | Nice-to-haves |

## Status Columns

| Column | Purpose |
|--------|---------|
| Backlog | Ideas, future work |
| Todo | Ready to work on |
| In-Progress | Currently working |
| Review | Needs review/QA |
| Done | Complete |
| Archived | Closed/hidden |

## Task Data

Each task includes:
- **ID:** Unique identifier (TASK-XXXXXXXX)
- **Title:** Short description
- **Description:** Full details
- **Project:** Which project it belongs to
- **Status:** Current column
- **Priority:** Importance level
- **Due Date:** Deadline
- **Assignee:** Who's responsible
- **Tags:** Categories
- **Created:** When added
- **Updated:** Last change
- **Completed:** When finished

## Storage Location

Projects and tasks stored in:
```
~/.smf/tasks/
├── projects.json         # Project definitions
├── task-TASK-XXXXXXXX.json  # Individual task files
└── ...
```

All data is local and private.

## Tips & Tricks

### Daily Standup Script

Create `~/standup.sh`:
```bash
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"

echo "📋 Yesterday's completed:"
smf run task-manager list --status done | tail -5

echo ""
echo "🔄 In progress:"
smf run task-manager list --status in-progress

echo ""
echo "📝 Today's plan:"
smf run task-manager list --status todo | head -5
```

Make executable:
```bash
chmod +x ~/standup.sh
~/standup.sh
```

### Weekly Review

```bash
# Check overdue tasks
smf run task-manager stats

# Archive completed
# (Tasks in done column automatically tracked)
```

### Priority Filtering

Combine with grep:
```bash
# Show only critical tasks
smf run task-manager list | grep "🔴"

# Show overdue
smf run task-manager stats | grep "Overdue"
```

## Backup

```bash
# Backup all tasks
cp -r ~/.smf/tasks ~/backups/tasks-$(date +%Y%m%d)

# Or sync to cloud
rclone sync ~/.smf/tasks gdrive:tasks-backup/
```

## Pricing

**Task Manager is a premium SMF Works skill.**

This is a paid skill that is part of the SMF Works subscription service. One monthly fee for unlimited access to the growing library of premium SMF Skills and applications.

- **Price:** $19.99/month (locked forever at signup rate)
- **Includes:** All premium skills, updates, priority support
- **Free alternative:** Use Trello, GitHub Issues, or pen and paper

Subscribe at https://smf.works/subscribe

## See Also

- [SETUP.md](./SETUP.md) — Complete setup and configuration guide
- `smf help` — CLI documentation
- `smf status` — Check subscription status

## License

SMF Works Pro Skill — See SMF Works Terms of Service
