#!/usr/bin/env python3
"""
SMF Login CLI Tool
Authenticate and download subscription token for SMF Works skills.
"""

import sys
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

SMF_DIR = Path.home() / ".smf"
TOKEN_PATH = SMF_DIR / "token"
API_BASE = "https://smfworks.com/api"


def ensure_smf_dir():
    """Ensure ~/.smf directory exists."""
    SMF_DIR.mkdir(mode=0o700, exist_ok=True)


def save_token(token: str):
    """Save token to ~/.smf/token with restricted permissions."""
    ensure_smf_dir()
    TOKEN_PATH.write_text(token)
    TOKEN_PATH.chmod(0o600)  # Only owner can read/write


def load_token() -> str:
    """Load existing token."""
    if TOKEN_PATH.exists():
        return TOKEN_PATH.read_text().strip()
    return None


def validate_token(token: str) -> dict:
    """Validate token with SMF API."""
    try:
        req = Request(
            f"{API_BASE}/token/validate",
            method="POST",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"token": token}).encode()
        )
        
        with urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"valid": False, "error": f"HTTP {e.code}"}
    except URLError:
        # Offline mode - check local
        return {"valid": True, "offline": True}
    except Exception as e:
        return {"valid": False, "error": str(e)}


def login():
    """Interactive login flow."""
    print("🔐 SMF Works Login")
    print("=" * 40)
    print("")
    
    # Check for existing token
    existing = load_token()
    if existing:
        print("ℹ️  Existing token found. Validating...")
        result = validate_token(existing)
        if result.get("valid"):
            print(f"✅ Token is valid!")
            print(f"   Tier: {result.get('tier', 'unknown')}")
            print(f"   Expires: {result.get('expires', 'unknown')}")
            print("")
            
            overwrite = input("Replace existing token? (y/N): ").lower()
            if overwrite != 'y':
                print("Keeping existing token.")
                return
        else:
            print(f"⚠️  Existing token invalid: {result.get('error')}")
            print("")
    
    # New token flow
    print("To get your token:")
    print("1. Visit: https://smfworks.com/dashboard")
    print("2. Sign in with your account")
    print("3. Copy your API token")
    print("")
    
    token = input("Paste your SMF token: ").strip()
    
    if not token:
        print("❌ No token provided. Exiting.")
        sys.exit(1)
    
    # Validate token
    print("\nValidating token...")
    result = validate_token(token)
    
    if not result.get("valid"):
        print(f"❌ Token validation failed: {result.get('error')}")
        sys.exit(1)
    
    # Save token
    save_token(token)
    print(f"✅ Token saved to {TOKEN_PATH}")
    print(f"   Tier: {result.get('tier', 'pro')}")
    print(f"   Skills: {result.get('skills_count', 'unlimited')}")
    print("")
    print("You're ready to use SMF Works Pro skills!")


def logout():
    """Remove stored token."""
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()
        print("✅ Logged out. Token removed.")
    else:
        print("ℹ️  No token found. Already logged out.")


def status():
    """Show current subscription status."""
    token = load_token()
    
    if not token:
        print("❌ Not logged in")
        print("   Run: smf login")
        sys.exit(1)
    
    print("🔐 SMF Works Subscription Status")
    print("=" * 40)
    
    result = validate_token(token)
    
    if result.get("valid"):
        print(f"✅ Active subscription")
        print(f"   Tier: {result.get('tier', 'unknown')}")
        print(f"   Expires: {result.get('expires', 'unknown')}")
        if result.get("offline"):
            print(f"   Mode: Offline (cached)")
    else:
        print(f"❌ Invalid subscription: {result.get('error')}")
        print(f"   Run: smf login")


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: smf <command>")
        print("")
        print("Commands:")
        print("  login     - Authenticate and save token")
        print("  logout    - Remove saved token")
        print("  status    - Show subscription status")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "login":
        login()
    elif command == "logout":
        logout()
    elif command == "status":
        status()
    else:
        print(f"Unknown command: {command}")
        print("Run without arguments for help")
        sys.exit(1)


if __name__ == "__main__":
    main()
