# Task Manager

> Manage tasks and projects with a Kanban-style board in your terminal — with priorities, due dates, assignees, and project grouping.

**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo at [smfworks.com/subscribe](https://smfworks.com/subscribe))  
**Version:** 1.0  
**Category:** Productivity / Project Management

---

## What It Does

Task Manager is an OpenClaw Pro skill for tracking work with a command-line Kanban board. Create projects, add tasks with priorities and due dates, move tasks through status columns (backlog → todo → in-progress → review → done), and see statistics on your project progress.

All tasks are stored locally in `~/.smf/tasks/`. No cloud sync, no subscription-per-seat — just fast, private task management.

**What it does NOT do:** It does not sync to Jira, Trello, Asana, or other platforms, send notifications, track time, or handle recurring tasks.

---

## Prerequisites

- [ ] **SMF Works Pro subscription** — [smfworks.com/subscribe](https://smfworks.com/subscribe)
- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed and authenticated**

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/task-manager
python3 main.py help
```

---

## Quick Start

```bash
# Create a project
python3 main.py project add "Website Redesign"

# Add a task
python3 main.py task add "Fix navigation bug" --project website --priority high

# View the board
python3 main.py board --project website

# Move task to in-progress
python3 main.py task move TASK-ABC123 --to in-progress
```

---

## Command Reference

### `project add "Name"`

Creates a new project.

```bash
python3 main.py project add "Website Redesign"
python3 main.py project add "Q2 Marketing" "Marketing campaigns for Q2"
```

Output:
```
✅ Project created: Website Redesign (website-redesign)
```

---

### `project list`

Lists all projects.

```bash
python3 main.py project list
```

Output:
```
📁 Projects (3 total):

1. Website Redesign (website-redesign) — 12 tasks, 4 done
2. Q2 Marketing (q2-marketing) — 8 tasks, 2 done
3. Infrastructure (infrastructure) — 5 tasks, 1 done
```

---

### `task add "Title"`

Adds a task. Interactive if no flags provided; flags for quick add.

```bash
python3 main.py task add "Fix navigation bug"
python3 main.py task add "Fix navigation" --project website --priority high --due 2024-03-20
python3 main.py task add "Write tests" --project website --priority medium --assignee "Alice"
```

**Options for task add:**

| Option | Description | Values |
|--------|-------------|--------|
| `--project PROJECT` | Project slug | e.g., `website-redesign` |
| `--priority LEVEL` | Priority | `low`, `medium`, `high`, `critical` |
| `--due YYYY-MM-DD` | Due date | e.g., `2024-03-20` |
| `--assignee NAME` | Assigned to | Any name |
| `--tags TAGS` | Comma-separated tags | e.g., `bug,frontend` |
| `--description TEXT` | Task description | Any text |

Output:
```
✅ Task created: TASK-ABC123
   Title: Fix navigation bug
   Project: Website Redesign
   Priority: high
   Status: backlog
```

---

### `board`

Shows the Kanban board for a project (or all tasks).

```bash
python3 main.py board
python3 main.py board --project website-redesign
```

Output:
```
📋 Board: Website Redesign
═══════════════════════════════════════════════════════

BACKLOG (3)          TODO (2)          IN-PROGRESS (2)   REVIEW (1)    DONE (4)
──────────────       ─────────────     ──────────────     ──────────    ──────────
TASK-001             TASK-004          TASK-006 ⚠️ DUE    TASK-008      TASK-003
Fix nav bug          Write tests       Design mockups      Code review   Landing page
● high               ● medium          ● high             ● medium      ✅ done

TASK-002             TASK-005          TASK-007
Add dark mode        Review PRs        API integration
● medium             ● low             ● critical
...
```

---

### `task move TASK-ID --to STATUS`

Moves a task to a different Kanban column.

```bash
python3 main.py task move TASK-ABC123 --to in-progress
python3 main.py task move TASK-ABC123 --to done
```

Status columns: `backlog` → `todo` → `in-progress` → `review` → `done`

Output:
```
✅ Task TASK-ABC123 moved to in-progress
```

---

### `task show TASK-ID`

Shows full task details.

```bash
python3 main.py task show TASK-ABC123
```

Output:
```
📋 Task: TASK-ABC123

Title: Fix navigation bug
Project: Website Redesign
Status: in-progress
Priority: high 🔴
Due: 2024-03-20 (5 days remaining)
Assignee: Alice
Tags: bug, frontend
Description: Navigation links don't work on mobile Safari
Created: 2024-03-15 09:42
```

---

### `task edit TASK-ID`

Prompts to update task fields.

```bash
python3 main.py task edit TASK-ABC123
```

---

### `list`

Lists all tasks with optional filters.

```bash
python3 main.py list
python3 main.py list --status in-progress
python3 main.py list --project website-redesign
```

---

### `stats`

Shows project statistics.

```bash
python3 main.py stats
python3 main.py stats --project website-redesign
```

Output:
```
📊 Statistics: Website Redesign

Total tasks: 12
  Backlog: 3
  To Do: 2
  In Progress: 2
  Review: 1
  Done: 4

Completion rate: 33.3%
Critical tasks: 1
Overdue: 1
```

---

## Use Cases

### 1. Personal project tracking

Track tasks for any personal project with priorities and due dates.

### 2. Team task assignment

Assign tasks to team members with `--assignee` and view who's working on what.

### 3. Daily standup prep

View the board each morning before standup: `python3 main.py board --project myproject`

---

## Configuration

No configuration file needed. Data stored at: `~/.smf/tasks/`

---

## Troubleshooting

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

### `Task not found: TASK-XYZ`
**Fix:** Task IDs are case-sensitive. Use `python3 main.py list` to find the exact ID.

### `Project not found`
**Fix:** Use the project slug (lowercase, hyphenated), not the display name. Check with `python3 main.py project list`.

### Board shows all tasks instead of one project
**Fix:** Use `--project PROJECT-SLUG` to filter by project.

---

## FAQ

**Q: Can I delete a task?**  
A: `task delete TASK-ID` archives the task (moves it to an archived state, not permanent deletion).

**Q: Can I export tasks?**  
A: Tasks are stored as JSON in `~/.smf/tasks/`. You can export or process the JSON directly.

**Q: What's the difference between `list` and `board`?**  
A: `list` shows a simple list of tasks. `board` shows the Kanban view organized by status columns.

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

- 📖 [Documentation](https://smfworks.com/skills/task-manager)
- 🔑 [Subscribe](https://smfworks.com/subscribe)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
