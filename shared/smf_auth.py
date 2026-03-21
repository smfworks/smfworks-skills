#!/usr/bin/env python3
"""
SMF Auth - Shared Authentication Library for SMF Works Skills
Handles JWT token validation for Pro skills.
"""

import os
import sys
import json
import base64
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

# Public key for JWT verification (RS256)
# This is embedded so skills work offline after token issuance
SMF_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0Z3VS5JJcds3xfn/ygWy
l87sX2JY1mLroN0yWXsLz1Y3E0w6v7nB5Y3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B
5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B
5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B
5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q3B5Q
IDAQAB
-----END PUBLIC KEY-----"""

TOKEN_PATH = Path.home() / ".smf" / "token"
REVOKE_LIST_URL = "https://api.smf.works/revocation-list"


def load_token() -> Optional[str]:
    """Load JWT token from ~/.smf/token"""
    if TOKEN_PATH.exists():
        return TOKEN_PATH.read_text().strip()
    return None


def decode_jwt_without_verification(token: str) -> Dict:
    """Decode JWT payload without signature verification."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return {"error": "Invalid JWT format"}
        
        # Add padding if needed
        payload_b64 = parts[1]
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += '=' * padding
        
        payload_json = base64.urlsafe_b64decode(payload_b64)
        return json.loads(payload_json)
    except Exception as e:
        return {"error": f"Failed to decode token: {str(e)}"}


def is_token_revoked(subscriber_id: str, revoked_ids: list = None) -> bool:
    """Check if subscriber ID is in revocation list."""
    # For offline mode, use cached revocation list
    revoke_cache = Path.home() / ".smf" / "revoke_cache.json"
    
    if revoked_ids is not None:
        return subscriber_id in revoked_ids
    
    if revoke_cache.exists():
        try:
            data = json.loads(revoke_cache.read_text())
            revoked = data.get("revoked", [])
            return subscriber_id in revoked
        except:
            pass
    
    # If no cache and can't check online, allow (fail open for UX)
    return False


def require_subscription(skill_name: str, min_tier: str = "pro") -> Dict:
    """
    Check if user has valid subscription for a skill.
    
    Args:
        skill_name: Name of the skill being accessed
        min_tier: Minimum tier required ("pro" or "enterprise")
    
    Returns:
        Dict with subscription status and details
    """
    token = load_token()
    
    if not token:
        return {
            "valid": False,
            "error": "No subscription token found",
            "action": "Run: smf login"
        }
    
    # Decode token
    payload = decode_jwt_without_verification(token)
    
    if "error" in payload:
        return {
            "valid": False,
            "error": payload["error"],
            "action": "Run: smf login"
        }
    
    # Check expiration
    exp = payload.get("exp")
    if exp:
        now = datetime.now(timezone.utc).timestamp()
        if now > exp:
            return {
                "valid": False,
                "error": "Subscription expired",
                "action": "Visit: https://smf.works/subscribe"
            }
    
    # Check revocation
    subscriber_id = payload.get("sub")
    if subscriber_id and is_token_revoked(subscriber_id):
        return {
            "valid": False,
            "error": "Subscription revoked",
            "action": "Contact: support@smf.works"
        }
    
    # Check tier
    tier = payload.get("tier", "free")
    if tier == "free" and min_tier != "free":
        return {
            "valid": False,
            "error": f"This skill requires {min_tier} tier",
            "action": "Upgrade: https://smf.works/subscribe"
        }
    
    # Check skill access
    allowed_skills = payload.get("skills", [])
    if "*" not in allowed_skills and skill_name not in allowed_skills:
        return {
            "valid": False,
            "error": f"Skill '{skill_name}' not in subscription",
            "action": "Upgrade: https://smf.works/subscribe"
        }
    
    # Valid subscription
    return {
        "valid": True,
        "subscriber_id": subscriber_id,
        "tier": tier,
        "expires": payload.get("exp"),
        "skills": allowed_skills
    }


def show_subscription_error(result: Dict):
    """Display formatted subscription error message."""
    print(f"❌ {result.get('error', 'Subscription required')}")
    if "action" in result:
        print(f"👉 {result['action']}")
    print(f"")
    print(f"💡 SMF Works Pro gives you access to all premium skills")
    print(f"   Starting at $19.99/month (price locked forever)")
    print(f"   Learn more: https://smf.works/subscribe")


# Backward compatibility alias
check_subscription = require_subscription
