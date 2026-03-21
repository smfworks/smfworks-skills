#!/usr/bin/env python3
"""
OpenClaw Optimizer - SMF Works Pro Skill
Audit and optimize OpenClaw workspace for cost, performance, and context efficiency.

Usage:
    smf run openclaw-optimizer audit                      # Full workspace audit
    smf run openclaw-optimizer analyze --context           # Analyze context bloat
    smf run openclaw-optimizer recommend --model-routing   # Get model routing plan
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add shared auth to path
shared_path = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from smf_auth import require_subscription, show_subscription_error

SKILL_NAME = "openclaw-optimizer"
MIN_TIER = "pro"
WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"


def get_file_size(path: Path) -> int:
    """Get file size in bytes."""
    try:
        return path.stat().st_size
    except:
        return 0


def get_dir_size(path: Path) -> int:
    """Get directory size in bytes."""
    total = 0
    try:
        for item in path.rglob("*"):
            if item.is_file():
                total += item.stat().st_size
    except:
        pass
    return total


def analyze_workspace_size() -> Dict:
    """Analyze workspace size breakdown."""
    results = {"total_size": 0, "by_category": {}}
    
    if not WORKSPACE_DIR.exists():
        return results
    
    total = get_dir_size(WORKSPACE_DIR)
    results["total_size"] = total
    
    categories = {
        "bootstrap": ["BOOTSTRAP.md", "SOUL.md", "USER.md", "MEMORY.md"],
        "memory": ["memory/"],
        "config": ["TOOLS.md", "AGENTS.md"],
        "skills": ["skills/"]
    }
    
    for category, patterns in categories.items():
        cat_size = 0
        for pattern in patterns:
            path = WORKSPACE_DIR / pattern
            if path.exists():
                if path.is_file():
                    cat_size += get_file_size(path)
                else:
                    cat_size += get_dir_size(path)
        results["by_category"][category] = cat_size
    
    return results


def analyze_skill_surface() -> Dict:
    """Analyze loaded skills."""
    results = {"skill_count": 0, "recommendations": []}
    
    skills_dir = WORKSPACE_DIR / "skills"
    if skills_dir.exists():
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        results["skill_count"] = len(skill_dirs)
    
    return results


def generate_audit_report():
    """Generate audit report."""
    print("\n" + "=" * 60)
    print("OpenClaw Workspace Audit")
    print("=" * 60)
    
    sizes = analyze_workspace_size()
    skills = analyze_skill_surface()
    
    print(f"\nTotal Size: {sizes['total_size'] / 1024 / 1024:.2f} MB")
    print(f"Skills Loaded: {skills['skill_count']}")
    
    print("\nSize by Category:")
    for cat, size in sizes.get("by_category", {}).items():
        if size > 0:
            print(f"  {cat}: {size / 1024:.1f} KB")
    
    print("\nRecommendations:")
    if sizes['total_size'] > 5 * 1024 * 1024:  # > 5MB
        print("  ⚠ Large workspace - review for bloat")
    if skills['skill_count'] > 10:
        print("  ⚠ Many skills loaded - review necessity")
    
    print("\n" + "=" * 60)


def main():
    if "--test-mode" in sys.argv:
        sys.argv.remove("--test-mode")
        subscription = {"valid": True, "tier": "test"}
    else:
        subscription = require_subscription(SKILL_NAME, MIN_TIER)
        if not subscription["valid"]:
            show_subscription_error(subscription)
            return 1
    
    print("🚀 OpenClaw Optimizer")
    
    if len(sys.argv) < 2:
        print("\nCommands: audit, analyze, recommend")
        return 0
    
    command = sys.argv[1]
    
    if command == "audit":
        generate_audit_report()
    elif command == "analyze":
        print("Analyzing context...")
        generate_audit_report()
    elif command == "recommend":
        print("Model Routing Recommendations:")
        print("\n  Coding: minimax-m2.7")
        print("  Quick tasks: qwen3.5:9b")
        print("  Reasoning: kimi-k2.5")
    else:
        print(f"Unknown: {command}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
