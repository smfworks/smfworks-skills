#!/usr/bin/env python3
"""
SMF Auth - Shared Authentication Library for SMF Works Skills
Handles JWT token validation for Pro skills with proper RS256 signature verification.
"""

import os
import sys
import json
import jwt
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Public key for JWT verification (RS256)
# This is embedded so skills work offline after token issuance
SMF_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApNewZh6+NcnXN/9EwS7l
GynbV3E20yDIJ226+OmBsGTaHKIs8lYsLFiemUXW/m+RoMRydXGDkhRywIBxCiCb
FE2xYnZSWgdLGs5csjtAOvBA7Vd/o/jIZw8yyHBznKyNLKlhxaZv0wmGqFcc9pYQ
jLg42fcpBIH//iIKSEQ0RYE+QJ1CyulWj0x8Ty0/vAJuDClQlOimubB9WsqoGblW
Whk0/3/yHl7R6sQikybxSRW82xfvw4ASUdCtJ9H+B5YFV4QwjR3Xe+ytcYACp1Kx
RvjBRhZVnFOOvuMl88afwGV/GypSA7nZEn6X9IVRyR/YuBhwt7ppAAl5KNrrcaBw
qQIDAQAB
-----END PUBLIC KEY-----"""

TOKEN_PATH = Path.home() / ".smf" / "token"
REVOKE_LIST_URL = "https://api.smf.works/revocation-list"

# Try to load public key at module load time
try:
    PUBLIC_KEY = serialization.load_pem_public_key(
        SMF_PUBLIC_KEY.encode(),
        backend=default_backend()
    )
except Exception:
    PUBLIC_KEY = None


def load_token() -> Optional[str]:
    """Load JWT token from ~/.smf/token"""
    if TOKEN_PATH.exists():
        return TOKEN_PATH.read_text().strip()
    return None


def load_revocation_list() -> list:
    """Load cached revocation list."""
    revoke_cache = Path.home() / ".smf" / "revoke_cache.json"
    
    if revoke_cache.exists():
        try:
            data = json.loads(revoke_cache.read_text())
            return data.get("revoked", [])
        except (json.JSONDecodeError, IOError):
            pass
    
    return []


def is_token_revoked(subscriber_id: str) -> bool:
    """Check if subscriber ID is in revocation list."""
    revoked_ids = load_revocation_list()
    return subscriber_id in revoked_ids


def verify_jwt(token: str) -> Dict:
    """
    Verify JWT token signature and decode payload.
    
    Args:
        token: JWT token string
    
    Returns:
        Dict with payload if valid, or error details if invalid
    """
    if PUBLIC_KEY is None:
        return {"error": "Public key failed to load", "valid": False}
    
    try:
        # Verify signature and decode
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            options={
                "require": ["exp", "sub", "tier"],  # Required claims
                "verify_signature": True,
                "verify_exp": True,
                "verify_iat": True,
            }
        )
        
        return {"valid": True, "payload": payload}
        
    except jwt.ExpiredSignatureError:
        return {"valid": False, "error": "Token has expired"}
    except jwt.InvalidSignatureError:
        return {"valid": False, "error": "Invalid token signature - token may be forged"}
    except jwt.DecodeError:
        return {"valid": False, "error": "Token decode failed - invalid format"}
    except jwt.MissingRequiredClaimError as e:
        return {"valid": False, "error": f"Missing required claim: {e}"}
    except jwt.InvalidTokenError:
        return {"valid": False, "error": "Invalid token"}
    except Exception as e:
        return {"valid": False, "error": f"Token verification failed: {str(e)}"}


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
    
    # Verify JWT signature and decode
    result = verify_jwt(token)
    
    if not result.get("valid"):
        return {
            "valid": False,
            "error": result.get("error", "Token validation failed"),
            "action": "Run: smf login"
        }
    
    payload = result["payload"]
    
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
    tier_levels = {"free": 0, "pro": 1, "enterprise": 2}
    
    if tier_levels.get(tier, 0) < tier_levels.get(min_tier, 1):
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


# Legacy function - kept for compatibility but NOT USED by secure code
def decode_jwt_without_verification(token: str) -> Dict:
    """
    DEPRECATED: This function does NOT verify signatures.
    Use verify_jwt() instead for secure token validation.
    """
    raise RuntimeError(
        "decode_jwt_without_verification is deprecated and insecure. "
        "Use verify_jwt() for proper signature verification."
    )
