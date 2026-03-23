# Task Manager — How-To Guide

**Prerequisites:** SMF Works Pro subscription active. Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Set Up a Project](#1-how-to-set-up-a-project)
2. [How to Add and Manage Tasks](#2-how-to-add-and-manage-tasks)
3. [How to Use the Kanban Board](#3-how-to-use-the-kanban-board)
4. [How to Track Progress with Stats](#4-how-to-track-progress-with-stats)
5. [How to Handle Priority and Due Dates](#5-how-to-handle-priority-and-due-dates)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Set Up a Project

**What this does:** Creates a project container for grouping related tasks.

### Steps

**Step 1 — Navigate to the skill.**

```bash
cd ~/smfworks-skills/skills/task-manager
```

**Step 2 — Create your project.**

```bash
python3 main.py project add "Website Redesign"
```

Output:
```
✅ Project created: Website Redesign (website-redesign)
```

The slug in parentheses (`website-redesign`) is used in other commands.

**Step 3 — Create more projects if needed.**

```bash
python3 main.py project add "Q2 Marketing"
python3 main.py project add "Infrastructure Upgrade"
```

**Step 4 — List all projects.**

```bash
python3 main.py project list
```

**Result:** Projects are created and ready to receive tasks.

---

## 2. How to Add and Manage Tasks

**What this does:** Creates tasks with title, priority, due date, and assignee.

### Steps

**Step 1 — Add a task to a project.**

```bash
python3 main.py task add "Fix mobile navigation" --project website-redesign --priority high --due 2024-03-20 --assignee Alice
```

Output:
```
✅ Task created: TASK-A1B2C3
   Title: Fix mobile navigation
   Project: Website Redesign
   Priority: high
   Due: 2024-03-20
   Status: backlog
```

**Step 2 — Add more tasks.**

```bash
python3 main.py task add "Write unit tests" --project website-redesign --priority medium
python3 main.py task add "Design new homepage" --project website-redesign --priority critical --due 2024-03-15
```

**Step 3 — View a task's full details.**

```bash
python3 main.py task show TASK-A1B2C3
```

**Step 4 — Edit a task.**

```bash
python3 main.py task edit TASK-A1B2C3
```

The skill prompts you to update any field.

---

## 3. How to Use the Kanban Board

**What this does:** Shows tasks organized by status column — Backlog, Todo, In-Progress, Review, Done.

### Steps

**Step 1 — View the board for your project.**

```bash
python3 main.py board --project website-redesign
```

Output:
```
📋 Board: Website Redesign
═══════════════════════════════════════════════

BACKLOG (2)        TODO (1)         IN-PROGRESS (1)   DONE (3)
──────────         ─────────        ──────────────     ──────────
TASK-A1B2C3        TASK-D4E5F6      TASK-G7H8I9        TASK-J0K1
Fix nav bug        Write tests      Design homepage     Landing page
● high ⚠️ DUE      ● medium         ● critical          ✅ done
```

**Step 2 — Move a task forward.**

When you start working on a task, move it to `in-progress`:

```bash
python3 main.py task move TASK-A1B2C3 --to in-progress
```

When it's ready for review:

```bash
python3 main.py task move TASK-A1B2C3 --to review
```

When done:

```bash
python3 main.py task move TASK-A1B2C3 --to done
```

**Step 3 — View all tasks across all projects.**

```bash
python3 main.py board
```

**Result:** A clear visual overview of your project's work in progress.

---

## 4. How to Track Progress with Stats

```bash
python3 main.py stats --project website-redesign
```

Output:
```
📊 Statistics: Website Redesign

Total tasks: 12
  Backlog: 3  |  To Do: 2  |  In Progress: 2  |  Review: 1  |  Done: 4

Completion rate: 33.3%
Critical tasks: 1
Overdue: 1

Assignees:
  Alice: 5 tasks
  Bob: 3 tasks
  Unassigned: 4 tasks
```

---

## 5. How to Handle Priority and Due Dates

**Priority levels** (used with `--priority`):

| Level | When to use |
|-------|-------------|
| `low` | Nice to have, no urgency |
| `medium` | Normal work, no deadline pressure |
| `high` | Important, needs attention this sprint |
| `critical` | Blocking or deadline tomorrow |

**Viewing tasks by priority:**

```bash
python3 main.py list --status in-progress
```

**The board shows ⚠️ DUE** next to tasks with overdue or soon-due dates.

---

## 6. Automating with Cron

### Example: Daily standup board print at 9 AM

```bash
0 9 * * 1-5 python3 /home/yourname/smfworks-skills/skills/task-manager/main.py board >> /home/yourname/logs/daily-board.log 2>&1
```

### Example: Weekly stats report every Monday

```bash
0 8 * * 1 python3 /home/yourname/smfworks-skills/skills/task-manager/main.py stats > /home/yourname/Reports/weekly-tasks-$(date +\%Y-W\%V).txt 2>&1
```

---

## 7. Combining with Other Skills

**Task Manager + Self Improvement:** Log learnings from completed tasks:

```bash
python3 main.py task move TASK-ABC --to done
python3 ~/smfworks-skills/skills/self-improvement/main.py log-learning "Learned that CSS grid works better than flexbox for this layout" --tags css,frontend
```

**Task Manager + Coffee Briefing:** Morning briefing includes calendar; add a task board review:

```bash
python3 ~/smfworks-skills/skills/coffee-briefing/main.py
python3 ~/smfworks-skills/skills/task-manager/main.py board --project myproject
```

---

## 8. Troubleshooting Common Issues

### `Task not found: TASK-XYZ`

Task IDs are case-sensitive.  
**Fix:** Run `python3 main.py list` to see exact IDs.

### Board looks cluttered

Too many tasks in one view.  
**Fix:** Use `--project PROJECT-SLUG` to filter to a specific project.

### `Project not found: my project`

You're using the display name instead of the slug.  
**Fix:** Use the slug (lowercase hyphenated). `python3 main.py project list` shows both display names and slugs.

---

## 9. Tips & Best Practices

**Use projects to group work.** One project per major effort. Don't put everything in one project — it makes the board unreadable.

**Move tasks through status actively.** The board is only useful if you keep it updated. Make a habit of moving tasks to `in-progress` when you start and `done` when you finish.

**Use `--priority critical` sparingly.** If everything is critical, nothing is. Reserve `critical` for actual blockers or same-day deadlines.

**Set due dates on important tasks.** Due dates trigger the ⚠️ DUE indicator on the board. Without them, overdue tasks are invisible.

**Review stats weekly.** The completion rate and overdue count from `stats` are your project health indicators. A rising overdue count signals capacity issues.
