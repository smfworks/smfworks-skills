#!/usr/bin/env python3
"""
Task/Project Manager - SMF Works Pro Skill
Kanban-style task and project management for individuals and teams.

Usage:
    smf run task-manager task add "Fix login bug" --project website --priority high --due 2026-03-25
    smf run task-manager board --project website
    smf run task-manager task move TASK-123 --to done
    smf run task-manager list --status todo
    smf run task-manager stats
"""

import sys
import json
import fcntl
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid

# Add shared auth to path
shared_path = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from smf_auth import require_subscription, show_subscription_error

# Skill configuration
SKILL_NAME = "task-manager"
MIN_TIER = "pro"
TASKS_DIR = Path.home() / ".smf" / "tasks"
PROJECTS_FILE = TASKS_DIR / "projects.json"
LOCK_FILE = TASKS_DIR / ".lock"

# Status columns (Kanban)
STATUSES = ["backlog", "todo", "in-progress", "review", "done", "archived"]
PRIORITIES = ["low", "medium", "high", "critical"]


def ensure_dirs():
    """Ensure tasks directory exists."""
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    if not PROJECTS_FILE.exists():
        PROJECTS_FILE.write_text(json.dumps({"projects": []}, indent=2))


class FileLock:
    """Simple file-based lock for preventing race conditions."""
    
    def __init__(self, lock_path: Path, timeout: float = 10.0):
        self.lock_path = lock_path
        self.timeout = timeout
        self.lock_file = None
    
    def __enter__(self):
        """Acquire lock with timeout."""
        start_time = time.time()
        while True:
            try:
                self.lock_file = open(self.lock_path, 'w')
                fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except (IOError, OSError):
                if time.time() - start_time >= self.timeout:
                    raise TimeoutError("Could not acquire lock")
                time.sleep(0.1)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Release lock."""
        if self.lock_file:
            try:
                fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_UN)
                self.lock_file.close()
                # Try to remove lock file
                try:
                    self.lock_path.unlink()
                except:
                    pass
            except:
                pass
        return False


def atomic_write_json(file_path: Path, data: Dict):
    """Write JSON file atomically to prevent data corruption."""
    temp_path = file_path.with_suffix('.tmp')
    try:
        temp_path.write_text(json.dumps(data, indent=2))
        temp_path.rename(file_path)
    except Exception as e:
        # Cleanup temp file on error
        try:
            temp_path.unlink()
        except:
            pass
        raise e


def generate_task_id() -> str:
    """Generate unique task ID using UUID to prevent collisions."""
    return f"TASK-{uuid.uuid4().hex[:8].upper()}"


def load_projects() -> List[Dict]:
    """Load all projects with locking."""
    ensure_dirs()
    try:
        with FileLock(LOCK_FILE):
            data = json.loads(PROJECTS_FILE.read_text())
            return data.get("projects", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    except TimeoutError:
        print("⚠️  Could not acquire lock, trying without...", file=sys.stderr)
        try:
            data = json.loads(PROJECTS_FILE.read_text())
            return data.get("projects", [])
        except:
            return []


def save_projects(projects: List[Dict]):
    """Save projects list with atomic write."""
    ensure_dirs()
    try:
        with FileLock(LOCK_FILE):
            atomic_write_json(PROJECTS_FILE, {"projects": projects})
    except TimeoutError:
        print("⚠️  Could not acquire lock for save, retrying...", file=sys.stderr)
        time.sleep(0.5)
        atomic_write_json(PROJECTS_FILE, {"projects": projects})


def create_project(name: str, description: str = "") -> Dict:
    """Create a new project."""
    try:
        with FileLock(LOCK_FILE):
            # Reload inside lock
            try:
                data = json.loads(PROJECTS_FILE.read_text())
                projects = data.get("projects", [])
            except:
                projects = []
            
            # Check if project exists
            for p in projects:
                if p["name"].lower() == name.lower():
                    return {"success": False, "error": f"Project '{name}' already exists"}
            
            project = {
                "id": f"proj-{uuid.uuid4().hex[:8]}",
                "name": name,
                "description": description,
                "created_at": datetime.now().isoformat(),
                "status": "active"
            }
            
            projects.append(project)
            atomic_write_json(PROJECTS_FILE, {"projects": projects})
            
            return {"success": True, "project": project}
        
    except TimeoutError:
        return {"success": False, "error": "Could not acquire lock - try again"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_project(project_name: str) -> Optional[Dict]:
    """Get project by name or ID."""
    projects = load_projects()
    for p in projects:
        if p["name"].lower() == project_name.lower() or p["id"] == project_name:
            return p
    return None


def load_tasks(project_id: str = None, status: str = None) -> List[Dict]:
    """Load tasks with optional filters."""
    ensure_dirs()
    
    tasks = []
    for task_file in TASKS_DIR.glob("TASK-*.json"):
        try:
            task = json.loads(task_file.read_text())
            
            # Apply filters
            if project_id and task.get("project_id") != project_id:
                continue
            if status and task.get("status") != status:
                continue
            
            tasks.append(task)
        except (json.JSONDecodeError, IOError):
            continue
    
    # Sort by priority and due date
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    tasks.sort(key=lambda x: (
        priority_order.get(x.get("priority", "medium"), 2),
        x.get("due_date", "9999-12-31")
    ))
    
    return tasks


def save_task(task: Dict):
    """Save task to file atomically."""
    ensure_dirs()
    task_file = TASKS_DIR / f"{task['id']}.json"
    atomic_write_json(task_file, task)


def create_task(title: str, project_id: str, description: str = "",
               priority: str = "medium", due_date: str = None,
               assignee: str = None, tags: List[str] = None) -> Dict:
    """Create a new task."""
    try:
        task = {
            "id": generate_task_id(),
            "title": title,
            "description": description,
            "project_id": project_id,
            "status": "todo",
            "priority": priority if priority in PRIORITIES else "medium",
            "due_date": due_date,
            "assignee": assignee,
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        save_task(task)
        
        return {"success": True, "task": task}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_task(task_id: str) -> Optional[Dict]:
    """Get task by ID."""
    task_file = TASKS_DIR / f"{task_id}.json"
    if task_file.exists():
        try:
            return json.loads(task_file.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    return None


def update_task(task_id: str, updates: Dict) -> Dict:
    """Update task fields atomically."""
    task = get_task(task_id)
    if not task:
        return {"success": False, "error": "Task not found"}
    
    # Apply updates
    for key, value in updates.items():
        if key in ["status", "priority", "title", "description", "due_date", "assignee"]:
            task[key] = value
    
    task["updated_at"] = datetime.now().isoformat()
    
    # If moved to done, record completion time
    if updates.get("status") == "done" and not task.get("completed_at"):
        task["completed_at"] = datetime.now().isoformat()
    
    save_task(task)
    
    return {"success": True, "task": task}


def move_task(task_id: str, new_status: str) -> Dict:
    """Move task to different status column."""
    if new_status not in STATUSES:
        return {"success": False, "error": f"Invalid status. Use: {', '.join(STATUSES)}"}
    
    return update_task(task_id, {"status": new_status})


def delete_task(task_id: str) -> Dict:
    """Archive a task instead of deleting."""
    task_file = TASKS_DIR / f"{task_id}.json"
    
    if not task_file.exists():
        return {"success": False, "error": "Task not found"}
    
    # Move to archive instead of deleting
    task = get_task(task_id)
    if task:
        task["status"] = "archived"
        task["updated_at"] = datetime.now().isoformat()
        save_task(task)
    
    return {"success": True, "message": "Task archived"}


def display_kanban_board(project_id: str = None):
    """Display Kanban board view."""
    tasks = load_tasks(project_id=project_id)
    
    # Group by status
    columns = {status: [] for status in STATUSES if status != "archived"}
    for task in tasks:
        status = task.get("status", "todo")
        if status in columns:
            columns[status].append(task)
    
    # Print board
    print("\n📋 Kanban Board")
    print("=" * 80)
    
    # Show project info
    if project_id:
        project = get_project(project_id)
        if project:
            print(f"Project: {project['name']}")
    
    print("")
    
    # Print columns
    for status in ["backlog", "todo", "in-progress", "review", "done"]:
        tasks_in_column = columns[status]
        count = len(tasks_in_column)
        
        icon = {
            "backlog": "📥",
            "todo": "📝",
            "in-progress": "🔄",
            "review": "👀",
            "done": "✅"
        }.get(status, "•")
        
        print(f"{icon} {status.upper().replace('-', ' ')} ({count})")
        print("-" * 78)
        
        if tasks_in_column:
            for task in tasks_in_column[:5]:  # Show first 5
                priority_icon = {
                    "critical": "🔴",
                    "high": "🟠",
                    "medium": "🟡",
                    "low": "🟢"
                }.get(task.get("priority", "medium"), "⚪")
                
                title = task['title'][:40] + "..." if len(task['title']) > 40 else task['title']
                due = task.get('due_date', 'no due')
                if due and due != 'no due':
                    due_str = f"📅 {due}"
                else:
                    due_str = ""
                
                print(f"   {priority_icon} {task['id']}: {title} {due_str}")
            
            if len(tasks_in_column) > 5:
                print(f"   ... and {len(tasks_in_column) - 5} more")
        else:
            print("   (empty)")
        
        print("")


def display_task_list(tasks: List[Dict], title: str = "Tasks"):
    """Display task list view."""
    if not tasks:
        print(f"\nNo {title.lower()} found.")
        return
    
    print(f"\n📋 {title} ({len(tasks)})")
    print("-" * 80)
    print(f"{'ID':<15} {'Status':<12} {'Priority':<10} {'Due':<12} {'Title':<30}")
    print("-" * 80)
    
    for task in tasks[:20]:  # Limit to 20
        task_id = task['id']
        status = task.get('status', 'todo')[:10]
        priority = task.get('priority', 'medium')[:8]
        due = task.get('due_date', '-')[:10]
        title_display = task['title'][:28]
        
        print(f"{task_id:<15} {status:<12} {priority:<10} {due:<12} {title_display:<30}")
    
    if len(tasks) > 20:
        print(f"\n... and {len(tasks) - 20} more tasks")
    
    print("-" * 80)


def display_task_detail(task_id: str):
    """Display full task details."""
    task = get_task(task_id)
    
    if not task:
        print(f"❌ Task {task_id} not found")
        return
    
    print("\n📋 Task Details")
    print("=" * 60)
    print(f"ID: {task['id']}")
    print(f"Title: {task['title']}")
    print(f"Status: {task['status']}")
    print(f"Priority: {task['priority']}")
    
    if task.get('description'):
        print(f"\nDescription:\n{task['description']}")
    
    if task.get('due_date'):
        print(f"\nDue Date: {task['due_date']}")
    
    if task.get('assignee'):
        print(f"Assignee: {task['assignee']}")
    
    if task.get('tags'):
        print(f"Tags: {', '.join(task['tags'])}")
    
    print(f"\nCreated: {task['created_at'][:19]}")
    print(f"Updated: {task['updated_at'][:19]}")
    
    if task.get('completed_at'):
        print(f"Completed: {task['completed_at'][:19]}")


def show_statistics(project_id: str = None):
    """Show project/task statistics."""
    tasks = load_tasks(project_id=project_id)
    
    if not tasks:
        print("\nNo tasks found.")
        return
    
    # Calculate stats
    total = len(tasks)
    
    by_status = {}
    for status in STATUSES:
        count = len([t for t in tasks if t.get("status") == status])
        if count > 0:
            by_status[status] = count
    
    by_priority = {}
    for priority in PRIORITIES:
        count = len([t for t in tasks if t.get("priority") == priority])
        if count > 0:
            by_priority[priority] = count
    
    completed = len([t for t in tasks if t.get("status") == "done"])
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    # Due soon
    today = datetime.now().date()
    due_soon = len([t for t in tasks if t.get("due_date") and 
                    datetime.fromisoformat(t["due_date"]).date() <= today + timedelta(days=3) and
                    t.get("status") not in ["done", "archived"]])
    
    overdue = len([t for t in tasks if t.get("due_date") and
                   datetime.fromisoformat(t["due_date"]).date() < today and
                   t.get("status") not in ["done", "archived"]])
    
    print("\n📊 Task Statistics")
    print("=" * 40)
    
    if project_id:
        project = get_project(project_id)
        if project:
            print(f"Project: {project['name']}")
    
    print(f"\nTotal Tasks: {total}")
    print(f"Completed: {completed} ({completion_rate:.1f}%)")
    print(f"Due Soon (≤3 days): {due_soon}")
    
    if overdue > 0:
        print(f"⚠️  Overdue: {overdue}")
    
    print("\nBy Status:")
    for status, count in by_status.items():
        print(f"  {status}: {count}")
    
    print("\nBy Priority:")
    for priority in ["critical", "high", "medium", "low"]:
        if priority in by_priority:
            print(f"  {priority}: {by_priority[priority]}")


def interactive_add_task():
    """Interactive task creation."""
    print("\n➕ Add New Task")
    print("-" * 40)
    
    # Get project
    projects = load_projects()
    if projects:
        print("\nAvailable projects:")
        for i, p in enumerate(projects, 1):
            print(f"  {i}. {p['name']}")
        print("  0. Create new project")
    else:
        print("\nNo projects exist. Creating new...")
    
    project_choice = input("\nSelect project (number or name): ").strip()
    
    if project_choice == "0" or not projects:
        project_name = input("New project name: ").strip()
        result = create_project(project_name)
        if result["success"]:
            project_id = result["project"]["id"]
            print(f"✅ Created project: {project_name}")
        else:
            print(f"❌ {result['error']}")
            return {"success": False, "error": result['error']}
    else:
        # Try to find by number or name
        try:
            idx = int(project_choice) - 1
            if 0 <= idx < len(projects):
                project_id = projects[idx]["id"]
            else:
                # Try by name
                project = get_project(project_choice)
                if project:
                    project_id = project["id"]
                else:
                    print("❌ Project not found")
                    return {"success": False, "error": "Project not found"}
        except ValueError:
            project = get_project(project_choice)
            if project:
                project_id = project["id"]
            else:
                print("❌ Project not found")
                return {"success": False, "error": "Project not found"}
    
    # Get task details
    title = input("\nTask title: ").strip()
    if not title:
        print("❌ Title required")
        return {"success": False, "error": "Title required"}
    
    description = input("Description (optional): ").strip()
    
    print("\nPriority:")
    print("  1. Low")
    print("  2. Medium")
    print("  3. High")
    print("  4. Critical")
    
    priority_choice = input("Choice [2]: ").strip() or "2"
    priorities = {"1": "low", "2": "medium", "3": "high", "4": "critical"}
    priority = priorities.get(priority_choice, "medium")
    
    due_date = input("Due date (YYYY-MM-DD, optional): ").strip() or None
    
    assignee = input("Assignee (optional): ").strip() or None
    
    tags_str = input("Tags (comma-separated, optional): ").strip()
    tags = [t.strip() for t in tags_str.split(",")] if tags_str else None
    
    return create_task(title, project_id, description, priority, due_date, assignee, tags)


def show_help():
    """Show help message."""
    print("""📋 Task/Project Manager

Kanban-style task and project management.

Commands:
  project add "Name" [desc]     Create new project
  project list                  List all projects
  task add "Title"               Add task (interactive)
  task show TASK-ID             Show task details
  task edit TASK-ID             Edit task
  task move TASK-ID --to STATUS Move task to column
  task delete TASK-ID           Archive task
  board [--project NAME]        Show Kanban board
  list [--status STATUS]        List all tasks
  stats [--project NAME]        Show statistics
  help                          Show this help

Status columns: backlog, todo, in-progress, review, done

Examples:
  smf run task-manager project add "Website Redesign"
  smf run task-manager task add "Fix navigation" --project website --priority high
  smf run task-manager board --project website
  smf run task-manager task move TASK-ABC123 --to done
  smf run task-manager stats

Options for task add:
  --project PROJECT    Assign to project
  --priority LEVEL     low/medium/high/critical
  --due YYYY-MM-DD     Due date
  --assignee NAME      Assign to person
  --tags TAGS          Comma-separated tags
""")


def main():
    """CLI entry point."""
    # Check for test mode
    if "--test-mode" in sys.argv:
        sys.argv.remove("--test-mode")
        print("🔧 TEST MODE: Subscription check skipped")
        subscription = {"valid": True, "tier": "test"}
    else:
        # Check subscription
        subscription = require_subscription(SKILL_NAME, MIN_TIER)
        
        if not subscription["valid"]:
            show_subscription_error(subscription)
            return 1
        
        print(f"📋 Task/Project Manager")
        print(f"   Subscription: {subscription['tier']}")
        print("")
    
    # Parse command
    if len(sys.argv) < 2:
        show_help()
        return 0
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "project":
        if len(args) < 1:
            print("❌ Project command required (add, list)")
            return 1
        
        subcommand = args[0]
        
        if subcommand == "add":
            if len(args) < 2:
                print("❌ Project name required")
                return 1
            
            name = args[1]
            description = args[2] if len(args) > 2 else ""
            
            result = create_project(name, description)
            
            if result["success"]:
                print(f"✅ Project created: {result['project']['name']}")
                print(f"   ID: {result['project']['id']}")
            else:
                print(f"❌ {result['error']}")
                return 1
        
        elif subcommand == "list":
            projects = load_projects()
            
            if not projects:
                print("No projects found.")
                return 0
            
            print(f"\n📁 {len(projects)} Project(s)")
            print("-" * 60)
            
            for p in projects:
                status_icon = "✅" if p.get("status") == "active" else "⏸️"
                print(f"{status_icon} {p['name']}")
                if p.get('description'):
                    print(f"   {p['description'][:50]}")
        
        else:
            print(f"Unknown project command: {subcommand}")
            return 1
    
    elif command == "task":
        if len(args) < 1:
            print("❌ Task command required (add, show, edit, move, delete)")
            return 1
        
        subcommand = args[0]
        
        if subcommand == "add":
            if len(args) > 1 and not args[1].startswith("--"):
                # Command line mode: task add "Title" --project X --priority Y
                title = args[1]
                
                # Parse options
                project_name = None
                priority = "medium"
                due_date = None
                assignee = None
                tags = None
                description = ""
                
                i = 2
                while i < len(args):
                    if args[i] == "--project" and i + 1 < len(args):
                        project_name = args[i + 1]
                        i += 2
                    elif args[i] == "--priority" and i + 1 < len(args):
                        priority = args[i + 1]
                        i += 2
                    elif args[i] == "--due" and i + 1 < len(args):
                        due_date = args[i + 1]
                        i += 2
                    elif args[i] == "--assignee" and i + 1 < len(args):
                        assignee = args[i + 1]
                        i += 2
                    elif args[i] == "--tags" and i + 1 < len(args):
                        tags = args[i + 1].split(",")
                        i += 2
                    elif args[i] == "--description" and i + 1 < len(args):
                        description = args[i + 1]
                        i += 2
                    else:
                        i += 1
                
                # Find project
                if project_name:
                    project = get_project(project_name)
                    if project:
                        project_id = project["id"]
                    else:
                        print(f"❌ Project not found: {project_name}")
                        return 1
                else:
                    # Use first project
                    projects = load_projects()
                    if projects:
                        project_id = projects[0]["id"]
                    else:
                        print("❌ No projects exist. Create one first.")
                        return 1
                
                result = create_task(title, project_id, description, priority, due_date, assignee, tags)
            else:
                # Interactive mode
                result = interactive_add_task()
            
            if result["success"]:
                print(f"✅ Task created: {result['task']['id']}")
                print(f"   Title: {result['task']['title']}")
                print(f"   Status: {result['task']['status']}")
                print(f"\nView: smf run task-manager task show {result['task']['id']}")
            else:
                print(f"❌ {result['error']}")
                return 1
        
        elif subcommand == "show":
            if len(args) < 2:
                print("❌ Task ID required")
                return 1
            
            display_task_detail(args[1])
        
        elif subcommand == "move":
            if len(args) < 2:
                print("❌ Task ID required")
                return 1
            
            task_id = args[1]
            
            # Find --to flag
            new_status = None
            if "--to" in args:
                idx = args.index("--to")
                if idx + 1 < len(args):
                    new_status = args[idx + 1]
            
            if not new_status:
                print("❌ --to STATUS required")
                print(f"   Valid statuses: {', '.join(STATUSES)}")
                return 1
            
            result = move_task(task_id, new_status)
            
            if result["success"]:
                print(f"✅ Task moved to {new_status}")
            else:
                print(f"❌ {result['error']}")
                return 1
        
        elif subcommand == "delete":
            if len(args) < 2:
                print("❌ Task ID required")
                return 1
            
            result = delete_task(args[1])
            
            if result["success"]:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['error']}")
                return 1
        
        else:
            print(f"Unknown task command: {subcommand}")
            return 1
    
    elif command == "board":
        project_name = None
        if "--project" in args:
            idx = args.index("--project")
            if idx + 1 < len(args):
                project_name = args[idx + 1]
        
        project_id = None
        if project_name:
            project = get_project(project_name)
            if project:
                project_id = project["id"]
            else:
                print(f"❌ Project not found: {project_name}")
                return 1
        
        display_kanban_board(project_id)
    
    elif command == "list":
        status_filter = None
        if "--status" in args:
            idx = args.index("--status")
            if idx + 1 < len(args):
                status_filter = args[idx + 1]
        
        tasks = load_tasks(status=status_filter)
        display_task_list(tasks, f"Tasks")
    
    elif command == "stats":
        project_name = None
        if "--project" in args:
            idx = args.index("--project")
            if idx + 1 < len(args):
                project_name = args[idx + 1]
        
        project_id = None
        if project_name:
            project = get_project(project_name)
            if project:
                project_id = project["id"]
            else:
                print(f"❌ Project not found: {project_name}")
                return 1
        
        show_statistics(project_id)
    
    elif command in ("help", "--help", "-h"):
        show_help()
    
    else:
        print(f"Unknown command: {command}")
        print("Run 'smf run task-manager help' for usage.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
