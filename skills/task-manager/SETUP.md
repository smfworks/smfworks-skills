# Task Manager — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo)

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| SMF Works Pro subscription | [smfworks.com/subscribe](https://smfworks.com/subscribe) | $19.99/mo |
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| OpenClaw | Installed and authenticated | Free |
| smfworks-skills repository | Cloned via git | Included |

---

## Step 1 — Subscribe and Authenticate

```bash
openclaw auth status
```

If not subscribed: [smfworks.com/subscribe](https://smfworks.com/subscribe)

---

## Step 2 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 3 — Navigate and Verify

```bash
cd ~/smfworks-skills/skills/task-manager
python3 main.py help
```

---

## Verify Your Setup

Create a test project and task:

```bash
python3 main.py project add "Test Project"
python3 main.py task add "My first task" --project test-project --priority medium
python3 main.py board --project test-project
```

If you see the Kanban board with your task, setup is complete.

---

## Configuration Options

No configuration file needed. All task data is stored at `~/.smf/tasks/` automatically.

---

## Troubleshooting

**`Error: SMF Works Pro subscription required`** — Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

**`python3: command not found`** — Install Python 3.8+.

---

## Quick Reference

```bash
python3 main.py project add "Project Name"         # Create project
python3 main.py task add "Task title" --project X  # Add task
python3 main.py board --project X                  # View board
python3 main.py task move TASK-ID --to done        # Complete task
python3 main.py stats                               # View statistics
```

## Status Columns Reference

Tasks move through these Kanban columns in order:

| Column | Use when... |
|--------|-------------|
| `backlog` | Captured but not yet planned (default for new tasks) |
| `todo` | Planned for this week/sprint |
| `in-progress` | Actively being worked on right now |
| `review` | Work complete, needs review or testing |
| `done` | Finished and accepted |

## Priority Levels Reference

| Priority | When to use |
|----------|-------------|
| `low` | Nice to have, no urgency |
| `medium` | Normal priority, no deadline pressure |
| `high` | Important, needs attention this sprint |
| `critical` | Blocking other work or due immediately |

## Next Steps

Setup complete. See **HOWTO.md** for walkthroughs on project setup, task management, Kanban workflow, and cron automation.
