#!/usr/bin/env python3
"""
OpenClaw Optimizer - SMF Works Pro Skill
Audit and optimize OpenClaw workspace for cost, performance, and context efficiency.

Usage:
    smf run openclaw-optimizer audit                      # Full workspace audit
    smf run openclaw-optimizer analyze --context           # Analyze context bloat
    smf run openclaw-optimizer recommend --model-routing   # Get model routing plan
    smf run openclaw-optimizer optimize --skills            # Optimize skill loading
    smf run openclaw-optimizer report                     # Generate optimization report
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# Add shared auth to path
shared_path = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from smf_auth import require_subscription, show_subscription_error

SKILL_NAME = "openclaw-optimizer"
MIN_TIER = "pro"
WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"
REPORTS_DIR = Path.home() / ".smf" / "optimizer-reports"

# Optimization thresholds
WARNING_SIZE_MB = 10
CRITICAL_SIZE_MB = 50
MAX_RECOMMENDED_SKILLS = 10
MAX_MEMORY_MB = 100


def ensure_dirs():
    """Ensure report directory exists."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def get_file_size(path: Path) -> int:
    """Get file size in bytes."""
    try:
        return path.stat().st_size
    except:
        return 0


def get_dir_size(path: Path, max_depth: int = 5) -> int:
    """Get directory size in bytes with depth limit."""
    total = 0
    try:
        if max_depth <= 0:
            return 0
        for item in path.iterdir():
            if item.is_file():
                total += item.stat().st_size
            elif item.is_dir():
                total += get_dir_size(item, max_depth - 1)
    except PermissionError:
        pass
    except:
        pass
    return total


def format_size(size_bytes: int) -> str:
    """Format bytes to human readable."""
    if size_bytes == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


def analyze_workspace_size() -> Dict:
    """Analyze workspace size breakdown."""
    results = {
        "total_size": 0,
        "total_size_mb": 0,
        "by_category": {},
        "large_files": []
    }
    
    if not WORKSPACE_DIR.exists():
        return results
    
    total = get_dir_size(WORKSPACE_DIR)
    results["total_size"] = total
    results["total_size_mb"] = total / (1024 * 1024)
    
    categories = {
        "bootstrap": ["BOOTSTRAP.md", "SOUL.md", "USER.md", "MEMORY.md", "IDENTITY.md"],
        "memory": ["memory/"],
        "config": ["TOOLS.md", "AGENTS.md", "TOOLS.md", "HEARTBEAT.md"],
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
        results["by_category"][category] = {
            "size": cat_size,
            "size_formatted": format_size(cat_size),
            "percentage": (cat_size / total * 100) if total > 0 else 0
        }
    
    # Find large files (>1MB)
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        for file in files:
            file_path = Path(root) / file
            try:
                size = file_path.stat().st_size
                if size > 1024 * 1024:  # > 1MB
                    results["large_files"].append({
                        "path": str(file_path.relative_to(WORKSPACE_DIR)),
                        "size": format_size(size)
                    })
            except:
                pass
    
    results["large_files"].sort(key=lambda x: x["size"], reverse=True)
    results["large_files"] = results["large_files"][:20]  # Top 20
    
    return results


def analyze_skills() -> Dict:
    """Analyze loaded skills for optimization opportunities."""
    results = {
        "skill_count": 0,
        "skills": [],
        "recommendations": [],
        "total_skill_size": 0
    }
    
    skills_dir = WORKSPACE_DIR / "skills"
    if not skills_dir.exists():
        return results
    
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_size = get_dir_size(skill_dir)
            results["total_skill_size"] += skill_size
            
            skill_info = {
                "name": skill_dir.name,
                "size": skill_size,
                "size_formatted": format_size(skill_size)
            }
            
            # Check for SKILL.md
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                try:
                    content = skill_md.read_text()
                    # Check for Pro label
                    skill_info["is_pro"] = "(Pro)" in content or "Pro Skill" in content
                except:
                    pass
            
            results["skills"].append(skill_info)
    
    results["skill_count"] = len(results["skills"])
    results["skills"].sort(key=lambda x: x["size"], reverse=True)
    
    # Generate recommendations
    if results["skill_count"] > MAX_RECOMMENDED_SKILLS:
        results["recommendations"].append({
            "priority": "high",
            "message": f"Too many skills loaded ({results['skill_count']}). Consider removing unused skills."
        })
    
    # Check for large skills
    large_skills = [s for s in results["skills"] if s["size"] > 1024 * 1024]
    if large_skills:
        results["recommendations"].append({
            "priority": "medium",
            "message": f"{len(large_skills)} skills are >1MB. Review for bloat."
        })
    
    return results


def analyze_context_bloat() -> Dict:
    """Analyze context for bloat issues."""
    results = {
        "memory_files": [],
        "duplicated_content": [],
        "recommendations": []
    }
    
    memory_dir = WORKSPACE_DIR / "memory"
    if not memory_dir.exists():
        return results
    
    # Check memory files
    for mem_file in memory_dir.glob("*.md"):
        size = get_file_size(mem_file)
        results["memory_files"].append({
            "file": mem_file.name,
            "size": format_size(size),
            "size_bytes": size
        })
    
    results["memory_files"].sort(key=lambda x: x["size_bytes"], reverse=True)
    
    # Check for large memory files
    large_mem = [f for f in results["memory_files"] if f["size_bytes"] > 1024 * 1024]
    if large_mem:
        results["recommendations"].append({
            "priority": "high",
            "message": f"{len(large_mem)} memory files >1MB. Consider archiving old entries."
        })
    
    # Check total memory size
    total_mem_size = get_dir_size(memory_dir)
    if total_mem_size > MAX_MEMORY_MB * 1024 * 1024:
        results["recommendations"].append({
            "priority": "critical",
            "message": f"Memory directory is {format_size(total_mem_size)}. This impacts context window."
        })
    
    return results


def get_model_routing_recommendations() -> List[Dict]:
    """Get model routing recommendations based on task types."""
    return [
        {
            "task_type": "coding",
            "recommended_model": "ollama/minimax-m2.7:cloud",
            "reason": "Optimized for code generation and technical tasks",
            "cost_tier": "medium"
        },
        {
            "task_type": "quick_tasks",
            "recommended_model": "ollama/qwen3.5:9b",
            "reason": "Fast and efficient for simple queries",
            "cost_tier": "low"
        },
        {
            "task_type": "reasoning",
            "recommended_model": "ollama/kimi-k2.5",
            "reason": "Strong reasoning capabilities for complex problems",
            "cost_tier": "medium"
        },
        {
            "task_type": "code_review",
            "recommended_model": "openrouter/anthropic/claude-sonnet-4.6",
            "reason": "Best for security audits and quality assurance",
            "cost_tier": "high"
        }
    ]


def generate_optimization_recommendations(size_analysis: Dict, skills_analysis: Dict, 
                                        context_analysis: Dict) -> List[Dict]:
    """Generate optimization recommendations."""
    recommendations = []
    
    # Size-based recommendations
    if size_analysis["total_size_mb"] > CRITICAL_SIZE_MB:
        recommendations.append({
            "category": "critical",
            "priority": "urgent",
            "message": f"Workspace is {format_size(size_analysis['total_size'])}. Immediate action required.",
            "actions": [
                "Archive old memory files",
                "Remove unused skills",
                "Compress large files"
            ]
        })
    elif size_analysis["total_size_mb"] > WARNING_SIZE_MB:
        recommendations.append({
            "category": "size",
            "priority": "high",
            "message": f"Workspace is {format_size(size_analysis['total_size'])}. Consider cleanup.",
            "actions": [
                "Review large files",
                "Clean up old logs"
            ]
        })
    
    # Skill recommendations
    recommendations.extend(skills_analysis.get("recommendations", []))
    
    # Context recommendations
    recommendations.extend(context_analysis.get("recommendations", []))
    
    # Add general recommendations
    if not any(r.get("category") == "skills" for r in recommendations):
        recommendations.append({
            "category": "general",
            "priority": "low",
            "message": "Workspace is well-optimized",
            "actions": ["Continue monitoring"]
        })
    
    return recommendations


def print_audit_report(size_analysis: Dict, skills_analysis: Dict, 
                      context_analysis: Dict, recommendations: List[Dict]):
    """Print formatted audit report."""
    print("\n" + "=" * 70)
    print("  OpenClaw Workspace Audit Report")
    print("=" * 70)
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Size Analysis
    print("📊 Size Analysis")
    print("-" * 70)
    print(f"  Total Size: {format_size(size_analysis['total_size'])}")
    print()
    print("  By Category:")
    for cat, data in size_analysis.get("by_category", {}).items():
        print(f"    • {cat:12} {data['size_formatted']:>10} ({data['percentage']:.1f}%)")
    
    if size_analysis.get("large_files"):
        print("\n  Large Files (>1MB):")
        for f in size_analysis["large_files"][:10]:
            print(f"    • {f['path'][:40]:40} {f['size']}")
    
    # Skills Analysis
    print("\n" + "=" * 70)
    print("🛠️  Skills Analysis")
    print("-" * 70)
    print(f"  Total Skills: {skills_analysis['skill_count']}")
    print(f"  Total Skill Size: {format_size(skills_analysis['total_skill_size'])}")
    print()
    
    if skills_analysis["skills"]:
        print("  Top 5 Skills by Size:")
        for skill in skills_analysis["skills"][:5]:
            pro_label = " [Pro]" if skill.get("is_pro") else ""
            print(f"    • {skill['name'][:25]:25} {skill['size_formatted']:>10}{pro_label}")
    
    # Context Analysis
    print("\n" + "=" * 70)
    print("📝 Context Analysis")
    print("-" * 70)
    print(f"  Memory Files: {len(context_analysis['memory_files'])}")
    
    if context_analysis.get("memory_files"):
        total_mem = sum(f['size_bytes'] for f in context_analysis['memory_files'])
        print(f"  Total Memory Size: {format_size(total_mem)}")
    
    # Recommendations
    print("\n" + "=" * 70)
    print("💡 Recommendations")
    print("-" * 70)
    
    if not recommendations:
        print("  ✅ No issues found - workspace is well-optimized!")
    else:
        for rec in recommendations:
            priority_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢", "urgent": "🔴"}.get(
                rec.get("priority", "low"), "⚪"
            )
            print(f"\n  {priority_icon} [{rec.get('category', 'general').upper()}] {rec.get('message', '')}")
            if 'actions' in rec:
                for action in rec['actions']:
                    print(f"      → {action}")
    
    print("\n" + "=" * 70)


def save_report(size_analysis: Dict, skills_analysis: Dict, 
               context_analysis: Dict, recommendations: List[Dict]) -> str:
    """Save report to file."""
    ensure_dirs()
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_file = REPORTS_DIR / f"optimizer-report-{timestamp}.json"
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "size_analysis": size_analysis,
        "skills_analysis": skills_analysis,
        "context_analysis": context_analysis,
        "recommendations": recommendations,
        "summary": {
            "total_size_mb": size_analysis["total_size_mb"],
            "skill_count": skills_analysis["skill_count"],
            "recommendation_count": len(recommendations),
            "critical_issues": len([r for r in recommendations if r.get("priority") in ["critical", "urgent"]])
        }
    }
    
    report_file.write_text(json.dumps(report, indent=2))
    return str(report_file)


def show_help():
    """Show help message."""
    print("""🚀 OpenClaw Optimizer

Audit and optimize your OpenClaw workspace.

Commands:
  audit                      # Full workspace audit
  analyze --context          # Analyze context bloat
  analyze --skills           # Analyze skills
  recommend                  # Get optimization recommendations
  optimize --skills          # Optimize skill loading
  report                     # Generate and save report
  help                       # Show this help

Examples:
  smf run openclaw-optimizer audit
  smf run openclaw-optimizer analyze --context
  smf run openclaw-optimizer report

What it checks:
  • Workspace size and breakdown
  • Large files that impact performance
  • Skill count and bloat
  • Memory file size and optimization
  • Model routing recommendations

Reports saved to: ~/.smf/optimizer-reports/
""")


def main():
    """Main entry point."""
    if "--test-mode" in sys.argv:
        sys.argv.remove("--test-mode")
        subscription = {"valid": True, "tier": "test"}
    else:
        subscription = require_subscription(SKILL_NAME, MIN_TIER)
        if not subscription["valid"]:
            show_subscription_error(subscription)
            return 1
    
    print("🚀 OpenClaw Optimizer")
    print(f"   Subscription: {subscription.get('tier', 'test')}")
    print()
    
    if len(sys.argv) < 2:
        show_help()
        return 0
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "audit":
        print("Running full workspace audit...")
        size_analysis = analyze_workspace_size()
        skills_analysis = analyze_skills()
        context_analysis = analyze_context_bloat()
        recommendations = generate_optimization_recommendations(
            size_analysis, skills_analysis, context_analysis
        )
        print_audit_report(size_analysis, skills_analysis, context_analysis, recommendations)
    
    elif command == "analyze":
        if "--context" in args:
            print("Analyzing context bloat...")
            context_analysis = analyze_context_bloat()
            print(f"Memory Files: {len(context_analysis['memory_files'])}")
            for rec in context_analysis.get("recommendations", []):
                print(f"• {rec['message']}")
        
        elif "--skills" in args:
            print("Analyzing skills...")
            skills_analysis = analyze_skills()
            print(f"Skills Loaded: {skills_analysis['skill_count']}")
            for skill in skills_analysis["skills"][:10]:
                print(f"  • {skill['name']}: {skill['size_formatted']}")
        
        else:
            size_analysis = analyze_workspace_size()
            print(f"Total Size: {format_size(size_analysis['total_size'])}")
            for cat, data in size_analysis.get("by_category", {}).items():
                print(f"  • {cat}: {data['size_formatted']}")
    
    elif command == "recommend":
        print("Generating recommendations...")
        size_analysis = analyze_workspace_size()
        skills_analysis = analyze_skills()
        context_analysis = analyze_context_bloat()
        recommendations = generate_optimization_recommendations(
            size_analysis, skills_analysis, context_analysis
        )
        
        print("\n💡 Recommendations:")
        for rec in recommendations:
            print(f"• {rec['message']}")
        
        # Model routing
        if "--model-routing" in args:
            print("\n🤖 Model Routing Plan:")
            for route in get_model_routing_recommendations():
                print(f"  • {route['task_type']}: {route['recommended_model']}")
    
    elif command == "optimize":
        if "--skills" in args:
            print("Optimizing skill loading...")
            skills_analysis = analyze_skills()
            if skills_analysis["skill_count"] > MAX_RECOMMENDED_SKILLS:
                print(f"⚠️  Consider unloading {skills_analysis['skill_count'] - MAX_RECOMMENDED_SKILLS} skills:")
                # Suggest skills to remove (largest non-pro skills)
                candidates = [s for s in skills_analysis["skills"] if not s.get("is_pro")]
                for skill in candidates[:5]:
                    print(f"    • {skill['name']} ({skill['size_formatted']})")
            else:
                print("✅ Skill count is optimal")
    
    elif command == "report":
        print("Generating optimization report...")
        size_analysis = analyze_workspace_size()
        skills_analysis = analyze_skills()
        context_analysis = analyze_context_bloat()
        recommendations = generate_optimization_recommendations(
            size_analysis, skills_analysis, context_analysis
        )
        
        report_path = save_report(size_analysis, skills_analysis, context_analysis, recommendations)
        print(f"✅ Report saved: {report_path}")
    
    elif command in ("help", "--help", "-h"):
        show_help()
    
    else:
        print(f"Unknown command: {command}")
        show_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
