# Task Manager

> Kanban-style task and project management for individuals and teams

---

## What It Does

Task Manager brings simple project management to your terminal. Create projects, add tasks with priorities and due dates, move them across Kanban columns (backlog, todo, in-progress, review, done), and track your progress with statistics.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Pro tier:**
```bash
smfw install task-manager
smf login
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Create a project and add your first task:

```bash
smf run task-manager project add "My Project"
smf run task-manager task add "First task" --project "My Project"
```

---

## Commands

### `project add`

**What it does:** Create a new project.

**Usage:**
```bash
smf run task-manager project add [name] [description]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `name` | ✅ Yes | Project name | `Website Redesign` |
| `description` | ❌ No | Project description | `Redesign company website` |

**Example:**
```bash
smf run task-manager project add "Website Redesign"
smf run task-manager project add "Website Redesign" "Redesign company website"
```

---

### `project list`

**What it does:** List all projects.

**Usage:**
```bash
smf run task-manager project list
```

---

### `task add`

**What it does:** Add a new task to a project.

**Usage:**
```bash
smf run task-manager task add [title] [options]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `title` | ✅ Yes | Task title | `Fix navigation` |

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--project` | ❌ No | Project name or ID | `--project "Website Redesign"` |
| `--priority` | ❌ No | low/medium/high/critical | `--priority high` |
| `--due` | ❌ No | Due date (YYYY-MM-DD) | `--due 2026-04-01` |
| `--assignee` | ❌ No | Person assigned | `--assignee "John"` |
| `--tags` | ❌ No | Comma-separated tags | `--tags "bug,urgent"` |

**Example:**
```bash
smf run task-manager task add "Fix navigation" --priority high --due 2026-04-01
smf run task-manager task add "Write content" --project "Website Redesign" --tags "content"
```

---

### `task show`

**What it does:** Show full details of a task.

**Usage:**
```bash
smf run task-manager task show [task-id]
```

**Example:**
```bash
smf run task-manager task show TASK-ABC123
```

---

### `task move`

**What it does:** Move a task to a different status column.

**Usage:**
```bash
smf run task-manager task move [task-id] --to [status]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `task-id` | ✅ Yes | Task ID | `TASK-ABC123` |

**Options:**

| Option | Required | Description |
|--------|----------|-------------|
| `--to` | ✅ Yes | Target status |

**Statuses:** `backlog`, `todo`, `in-progress`, `review`, `done`

**Example:**
```bash
smf run task-manager task move TASK-ABC123 --to done
smf run task-manager task move TASK-ABC123 --to in-progress
```

---

### `board`

**What it does:** Display Kanban board view of tasks.

**Usage:**
```bash
smf run task-manager board [options]
```

**Options:**

| Option | Required | Description |
|--------|----------|-------------|
| `--project` | ❌ No | Filter by project name |

**Example:**
```bash
smf run task-manager board
smf run task-manager board --project "Website Redesign"
```

---

### `list`

**What it does:** List all tasks in table format.

**Usage:**
```bash
smf run task-manager list [options]
```

**Options:**

| Option | Required | Description |
|--------|----------|-------------|
| `--status` | ❌ No | Filter by status |

**Example:**
```bash
smf run task-manager list
smf run task-manager list --status todo
```

---

### `stats`

**What it does:** Show project/task statistics.

**Usage:**
```bash
smf run task-manager stats [options]
```

**Example:**
```bash
smf run task-manager stats
```

**Output:**
```
📊 Task Statistics
==================================================

Total Tasks: 25
Completed: 18 (72.0%)
Due Soon (≤3 days): 3

By Status:
  todo: 5
  in-progress: 2
  review: 1
  done: 18

By Priority:
  critical: 2
  high: 5
  medium: 10
  low: 8
```

---

## Use Cases

- **Personal productivity:** Track personal tasks and to-dos
- **Project tracking:** Manage tasks for specific projects
- **Kanban workflow:** Visualize work across columns
- **Prioritization:** Focus on high-priority tasks
- **Due date tracking:** Never miss a deadline

---

## Tips & Tricks

- Create projects to organize tasks by area
- Use priorities to focus on what matters most
- Use `--due` to track deadlines
- Check `stats` regularly for progress overview
- Move tasks to `done` when completed

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Subscription required" | Run `smf login` to activate Pro access |
| "Project not found" | Check project name with `project list` |
| "Invalid status" | Use: backlog, todo, in-progress, review, done |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- Pro subscription

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/task-manager)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
