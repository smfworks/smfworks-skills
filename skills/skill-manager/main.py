#!/usr/bin/env python3
"""
Skill Manager - SMF Works Free Skill
Visual tool for managing installed OpenClaw skills.

View, backup, and cleanly remove skills with an interactive terminal UI.
"""

import os
import sys
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Optional rich import - graceful fallback
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Confirm, Prompt
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Configuration
SMF_DIR = Path.home() / ".smf"
SKILLS_DIR = SMF_DIR / "skills"
CONFIG_DIR = Path.home() / ".config" / "smf" / "skills"
BIN_DIR = Path.home() / ".local" / "bin"

# Fallback console
if RICH_AVAILABLE:
    console = Console()
else:
    class FallbackConsole:
        def print(self, text):
            print(text)
        def clear(self):
            os.system('clear' if os.name != 'nt' else 'cls')
    console = FallbackConsole()


def get_skill_info(skill_path: Path) -> Dict:
    """Extract metadata from an installed skill."""
    info = {
        "name": skill_path.name,
        "path": str(skill_path),
        "installed_date": None,
        "size_mb": 0,
        "has_config": False,
        "is_pro": False,
        "description": "No description available",
        "tier": "unknown"
    }
    
    # Check for main.py
    main_file = skill_path / "main.py"
    if main_file.exists():
        stat = main_file.stat()
        info["installed_date"] = datetime.fromtimestamp(stat.st_mtime)
    
    # Calculate size
    try:
        total_size = sum(f.stat().st_size for f in skill_path.rglob('*') if f.is_file())
        info["size_mb"] = round(total_size / (1024 * 1024), 2)
    except:
        pass
    
    # Check for config
    config_path = CONFIG_DIR / skill_path.name / "config.json"
    info["has_config"] = config_path.exists()
    
    # Try to read README for description
    readme_path = skill_path / "README.md"
    if readme_path.exists():
        try:
            content = readme_path.read_text()
            lines = content.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    info["description"] = line[:80] + "..." if len(line) > 80 else line
                    break
        except:
            pass
    
    # Detect tier from code
    try:
        main_content = main_file.read_text()
        if "require_subscription" in main_content:
            info["is_pro"] = True
            info["tier"] = "Pro"
        else:
            info["tier"] = "Free"
    except:
        pass
    
    return info


def get_installed_skills() -> List[Dict]:
    """Get list of installed skills with metadata."""
    skills = []
    
    if not SKILLS_DIR.exists():
        return skills
    
    for skill_dir in SKILLS_DIR.iterdir():
        if skill_dir.is_dir() and (skill_dir / "main.py").exists():
            info = get_skill_info(skill_dir)
            skills.append(info)
    
    # Sort by name
    skills.sort(key=lambda x: x["name"])
    return skills


def display_skills_table(skills: List[Dict], selected: set = None):
    """Display skills in a rich table."""
    if selected is None:
        selected = set()
    
    if not RICH_AVAILABLE:
        # Fallback text table
        print("\n" + "=" * 80)
        print(f"{'Name':<25} {'Tier':<8} {'Size':<10} {'Config':<8} {'Description'}")
        print("=" * 80)
        for skill in skills:
            marker = "[✓]" if skill["name"] in selected else "[ ]"
            size = f"{skill['size_mb']:.1f} MB"
            config = "Yes" if skill["has_config"] else "No"
            print(f"{marker} {skill['name']:<20} {skill['tier']:<8} {size:<10} {config:<8} {skill['description'][:40]}")
        print("=" * 80)
        return
    
    # Rich table
    table = Table(
        title="Installed SMF Skills",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    
    table.add_column("Select", justify="center", width=6)
    table.add_column("Name", style="cyan", width=25)
    table.add_column("Tier", width=8)
    table.add_column("Size", justify="right", width=10)
    table.add_column("Config", justify="center", width=8)
    table.add_column("Installed", width=12)
    table.add_column("Description", width=30)
    
    for skill in skills:
        marker = "✓" if skill["name"] in selected else " "
        
        # Tier styling
        tier = skill["tier"]
        tier_style = "yellow" if tier == "Pro" else "green"
        
        size_str = f"{skill['size_mb']:.1f} MB"
        config_str = "✓" if skill["has_config"] else "✗"
        date_str = skill["installed_date"].strftime("%Y-%m-%d") if skill["installed_date"] else "Unknown"
        
        desc = skill["description"][:35] + "..." if len(skill["description"]) > 35 else skill["description"]
        
        table.add_row(
            f"[{marker}]",
            skill["name"],
            f"[{tier_style}]{tier}[/{tier_style}]",
            size_str,
            config_str,
            date_str,
            desc
        )
    
    console.print(table)
    console.print()


def backup_skill(skill_name: str) -> bool:
    """Create a backup of a skill before removal."""
    skill_path = SKILLS_DIR / skill_name
    backup_dir = SMF_DIR / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"{skill_name}_{timestamp}"
    
    try:
        shutil.copytree(skill_path, backup_path)
        
        # Also backup config if exists
        config_path = CONFIG_DIR / skill_name
        if config_path.exists():
            config_backup = backup_dir / f"{skill_name}_config_{timestamp}"
            shutil.copytree(config_path, config_backup)
        
        return True
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]Backup failed: {e}[/red]")
        else:
            print(f"Backup failed: {e}")
        return False


def remove_skill(skill_name: str, dry_run: bool = False) -> Tuple[bool, str]:
    """Remove a skill completely."""
    actions = []
    
    # Paths to remove
    skill_path = SKILLS_DIR / skill_name
    config_path = CONFIG_DIR / skill_name
    wrapper_path = BIN_DIR / f"smf-{skill_name}"
    
    if not skill_path.exists():
        return False, f"Skill '{skill_name}' not found"
    
    if dry_run:
        actions.append(f"Would remove: {skill_path}")
        if config_path.exists():
            actions.append(f"Would remove config: {config_path}")
        if wrapper_path.exists():
            actions.append(f"Would remove wrapper: {wrapper_path}")
        return True, "\n".join(actions)
    
    # Actual removal
    try:
        # Remove skill directory
        shutil.rmtree(skill_path)
        actions.append(f"Removed: {skill_path}")
        
        # Remove config
        if config_path.exists():
            shutil.rmtree(config_path)
            actions.append(f"Removed config: {config_path}")
        
        # Remove wrapper
        if wrapper_path.exists():
            wrapper_path.unlink()
            actions.append(f"Removed wrapper: {wrapper_path}")
        
        return True, "\n".join(actions)
    
    except Exception as e:
        return False, f"Error removing skill: {e}"


def interactive_mode():
    """Interactive TUI mode."""
    skills = get_installed_skills()
    
    if not skills:
        if RICH_AVAILABLE:
            console.print(Panel("[yellow]No skills installed.[/yellow]\n\nRun: smf install <skill-name>"))
        else:
            print("No skills installed.")
        return
    
    selected = set()
    
    while True:
        if RICH_AVAILABLE:
            console.clear()
            console.print(Panel.fit("[bold cyan]SMF Skill Manager[/bold cyan]\n[dim]Manage your installed OpenClaw skills[/dim]"))
        else:
            os.system('clear' if os.name != 'nt' else 'cls')
            print("=" * 60)
            print("SMF Skill Manager")
            print("Manage your installed OpenClaw skills")
            print("=" * 60)
        
        display_skills_table(skills, selected)
        
        total_size = sum(s["size_mb"] for s in skills if s["name"] in selected)
        pro_count = sum(1 for s in skills if s["name"] in selected and s["is_pro"])
        
        if RICH_AVAILABLE:
            console.print(f"[dim]Selected: {len(selected)} skills ({total_size:.1f} MB)[/dim]")
            if pro_count > 0:
                console.print(f"[yellow]⚠️  {pro_count} Pro skills selected (subscription impact)[/yellow]")
            console.print()
            console.print("[bold]Commands:[/bold] [cyan]number[/cyan] toggle | [cyan]a[/cyan]ll | [cyan]n[/cyan]one | [cyan]b[/cyan]ackup selected | [cyan]r[/cyan]emove selected | [cyan]q[/cyan]uit")
            cmd = Prompt.ask("Enter command", default="").strip().lower()
        else:
            print(f"Selected: {len(selected)} skills ({total_size:.1f} MB)")
            if pro_count > 0:
                print(f"⚠️  {pro_count} Pro skills selected (subscription impact)")
            print()
            print("Commands: number toggle | a (all) | n (none) | b (backup) | r (remove) | q (quit)")
            cmd = input("Enter command: ").strip().lower()
        
        if cmd == 'q':
            break
        elif cmd == 'a':
            selected = {s["name"] for s in skills}
        elif cmd == 'n':
            selected = set()
        elif cmd == 'b':
            if not selected:
                if RICH_AVAILABLE:
                    console.print("[yellow]No skills selected for backup.[/yellow]")
                else:
                    print("No skills selected.")
                input("Press Enter to continue...")
                continue
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console if RICH_AVAILABLE else None
            ) as progress:
                task = progress.add_task("[cyan]Backing up skills...", total=len(selected))
                for skill_name in selected:
                    if backup_skill(skill_name):
                        progress.update(task, advance=1)
            
            if RICH_AVAILABLE:
                console.print(f"[green]✅ Backed up {len(selected)} skills to ~/.smf/backups/[/green]")
            else:
                print(f"Backed up {len(selected)} skills.")
            input("Press Enter to continue...")
            
        elif cmd == 'r':
            if not selected:
                if RICH_AVAILABLE:
                    console.print("[yellow]No skills selected for removal.[/yellow]")
                else:
                    print("No skills selected.")
                input("Press Enter to continue...")
                continue
            
            # Show what will be removed
            if RICH_AVAILABLE:
                console.print("\n[bold red]The following will be REMOVED:[/bold red]")
                for name in sorted(selected):
                    console.print(f"  • {name}")
                console.print(f"\n[bold]Total: {len(selected)} skills[/bold]")
                
                if pro_count > 0:
                    console.print(f"\n[yellow]⚠️  Warning: {pro_count} Pro skills will be removed.[/yellow]")
                    console.print("[dim]You may lose access to these features until reinstalled.[/dim]")
                
                if not Confirm.ask("\nAre you sure?", default=False):
                    continue
                
                backup_first = Confirm.ask("Create backup first?", default=True)
            else:
                print("\nThe following will be REMOVED:")
                for name in sorted(selected):
                    print(f"  • {name}")
                print(f"\nTotal: {len(selected)} skills")
                
                if pro_count > 0:
                    print(f"\n⚠️  Warning: {pro_count} Pro skills will be removed.")
                
                confirm = input("\nAre you sure? (yes/no): ").lower()
                if confirm != 'yes':
                    continue
                
                backup_first = input("Create backup first? (yes/no): ").lower() == 'yes'
            
            # Backup if requested
            if backup_first:
                for name in selected:
                    backup_skill(name)
            
            # Remove skills
            removed = []
            failed = []
            
            for name in selected:
                success, msg = remove_skill(name)
                if success:
                    removed.append(name)
                else:
                    failed.append((name, msg))
            
            if RICH_AVAILABLE:
                console.print(f"\n[green]✅ Removed {len(removed)} skills[/green]")
                if failed:
                    console.print(f"[red]❌ Failed to remove {len(failed)}:[/red]")
                    for name, err in failed:
                        console.print(f"  • {name}: {err}")
            else:
                print(f"\nRemoved {len(removed)} skills.")
                if failed:
                    print(f"Failed: {len(failed)}")
            
            # Refresh skills list
            skills = get_installed_skills()
            selected = set()
            input("Press Enter to continue...")
            
        elif cmd.isdigit():
            # Toggle by index
            idx = int(cmd) - 1
            if 0 <= idx < len(skills):
                name = skills[idx]["name"]
                if name in selected:
                    selected.remove(name)
                else:
                    selected.add(name)
        else:
            # Try to match skill name
            for skill in skills:
                if skill["name"] == cmd or skill["name"].startswith(cmd):
                    if skill["name"] in selected:
                        selected.remove(skill["name"])
                    else:
                        selected.add(skill["name"])
                    break


def list_skills():
    """Simple list command."""
    skills = get_installed_skills()
    
    if not skills:
        print("No skills installed.")
        return
    
    print(f"\nInstalled SMF Skills ({len(skills)} total):\n")
    print(f"{'Name':<25} {'Tier':<10} {'Size':<10} {'Installed'}")
    print("-" * 60)
    
    for skill in skills:
        tier = skill["tier"]
        tier_indicator = "💎" if skill["is_pro"] else "🎁"
        size = f"{skill['size_mb']:.1f} MB"
        date = skill["installed_date"].strftime("%Y-%m-%d") if skill["installed_date"] else "Unknown"
        print(f"{skill['name']:<25} {tier_indicator} {tier:<8} {size:<10} {date}")
    
    print()
    total_size = sum(s["size_mb"] for s in skills)
    print(f"Total size: {total_size:.1f} MB")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="SMF Skill Manager - Visual tool for managing installed OpenClaw skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smf run skill-manager              # Interactive TUI mode
  smf run skill-manager --list      # Simple list view
  smf run skill-manager --remove coffee-briefing  # Remove specific skill
  smf run skill-manager --backup morning-commute   # Backup specific skill

Interactive Commands:
  number      Toggle selection (e.g., '1' selects first skill)
  a           Select all skills
  n           Select none (clear)
  b           Backup selected skills
  r           Remove selected skills
  q           Quit
        """
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List installed skills (simple view)'
    )
    
    parser.add_argument(
        '--remove', '-r',
        metavar='SKILL',
        help='Remove a specific skill'
    )
    
    parser.add_argument(
        '--backup', '-b',
        metavar='SKILL',
        help='Backup a specific skill'
    )
    
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Show what would be done without doing it'
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_skills()
    elif args.remove:
        if args.dry_run:
            success, msg = remove_skill(args.remove, dry_run=True)
            print(msg)
        else:
            print(f"Removing {args.remove}...")
            success, msg = remove_skill(args.remove)
            if success:
                print(f"✅ {args.remove} removed successfully.")
            else:
                print(f"❌ {msg}")
    elif args.backup:
        print(f"Backing up {args.backup}...")
        if backup_skill(args.backup):
            print(f"✅ {args.backup} backed up to ~/.smf/backups/")
        else:
            print(f"❌ Backup failed.")
    else:
        # Interactive mode
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)


if __name__ == "__main__":
    main()
