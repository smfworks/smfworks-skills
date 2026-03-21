#!/usr/bin/env python3
"""
Self-Improvement Skill - SMF Works Pro Skill
Log learnings, errors, and insights for continuous improvement.
Coding agents can process these into fixes and promote important items to project memory.

Usage:
    smf run self-improvement log-error "File not found" --context "Reading config" --severity high --tags "file-io,config"
    smf run self-improvement log-learning "Always check file exists first" --category "best-practice"
    smf run self-improvement list --category errors
    smf run self-improvement search "config"
    smf run self-improvement promote ITEM-ID --to-project-memory
"""

import sys
import json
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Add shared auth to path
shared_path = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from smf_auth import require_subscription, show_subscription_error

# Skill configuration
SKILL_NAME = "self-improvement"
MIN_TIER = "pro"
LOGS_DIR = Path.home() / ".smf" / "improvement"
ERRORS_DIR = LOGS_DIR / "errors"
LEARNINGS_DIR = LOGS_DIR / "learnings"
INSIGHTS_DIR = LOGS_DIR / "insights"
MEMORY_FILE = LOGS_DIR / "promoted.md"

# Severity levels
SEVERITIES = ["low", "medium", "high", "critical"]

# Categories
ERROR_CATEGORIES = ["file-io", "network", "config", "logic", "syntax", "runtime", "other"]
LEARNING_CATEGORIES = ["best-practice", "pattern", "anti-pattern", "optimization", "architecture", "other"]


def ensure_dirs():
    """Ensure log directories exist."""
    ERRORS_DIR.mkdir(parents=True, exist_ok=True)
    LEARNINGS_DIR.mkdir(parents=True, exist_ok=True)
    INSIGHTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def generate_item_id(prefix: str = "ITEM") -> str:
    """Generate unique item ID."""
    timestamp = datetime.now().strftime("%Y%m%d")
    unique = uuid.uuid4().hex[:6].upper()
    return f"{prefix}-{timestamp}-{unique}"


def log_error(description: str, context: str = "", severity: str = "medium",
              tags: List[str] = None, resolution: str = "", prevention: str = "") -> Dict:
    """Log an error for analysis and improvement."""
    try:
        ensure_dirs()
        
        item_id = generate_item_id("ERR")
        
        error_data = {
            "id": item_id,
            "type": "error",
            "description": description,
            "context": context,
            "severity": severity if severity in SEVERITIES else "medium",
            "tags": tags or [],
            "resolution": resolution,
            "prevention": prevention,
            "status": "open",
            "occurrences": 1,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "resolved_at": None
        }
        
        # Save as JSON
        json_file = ERRORS_DIR / f"{item_id}.json"
        json_file.write_text(json.dumps(error_data, indent=2))
        
        # Also append to daily markdown log
        md_file = ERRORS_DIR / f"errors-{datetime.now().strftime('%Y-%m-%d')}.md"
        with open(md_file, 'a') as f:
            f.write(f"\n## {item_id}\n\n")
            f.write(f"**Error:** {description}\n\n")
            f.write(f"**Context:** {context}\n\n")
            f.write(f"**Severity:** {severity}\n\n")
            f.write(f"**Tags:** {', '.join(tags) if tags else 'None'}\n\n")
            f.write(f"**Timestamp:** {datetime.now().isoformat()}\n\n")
            f.write("---\n")
        
        return {"success": True, "item_id": item_id, "file": str(json_file)}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def log_learning(insight: str, category: str = "best-practice", 
                 context: str = "", tags: List[str] = None,
                 related_errors: List[str] = None) -> Dict:
    """Log a learning or insight."""
    try:
        ensure_dirs()
        
        item_id = generate_item_id("LRN")
        
        learning_data = {
            "id": item_id,
            "type": "learning",
            "insight": insight,
            "category": category if category in LEARNING_CATEGORIES else "other",
            "context": context,
            "tags": tags or [],
            "related_errors": related_errors or [],
            "promoted": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save as JSON
        json_file = LEARNINGS_DIR / f"{item_id}.json"
        json_file.write_text(json.dumps(learning_data, indent=2))
        
        # Also append to daily markdown log
        md_file = LEARNINGS_DIR / f"learnings-{datetime.now().strftime('%Y-%m-%d')}.md"
        with open(md_file, 'a') as f:
            f.write(f"\n## {item_id}\n\n")
            f.write(f"**Insight:** {insight}\n\n")
            f.write(f"**Category:** {category}\n\n")
            f.write(f"**Context:** {context}\n\n")
            f.write(f"**Tags:** {', '.join(tags) if tags else 'None'}\n\n")
            f.write(f"**Timestamp:** {datetime.now().isoformat()}\n\n")
            f.write("---\n")
        
        return {"success": True, "item_id": item_id, "file": str(json_file)}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def log_insight(title: str, description: str, impact: str = "medium",
                tags: List[str] = None) -> Dict:
    """Log a general insight or observation."""
    try:
        ensure_dirs()
        
        item_id = generate_item_id("INS")
        
        insight_data = {
            "id": item_id,
            "type": "insight",
            "title": title,
            "description": description,
            "impact": impact,
            "tags": tags or [],
            "promoted": False,
            "created_at": datetime.now().isoformat()
        }
        
        json_file = INSIGHTS_DIR / f"{item_id}.json"
        json_file.write_text(json.dumps(insight_data, indent=2))
        
        return {"success": True, "item_id": item_id}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def load_items(item_type: str = None, status: str = None, 
               category: str = None, tags: List[str] = None) -> List[Dict]:
    """Load logged items with filters."""
    ensure_dirs()
    
    items = []
    
    # Determine which directories to search
    if item_type == "error":
        dirs = [ERRORS_DIR]
    elif item_type == "learning":
        dirs = [LEARNINGS_DIR]
    elif item_type == "insight":
        dirs = [INSIGHTS_DIR]
    else:
        dirs = [ERRORS_DIR, LEARNINGS_DIR, INSIGHTS_DIR]
    
    for directory in dirs:
        if not directory.exists():
            continue
        
        for json_file in directory.glob("*.json"):
            try:
                item = json.loads(json_file.read_text())
                
                # Apply filters
                if status and item.get("status") != status:
                    continue
                if category:
                    if item.get("category") != category:
                        continue
                if tags:
                    item_tags = set(item.get("tags", []))
                    if not any(tag in item_tags for tag in tags):
                        continue
                
                items.append(item)
            except:
                continue
    
    # Sort by date (newest first)
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return items


def get_item(item_id: str) -> Optional[Dict]:
    """Get specific item by ID."""
    # Search in all directories
    for directory in [ERRORS_DIR, LEARNINGS_DIR, INSIGHTS_DIR]:
        json_file = directory / f"{item_id}.json"
        if json_file.exists():
            try:
                return json.loads(json_file.read_text())
            except:
                continue
    return None


def update_item(item_id: str, updates: Dict) -> Dict:
    """Update an item."""
    item = get_item(item_id)
    if not item:
        return {"success": False, "error": "Item not found"}
    
    # Apply updates
    for key, value in updates.items():
        if key in ["status", "resolution", "prevention", "promoted"]:
            item[key] = value
    
    item["updated_at"] = datetime.now().isoformat()
    
    # If resolving error
    if updates.get("status") == "resolved" and not item.get("resolved_at"):
        item["resolved_at"] = datetime.now().isoformat()
    
    # Save back
    item_type = item.get("type")
    if item_type == "error":
        directory = ERRORS_DIR
    elif item_type == "learning":
        directory = LEARNINGS_DIR
    else:
        directory = INSIGHTS_DIR
    
    json_file = directory / f"{item_id}.json"
    json_file.write_text(json.dumps(item, indent=2))
    
    return {"success": True, "item": item}


def promote_to_memory(item_id: str, notes: str = "") -> Dict:
    """Promote an item to project memory."""
    item = get_item(item_id)
    if not item:
        return {"success": False, "error": "Item not found"}
    
    try:
        ensure_dirs()
        
        # Build memory entry
        if item["type"] == "error":
            memory_entry = f"""
## {item_id} - Error Pattern

**Error:** {item['description']}

**Context:** {item['context']}

**Resolution:** {item.get('resolution', 'Not resolved yet')}

**Prevention:** {item.get('prevention', 'No prevention strategy')}

**Tags:** {', '.join(item.get('tags', []))}

**Promoted:** {datetime.now().isoformat()}
{notes and f"**Notes:** {notes}" or ""}

---
"""
        elif item["type"] == "learning":
            memory_entry = f"""
## {item_id} - Learning

**Insight:** {item['insight']}

**Category:** {item.get('category', 'general')}

**Context:** {item.get('context', '')}

**Tags:** {', '.join(item.get('tags', []))}

**Promoted:** {datetime.now().isoformat()}
{notes and f"**Notes:** {notes}" or ""}

---
"""
        else:
            memory_entry = f"""
## {item_id} - Insight

**Title:** {item.get('title', '')}

**Description:** {item['description']}

**Promoted:** {datetime.now().isoformat()}

---
"""
        
        # Append to memory file
        with open(MEMORY_FILE, 'a') as f:
            f.write(memory_entry)
        
        # Mark item as promoted
        update_item(item_id, {"promoted": True})
        
        return {"success": True, "memory_file": str(MEMORY_FILE)}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def search_items(query: str, item_type: str = None) -> List[Dict]:
    """Search items by text."""
    items = load_items(item_type=item_type)
    query_lower = query.lower()
    
    results = []
    for item in items:
        # Search in various fields
        searchable_text = ""
        if item["type"] == "error":
            searchable_text = f"{item.get('description', '')} {item.get('context', '')}"
        elif item["type"] == "learning":
            searchable_text = f"{item.get('insight', '')} {item.get('context', '')}"
        else:
            searchable_text = f"{item.get('title', '')} {item.get('description', '')}"
        
        # Also search tags
        searchable_text += " " + " ".join(item.get("tags", []))
        
        if query_lower in searchable_text.lower():
            results.append(item)
    
    return results


def get_statistics() -> Dict:
    """Get logging statistics."""
    errors = load_items(item_type="error")
    learnings = load_items(item_type="learning")
    insights = load_items(item_type="insight")
    
    # Error stats
    open_errors = len([e for e in errors if e.get("status") == "open"])
    resolved_errors = len([e for e in errors if e.get("status") == "resolved"])
    
    by_severity = {}
    for severity in SEVERITIES:
        count = len([e for e in errors if e.get("severity") == severity])
        if count > 0:
            by_severity[severity] = count
    
    # Learning stats
    by_category = {}
    for category in LEARNING_CATEGORIES:
        count = len([l for l in learnings if l.get("category") == category])
        if count > 0:
            by_category[category] = count
    
    # Recent activity
    week_ago = datetime.now() - timedelta(days=7)
    recent_errors = len([e for e in errors if datetime.fromisoformat(e.get("created_at", "2000-01-01")) > week_ago])
    recent_learnings = len([l for l in learnings if datetime.fromisoformat(l.get("created_at", "2000-01-01")) > week_ago])
    
    return {
        "total_errors": len(errors),
        "open_errors": open_errors,
        "resolved_errors": resolved_errors,
        "total_learnings": len(learnings),
        "total_insights": len(insights),
        "by_severity": by_severity,
        "by_category": by_category,
        "recent_errors": recent_errors,
        "recent_learnings": recent_learnings
    }


def display_items(items: List[Dict], title: str = "Items"):
    """Display items in formatted list."""
    if not items:
        print(f"\nNo {title.lower()} found.")
        return
    
    print(f"\n📋 {title} ({len(items)})")
    print("-" * 90)
    print(f"{'ID':<20} {'Type':<10} {'Status/Cat':<15} {'Date':<12} {'Summary':<30}")
    print("-" * 90)
    
    for item in items[:20]:
        item_id = item['id']
        item_type = item.get('type', 'unknown')[:9]
        
        if item_type == "error":
            status_sev = f"{item.get('status', 'open')}/{item.get('severity', 'medium')}"
        else:
            status_sev = item.get('category', 'general')[:14]
        
        date = item.get('created_at', '')[:10]
        
        # Summary
        if item_type == "error":
            summary = item.get('description', '')[:28]
        elif item_type == "learning":
            summary = item.get('insight', '')[:28]
        else:
            summary = item.get('title', '')[:28]
        
        print(f"{item_id:<20} {item_type:<10} {status_sev:<15} {date:<12} {summary:<30}")
    
    if len(items) > 20:
        print(f"\n... and {len(items) - 20} more")
    
    print("-" * 90)


def display_statistics():
    """Display statistics view."""
    stats = get_statistics()
    
    print("\n📊 Self-Improvement Statistics")
    print("=" * 50)
    
    print(f"\n📈 Totals:")
    print(f"   Errors: {stats['total_errors']} ({stats['open_errors']} open, {stats['resolved_errors']} resolved)")
    print(f"   Learnings: {stats['total_learnings']}")
    print(f"   Insights: {stats['total_insights']}")
    
    print(f"\n📅 This Week:")
    print(f"   New errors: {stats['recent_errors']}")
    print(f"   New learnings: {stats['recent_learnings']}")
    
    if stats['by_severity']:
        print(f"\n🔥 Errors by Severity:")
        for severity, count in stats['by_severity'].items():
            icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(severity, "⚪")
            print(f"   {icon} {severity}: {count}")
    
    if stats['by_category']:
        print(f"\n💡 Learnings by Category:")
        for category, count in stats['by_category'].items():
            print(f"   • {category}: {count}")


def interactive_log_error():
    """Interactive error logging."""
    print("\n🐛 Log Error")
    print("-" * 40)
    
    description = input("Error description: ").strip()
    if not description:
        print("❌ Description required")
        return {"success": False, "error": "Description required"}
    
    context = input("Context (what were you doing?): ").strip()
    
    print("\nSeverity:")
    print("  1. Low (minor inconvenience)")
    print("  2. Medium (caused delay)")
    print("  3. High (significant blocker)")
    print("  4. Critical (system down/data loss)")
    
    severity_choice = input("Choice [2]: ").strip() or "2"
    severities = {"1": "low", "2": "medium", "3": "high", "4": "critical"}
    severity = severities.get(severity_choice, "medium")
    
    tags_str = input("Tags (comma-separated): ").strip()
    tags = [t.strip() for t in tags_str.split(",")] if tags_str else []
    
    resolution = input("Resolution (if known): ").strip()
    prevention = input("How to prevent in future: ").strip()
    
    return log_error(description, context, severity, tags, resolution, prevention)


def interactive_log_learning():
    """Interactive learning logging."""
    print("\n💡 Log Learning")
    print("-" * 40)
    
    insight = input("What did you learn? ").strip()
    if not insight:
        print("❌ Learning required")
        return {"success": False, "error": "Learning required"}
    
    print("\nCategory:")
    print("  1. Best Practice")
    print("  2. Pattern")
    print("  3. Anti-pattern")
    print("  4. Optimization")
    print("  5. Architecture")
    print("  6. Other")
    
    cat_choice = input("Choice [1]: ").strip() or "1"
    categories = {"1": "best-practice", "2": "pattern", "3": "anti-pattern", 
                  "4": "optimization", "5": "architecture", "6": "other"}
    category = categories.get(cat_choice, "best-practice")
    
    context = input("Context (when does this apply?): ").strip()
    
    tags_str = input("Tags (comma-separated): ").strip()
    tags = [t.strip() for t in tags_str.split(",")] if tags_str else []
    
    return log_learning(insight, category, context, tags)


def show_help():
    """Show help message."""
    print("""🧠 Self-Improvement Skill

Log errors, learnings, and insights for continuous improvement.

Commands:
  log-error "desc"           Log an error
  log-learning "insight"     Log a learning
  log-insight "title"        Log an insight
  list                       List all items
  list --category errors     List by category
  search "query"             Search items
  show ITEM-ID               Show item details
  promote ITEM-ID            Promote to project memory
  update ITEM-ID             Update item status
  stats                      Show statistics
  help                       Show this help

Examples:
  smf run self-improvement log-error "File not found" --context "Reading config" --severity high
  smf run self-improvement log-learning "Always validate JSON" --category best-practice
  smf run self-improvement list --category errors
  smf run self-improvement search "config"
  smf run self-improvement promote ERR-20260320-ABC123

Categories:
  Error: file-io, network, config, logic, syntax, runtime
  Learning: best-practice, pattern, anti-pattern, optimization, architecture

Storage:
  ~/.smf/improvement/errors/
  ~/.smf/improvement/learnings/
  ~/.smf/improvement/insights/
  ~/.smf/improvement/promoted.md (memory file)
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
        
        print(f"🧠 Self-Improvement Skill")
        print(f"   Subscription: {subscription['tier']}")
        print("")
    
    # Parse command
    if len(sys.argv) < 2:
        show_help()
        return 0
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "log-error":
        if len(args) < 1:
            result = interactive_log_error()
        else:
            # Parse command line args
            description = args[0]
            context = ""
            severity = "medium"
            tags = []
            resolution = ""
            prevention = ""
            
            i = 1
            while i < len(args):
                if args[i] == "--context" and i + 1 < len(args):
                    context = args[i + 1]
                    i += 2
                elif args[i] == "--severity" and i + 1 < len(args):
                    severity = args[i + 1]
                    i += 2
                elif args[i] == "--tags" and i + 1 < len(args):
                    tags = args[i + 1].split(",")
                    i += 2
                elif args[i] == "--resolution" and i + 1 < len(args):
                    resolution = args[i + 1]
                    i += 2
                elif args[i] == "--prevention" and i + 1 < len(args):
                    prevention = args[i + 1]
                    i += 2
                else:
                    i += 1
            
            result = log_error(description, context, severity, tags, resolution, prevention)
        
        if result["success"]:
            print(f"✅ Error logged: {result['item_id']}")
        else:
            print(f"❌ Failed: {result.get('error')}")
            return 1
    
    elif command == "log-learning":
        if len(args) < 1:
            result = interactive_log_learning()
        else:
            insight = args[0]
            category = "best-practice"
            context = ""
            tags = []
            
            i = 1
            while i < len(args):
                if args[i] == "--category" and i + 1 < len(args):
                    category = args[i + 1]
                    i += 2
                elif args[i] == "--context" and i + 1 < len(args):
                    context = args[i + 1]
                    i += 2
                elif args[i] == "--tags" and i + 1 < len(args):
                    tags = args[i + 1].split(",")
                    i += 2
                else:
                    i += 1
            
            result = log_learning(insight, category, context, tags)
        
        if result["success"]:
            print(f"✅ Learning logged: {result['item_id']}")
        else:
            print(f"❌ Failed: {result.get('error')}")
            return 1
    
    elif command == "log-insight":
        if len(args) < 2:
            print("❌ Usage: log-insight \"Title\" \"Description\"")
            return 1
        
        title = args[0]
        description = args[1]
        
        result = log_insight(title, description)
        
        if result["success"]:
            print(f"✅ Insight logged: {result['item_id']}")
        else:
            print(f"❌ Failed: {result.get('error')}")
            return 1
    
    elif command == "list":
        item_type = None
        status = None
        category = None
        tags = None
        
        i = 0
        while i < len(args):
            if args[i] == "--type" and i + 1 < len(args):
                item_type = args[i + 1]
                i += 2
            elif args[i] == "--status" and i + 1 < len(args):
                status = args[i + 1]
                i += 2
            elif args[i] == "--category" and i + 1 < len(args):
                category = args[i + 1]
                i += 2
            elif args[i] == "--tags" and i + 1 < len(args):
                tags = args[i + 1].split(",")
                i += 2
            else:
                i += 1
        
        items = load_items(item_type=item_type, status=status, category=category, tags=tags)
        
        title = "Items"
        if item_type:
            title = f"{item_type.title()}s"
        if category:
            title += f" ({category})"
        
        display_items(items, title)
    
    elif command == "search":
        if len(args) < 1:
            print("❌ Search query required")
            return 1
        
        query = args[0]
        item_type = None
        
        if "--type" in args:
            idx = args.index("--type")
            if idx + 1 < len(args):
                item_type = args[idx + 1]
        
        results = search_items(query, item_type)
        
        print(f"\n🔍 Search results for \"{query}\": {len(results)} found")
        display_items(results, "Search Results")
    
    elif command == "show":
        if len(args) < 1:
            print("❌ Item ID required")
            return 1
        
        item_id = args[0]
        item = get_item(item_id)
        
        if not item:
            print(f"❌ Item {item_id} not found")
            return 1
        
        print(f"\n📋 {item['type'].title()} Details")
        print("=" * 60)
        print(f"ID: {item['id']}")
        print(f"Type: {item['type']}")
        print(f"Created: {item['created_at']}")
        
        if item["type"] == "error":
            print(f"\nDescription: {item['description']}")
            print(f"Context: {item.get('context', 'N/A')}")
            print(f"Severity: {item.get('severity', 'medium')}")
            print(f"Status: {item.get('status', 'open')}")
            print(f"Tags: {', '.join(item.get('tags', [])) or 'None'}")
            
            if item.get('resolution'):
                print(f"\nResolution: {item['resolution']}")
            if item.get('prevention'):
                print(f"Prevention: {item['prevention']}")
        
        elif item["type"] == "learning":
            print(f"\nInsight: {item['insight']}")
            print(f"Category: {item.get('category', 'general')}")
            print(f"Context: {item.get('context', 'N/A')}")
            print(f"Tags: {', '.join(item.get('tags', [])) or 'None'}")
            
            if item.get('related_errors'):
                print(f"Related Errors: {', '.join(item['related_errors'])}")
        
        else:  # insight
            print(f"\nTitle: {item.get('title', '')}")
            print(f"Description: {item['description']}")
    
    elif command == "promote":
        if len(args) < 1:
            print("❌ Item ID required")
            return 1
        
        item_id = args[0]
        notes = ""
        
        if "--notes" in args:
            idx = args.index("--notes")
            if idx + 1 < len(args):
                notes = args[idx + 1]
        
        result = promote_to_memory(item_id, notes)
        
        if result["success"]:
            print(f"✅ Item promoted to memory: {result['memory_file']}")
        else:
            print(f"❌ Failed: {result.get('error')}")
            return 1
    
    elif command == "update":
        if len(args) < 1:
            print("❌ Item ID required")
            return 1
        
        item_id = args[0]
        updates = {}
        
        if "--status" in args:
            idx = args.index("--status")
            if idx + 1 < len(args):
                updates["status"] = args[idx + 1]
        
        if "--resolution" in args:
            idx = args.index("--resolution")
            if idx + 1 < len(args):
                updates["resolution"] = args[idx + 1]
        
        if not updates:
            print("❌ No updates specified")
            return 1
        
        result = update_item(item_id, updates)
        
        if result["success"]:
            print(f"✅ Item updated")
        else:
            print(f"❌ Failed: {result.get('error')}")
            return 1
    
    elif command == "stats":
        display_statistics()
    
    elif command in ("help", "--help", "-h"):
        show_help()
    
    else:
        print(f"Unknown command: {command}")
        print("Run 'smf run self-improvement help' for usage.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
