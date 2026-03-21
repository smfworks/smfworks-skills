#!/usr/bin/env python3
"""
Pro Skill Template for SMF Works
Template for building subscription-restricted skills.

Usage:
1. Copy this file to skills/<skill-name>/main.py
2. Update SKILL_NAME constant
3. Implement your skill logic in run_skill()
4. Test with: python main.py --test-mode
"""

import sys
from pathlib import Path

# Add shared auth to path (adjust based on skill location)
shared_path = Path(__file__).parent.parent / "shared"
sys.path.insert(0, str(shared_path))

try:
    from smf_auth import require_subscription, show_subscription_error
except ImportError:
    # Fallback for development
    print("⚠️  smf_auth not found. Running in test mode.")
    require_subscription = lambda skill, tier=None: {"valid": True, "tier": "test"}
    show_subscription_error = lambda r: print(f"Error: {r}")

# === SKILL CONFIGURATION ===
SKILL_NAME = "your-skill-name"  # Change this!
MIN_TIER = "pro"  # "pro" or "enterprise"


def run_skill(args: list) -> int:
    """
    Main skill logic. Implement your functionality here.
    
    Args:
        args: Command line arguments (sys.argv[1:])
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    print(f"🎯 Running {SKILL_NAME}")
    print("=" * 40)
    
    # Your skill implementation here
    print("Hello from your Pro skill!")
    print(f"Args: {args}")
    
    return 0


def main():
    """Entry point with subscription check."""
    
    # Check for test mode (skip auth)
    if "--test-mode" in sys.argv:
        sys.argv.remove("--test-mode")
        print("🔧 TEST MODE: Skipping subscription check")
        return run_skill(sys.argv[1:])
    
    # Check subscription
    sub = require_subscription(SKILL_NAME, MIN_TIER)
    
    if not sub["valid"]:
        show_subscription_error(sub)
        return 1
    
    # Run skill with subscription info
    print(f"✅ Subscription active: {sub['tier']} tier")
    print(f"   Subscriber: {sub.get('subscriber_id', 'unknown')[:8]}...")
    print("")
    
    return run_skill(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
