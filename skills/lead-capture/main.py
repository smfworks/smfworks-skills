#!/usr/bin/env python3
"""
Lead Capture System - SMF Works Pro Skill
Capture, qualify, and manage sales leads for small businesses.

Usage:
    python main.py capture          # Interactive lead capture
    python main.py list             # List all leads
    python main.py export [format]  # Export leads (csv/json)
    python main.py stats            # Show lead statistics
"""

import sys
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add shared auth to path
shared_path = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from smf_auth import require_subscription, show_subscription_error

# Skill configuration
SKILL_NAME = "lead-capture"
MIN_TIER = "pro"
LEADS_DIR = Path.home() / ".smf" / "leads"


def ensure_leads_dir():
    """Ensure leads directory exists."""
    LEADS_DIR.mkdir(parents=True, exist_ok=True)


def generate_lead_id() -> str:
    """Generate unique lead ID."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"lead-{timestamp}"


def capture_lead() -> Dict:
    """Interactive lead capture."""
    print("\n🎯 Lead Capture")
    print("=" * 40)
    
    lead = {
        "id": generate_lead_id(),
        "captured_at": datetime.now().isoformat(),
        "status": "new"
    }
    
    print("\nEnter lead information (press Enter to skip):")
    
    # Required fields
    lead["name"] = input("Name: ").strip()
    lead["email"] = input("Email: ").strip()
    lead["phone"] = input("Phone: ").strip()
    
    # Business info
    lead["company"] = input("Company: ").strip()
    lead["title"] = input("Title/Role: ").strip()
    
    # Qualification
    print("\nQualification:")
    print("  Budget: small/medium/large")
    lead["budget"] = input("Budget: ").strip().lower()
    
    print("  Timeline: immediate/1-month/3-months/6-months")
    lead["timeline"] = input("Timeline: ").strip().lower()
    
    print("  Source: website/referral/social/cold-outreach/other")
    lead["source"] = input("Source: ").strip().lower()
    
    # Notes
    lead["notes"] = input("Notes: ").strip()
    
    # Calculate score
    lead["score"] = calculate_lead_score(lead)
    
    # Save lead
    ensure_leads_dir()
    lead_file = LEADS_DIR / f"{lead['id']}.json"
    lead_file.write_text(json.dumps(lead, indent=2))
    
    return lead


def calculate_lead_score(lead: Dict) -> int:
    """Calculate lead qualification score (0-100)."""
    score = 0
    
    # Contact completeness
    if lead.get("email"):
        score += 20
    if lead.get("phone"):
        score += 20
    
    # Business info
    if lead.get("company"):
        score += 15
    if lead.get("title"):
        score += 10
    
    # Qualification
    budget_scores = {"small": 10, "medium": 20, "large": 30}
    score += budget_scores.get(lead.get("budget"), 0)
    
    timeline_scores = {"immediate": 30, "1-month": 20, "3-months": 10, "6-months": 5}
    score += timeline_scores.get(lead.get("timeline"), 0)
    
    return min(score, 100)


def get_lead_status(score: int) -> str:
    """Get status based on score."""
    if score >= 80:
        return "🔥 Hot"
    elif score >= 60:
        return "🌡️ Warm"
    elif score >= 40:
        return "❄️ Cold"
    else:
        return "💤 Dormant"


def list_leads(status_filter: str = None, limit: int = None) -> List[Dict]:
    """List all captured leads."""
    ensure_leads_dir()
    
    leads = []
    for lead_file in LEADS_DIR.glob("*.json"):
        try:
            lead = json.loads(lead_file.read_text())
            leads.append(lead)
        except:
            continue
    
    # Sort by captured_at (newest first)
    leads.sort(key=lambda x: x.get("captured_at", ""), reverse=True)
    
    # Apply filters
    if status_filter:
        leads = [l for l in leads if l.get("status") == status_filter]
    
    if limit:
        leads = leads[:limit]
    
    return leads


def display_leads(leads: List[Dict]):
    """Display leads in formatted table."""
    if not leads:
        print("No leads found.")
        return
    
    print(f"\n📊 {len(leads)} Lead(s)")
    print("-" * 80)
    print(f"{'ID':<20} {'Name':<20} {'Score':<8} {'Status':<12} {'Source':<15}")
    print("-" * 80)
    
    for lead in leads:
        lead_id = lead.get("id", "unknown")[:18]
        name = lead.get("name", "N/A")[:18]
        score = lead.get("score", 0)
        status = get_lead_status(score)
        source = lead.get("source", "unknown")[:13]
        
        print(f"{lead_id:<20} {name:<20} {score:<8} {status:<12} {source:<15}")
    
    print("-" * 80)


def export_leads(format: str = "csv", output_file: str = None) -> str:
    """Export leads to file."""
    leads = list_leads()
    
    if not leads:
        return "No leads to export."
    
    if format == "csv":
        if not output_file:
            output_file = f"leads-export-{datetime.now().strftime('%Y%m%d')}.csv"
        
        with open(output_file, 'w', newline='') as f:
            if leads:
                writer = csv.DictWriter(f, fieldnames=leads[0].keys())
                writer.writeheader()
                writer.writerows(leads)
        
        return f"Exported {len(leads)} leads to {output_file}"
    
    elif format == "json":
        if not output_file:
            output_file = f"leads-export-{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(output_file, 'w') as f:
            json.dump(leads, f, indent=2)
        
        return f"Exported {len(leads)} leads to {output_file}"
    
    else:
        return f"Unknown format: {format}"


def show_stats():
    """Show lead statistics."""
    leads = list_leads()
    
    if not leads:
        print("No leads captured yet.")
        return
    
    total = len(leads)
    
    # Score distribution
    hot = len([l for l in leads if l.get("score", 0) >= 80])
    warm = len([l for l in leads if 60 <= l.get("score", 0) < 80])
    cold = len([l for l in leads if 40 <= l.get("score", 0) < 60])
    dormant = len([l for l in leads if l.get("score", 0) < 40])
    
    # Source breakdown
    sources = {}
    for lead in leads:
        source = lead.get("source", "unknown")
        sources[source] = sources.get(source, 0) + 1
    
    print("\n📈 Lead Statistics")
    print("=" * 40)
    print(f"Total Leads: {total}")
    print("")
    print("Qualification:")
    print(f"  🔥 Hot (80-100):     {hot} ({hot/total*100:.1f}%)")
    print(f"  🌡️ Warm (60-79):     {warm} ({warm/total*100:.1f}%)")
    print(f"  ❄️ Cold (40-59):     {cold} ({cold/total*100:.1f}%)")
    print(f"  💤 Dormant (0-39):   {dormant} ({dormant/total*100:.1f}%)")
    print("")
    print("Sources:")
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        print(f"  {source}: {count}")


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
        
        print(f"✅ Lead Capture System")
        print(f"   Subscription: {subscription['tier']}")
        print("")
    
    # Parse command
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [options]")
        print("")
        print("Commands:")
        print("  capture              - Capture a new lead (interactive)")
        print("  list [limit]         - List all leads")
        print("  export [csv|json]    - Export leads to file")
        print("  stats                - Show lead statistics")
        print("")
        print("Examples:")
        print("  python main.py capture")
        print("  python main.py list 10")
        print("  python main.py export csv")
        print("  python main.py stats")
        return 0
    
    command = sys.argv[1]
    
    if command == "capture":
        lead = capture_lead()
        print(f"\n✅ Lead captured: {lead['id']}")
        print(f"   Score: {lead['score']}/100 ({get_lead_status(lead['score'])})")
        print(f"   Saved to: {LEADS_DIR / lead['id']}.json")
    
    elif command == "list":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
        leads = list_leads(limit=limit)
        display_leads(leads)
    
    elif command == "export":
        format = sys.argv[2] if len(sys.argv) > 2 else "csv"
        result = export_leads(format)
        print(result)
    
    elif command == "stats":
        show_stats()
    
    else:
        print(f"Unknown command: {command}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
