# Task Manager — Quick Reference

## Install
```bash
smfw install task-manager
```

## Commands
```bash
smf run task-manager project add "My Project"           # Create project
smf run task-manager task add "Task title"             # Add task
smf run task-manager task show TASK-123                # Show task
smf run task-manager task move TASK-123 --to done      # Move task
smf run task-manager board                             # View Kanban board
smf run task-manager list                              # List all tasks
smf run task-manager stats                             # Show statistics
```

## Common Examples
```bash
# Create a project
smf run task-manager project add "Website Redesign"

# Add a task
smf run task-manager task add "Fix navigation" --project "Website Redesign" --priority high

# View Kanban board
smf run task-manager board --project "Website Redesign"

# Move task to done
smf run task-manager task move TASK-ABC123 --to done

# List all tasks
smf run task-manager list

# View statistics
smf run task-manager stats
```

## Help
```bash
smf run task-manager help
```
