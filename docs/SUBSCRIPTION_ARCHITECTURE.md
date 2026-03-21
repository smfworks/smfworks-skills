# SMF Works Skills - Subscription Validation Architecture

**Date:** 2026-03-20  
**Purpose:** License/Auth system for free vs paid skills  
**Status:** Architecture design

---

## Requirements

### Functional Requirements

1. **Free Skills:** Work forever, no authentication required
2. **Paid Skills:** Require valid subscription token
3. **Token Format:** Unique per subscriber, contains tier/expiration info
4. **Revocation:** If subscription stops, paid skills stop working
5. **Graceful Degradation:** Free skills continue working if subscription lapses
6. **Offline Capability:** Skills work offline with cached validation
7. **Security:** Token cannot be easily forged or shared

### Non-Functional Requirements

- ✅ Low latency (don't slow down skill execution)
- ✅ Minimal dependencies (skills should be lightweight)
- ✅ No hardcoded secrets in skills
- ✅ Easy to implement in each skill
- ✅ Works with OpenClaw skill structure

---

## Architecture Options

### Option 1: JWT Token with Remote Validation ⭐ RECOMMENDED

**How it works:**
1. Subscriber gets JWT token upon signup
2. Token contains: subscriber_id, tier, expiration, permissions
3. Each paid skill validates token locally (cryptographically)
4. Skills periodically check subscription status via API (cached)
5. On revocation, token becomes invalid

**Token Format (JWT):**
```json
{
  "sub": "sub_abc123",           // Subscriber ID
  "tier": "pro",                 // free, pro, enterprise
  "skills": ["*"],               // ["*"] = all, or ["skill1", "skill2"]
  "iat": 1704067200,            // Issued at
  "exp": 1735689600,            // Expires at
  "jti": "unique-token-id"      // Token ID for revocation
}
```

**Validation Flow:**
```
Skill Execution
    ↓
Check if Paid Skill
    ↓
Load Token from ~/.smf/token
    ↓
Verify JWT Signature (local, fast)
    ↓
Check Expiration
    ↓
Check if Skill in Allowed List
    ↓
[Optional] Check Revocation List (cached)
    ↓
Execute Skill or Show "Subscription Required"
```

**Pros:**
- ✅ Fast (local signature verification)
- ✅ Secure (JWT cannot be forged without secret)
- ✅ Works offline (signature check is local)
- ✅ Standard format (industry standard)
- ✅ Easy to implement (libraries exist)

**Cons:**
- ⚠️ Need revocation mechanism (separate from expiration)
- ⚠️ Token can be shared (mitigated by rate limiting/subscriber tracking)

**Implementation:**
```python
import jwt
from datetime import datetime

def validate_subscription(skill_name: str) -> dict:
    """Validate subscription for a skill."""
    token_path = Path.home() / ".smf" / "token"
    
    if not token_path.exists():
        return {"valid": False, "reason": "No subscription token found"}
    
    try:
        with open(token_path) as f:
            token = f.read().strip()
        
        # Verify token (local, fast)
        payload = jwt.decode(
            token,
            key=SMF_PUBLIC_KEY,  # Public key for verification
            algorithms=["RS256"]
        )
        
        # Check expiration
        if datetime.now().timestamp() > payload["exp"]:
            return {"valid": False, "reason": "Subscription expired"}
        
        # Check if skill is allowed
        allowed_skills = payload.get("skills", [])
        if "*" not in allowed_skills and skill_name not in allowed_skills:
            return {"valid": False, "reason": "Skill not included in subscription"}
        
        # Check revocation (cached, optional)
        if is_token_revoked(payload["jti"]):
            return {"valid": False, "reason": "Subscription revoked"}
        
        return {
            "valid": True,
            "subscriber_id": payload["sub"],
            "tier": payload["tier"]
        }
        
    except jwt.ExpiredSignatureError:
        return {"valid": False, "reason": "Token expired"}
    except jwt.InvalidTokenError:
        return {"valid": False, "reason": "Invalid token"}
    except Exception as e:
        return {"valid": False, "reason": f"Validation error: {str(e)}"}
```

---

### Option 2: API Key with Local Validation

**How it works:**
1. Each subscriber gets unique API key
2. Skills hash the key and check against embedded hash
3. Periodic online validation to check revocation

**Pros:**
- ✅ Simple to understand
- ✅ Can implement revocation quickly

**Cons:**
- ❌ Requires online check for revocation
- ❌ Simpler format (easier to forge if not careful)
- ❌ Harder to encode permissions

---

### Option 3: GitHub-Based Access Control

**How it works:**
1. Use GitHub as authentication mechanism
2. Subscriber authenticates with GitHub
3. We check if they're in subscriber list
4. Grant access based on GitHub username

**Pros:**
- ✅ No custom auth system
- ✅ Users already have GitHub accounts

**Cons:**
- ❌ Requires internet connection
- ❌ Slower (API calls to GitHub)
- ❌ Dependency on GitHub availability
- ❌ Harder to implement per-skill permissions

---

### Option 4: License File with Hardware Binding

**How it works:**
1. Generate license file with machine fingerprint
2. Bind to specific hardware
3. License file contains expiration and permissions

**Pros:**
- ✅ Hard to share (bound to machine)
- ✅ Works offline completely

**Cons:**
- ❌ Harder for users (license management)
- ❌ Machine migration is painful
- ❌ Overkill for this use case

---

## Recommended Architecture: JWT with Revocation

### Components

#### 1. Token Issuance (SMF Backend)

**When:**
- New subscriber signs up
- Subscription renews
- Token needs refresh (monthly)

**Process:**
```python
def issue_token(subscriber_id: str, tier: str) -> str:
    """Issue new subscription token."""
    payload = {
        "sub": subscriber_id,
        "tier": tier,
        "skills": ["*"] if tier == "pro" else ["free_tier_skills"],
        "iat": datetime.now(),
        "exp": datetime.now() + timedelta(days=30),  // Monthly refresh
        "jti": str(uuid.uuid4())  // Unique token ID
    }
    
    token = jwt.encode(
        payload,
        key=SMF_PRIVATE_KEY,  // Private key for signing
        algorithm="RS256"
    )
    
    # Store token ID in database for revocation
    store_token_jti(payload["jti"], subscriber_id)
    
    return token
```

#### 2. Token Storage (Client Side)

**Location:** `~/.smf/token`
**Permissions:** 0600 (user read/write only)
**Format:** Raw JWT string

#### 3. Token Validation (In Each Skill)

**Shared library:** `shared/smf_auth.py`

```python
#!/usr/bin/env python3
"""SMF Works subscription validation library."""

import jwt
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# SMF Works public key (embedded in skills)
SMF_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
-----END PUBLIC KEY-----"""

class SMFAuth:
    """Subscription validation for SMF Works skills."""
    
    def __init__(self, skill_name: str, is_paid: bool = True):
        self.skill_name = skill_name
        self.is_paid = is_paid
        self.token_path = Path.home() / ".smf" / "token"
        self.revocation_cache_path = Path.home() / ".smf" / "revocation_cache.json"
    
    def validate(self) -> Dict:
        """
        Validate subscription for this skill.
        
        Returns:
            Dict with 'valid' (bool), 'reason' (str), and subscriber info
        """
        # Free skills don't need validation
        if not self.is_paid:
            return {"valid": True, "tier": "free", "reason": "Free skill"}
        
        # Check if token exists
        if not self.token_path.exists():
            return {
                "valid": False,
                "reason": "No subscription found. Get Pro at https://smf.works",
                "action": "subscribe"
            }
        
        try:
            # Load token
            with open(self.token_path, 'r') as f:
                token = f.read().strip()
            
            # Verify JWT (local, fast)
            payload = jwt.decode(
                token,
                key=SMF_PUBLIC_KEY,
                algorithms=["RS256"]
            )
            
            # Check if token is revoked (cached check)
            if self._is_revoked(payload.get("jti")):
                return {
                    "valid": False,
                    "reason": "Subscription revoked. Resubscribe at https://smf.works",
                    "action": "resubscribe"
                }
            
            # Check if skill is allowed
            allowed_skills = payload.get("skills", [])
            if "*" not in allowed_skills and self.skill_name not in allowed_skills:
                return {
                    "valid": False,
                    "reason": f"'{self.skill_name}' not included in your subscription",
                    "action": "upgrade"
                }
            
            return {
                "valid": True,
                "subscriber_id": payload["sub"],
                "tier": payload["tier"],
                "expires": payload["exp"]
            }
            
        except jwt.ExpiredSignatureError:
            return {
                "valid": False,
                "reason": "Subscription expired. Renew at https://smf.works",
                "action": "renew"
            }
        except jwt.InvalidTokenError:
            return {
                "valid": False,
                "reason": "Invalid subscription token. Reinstall from https://smf.works",
                "action": "reinstall"
            }
        except Exception as e:
            return {
                "valid": False,
                "reason": f"Error validating subscription: {str(e)}",
                "action": "contact_support"
            }
    
    def _is_revoked(self, jti: str) -> bool:
        """Check if token ID is revoked (with caching)."""
        # TODO: Implement revocation check
        # For now, return False (no revocation)
        # In production:
        # 1. Check local cache (updated hourly)
        # 2. If cache stale or not found, query SMF API
        # 3. Update cache with result
        return False
    
    def require_subscription(self):
        """
        Decorator-like function to enforce subscription.
        Raises exception if not valid.
        """
        result = self.validate()
        if not result["valid"]:
            raise PermissionError(result["reason"])
        return result


# Convenience function
def check_subscription(skill_name: str, is_paid: bool = True) -> Dict:
    """Quick check function."""
    auth = SMFAuth(skill_name, is_paid)
    return auth.validate()
```

#### 4. Revocation Mechanism

**Process:**
1. Subscriber cancels subscription
2. Backend adds token JTI to revocation list
3. Skills check revocation list periodically (cached)
4. Revoked tokens = paid skills stop working

**Implementation:**
```python
# Backend revocation endpoint
def revoke_token(subscriber_id: str):
    """Revoke all tokens for a subscriber."""
    # Get all active JTIs for subscriber
    jtis = get_active_tokens(subscriber_id)
    
    # Add to revocation list with timestamp
    for jti in jtis:
        add_to_revocation_list(jti, revoked_at=datetime.now())
    
    # Invalidate cache
    invalidate_revocation_cache()
```

---

## Skill Implementation Pattern

### Free Skill

```python
from smf_auth import check_subscription

def main():
    # Free skills just work
    result = check_subscription("file-organizer", is_paid=False)
    
    # No validation needed, but we can log
    if result["valid"]:
        print(f"✅ Running file-organizer (Free skill)")
    
    # Execute skill logic...
```

### Paid Skill

```python
from smf_auth import check_subscription, SMFAuth

def main():
    # Check subscription
    auth = SMFAuth("lead-capture", is_paid=True)
    
    try:
        subscription = auth.require_subscription()
        print(f"✅ Subscription valid: {subscription['tier']} tier")
        
        # Execute paid skill logic...
        
    except PermissionError as e:
        print(f"❌ {e}")
        print("\nGet Pro subscription at https://smf.works")
        print("Free skills available: file-organizer, pdf-toolkit, qr-generator")
        sys.exit(1)
```

---

## User Flow

### 1. Free User
```
Install skill → Works immediately → No token needed
```

### 2. Pro Subscriber
```
Subscribe on website → Get token → Install token (~/.smf/token)
                                    ↓
Install paid skill → Validate token → Works!
                                    ↓
Monthly refresh → New token issued → Replace old token
                                    ↓
Cancel subscription → Token revoked → Paid skills stop
                                    ↓
Free skills continue working!
```

---

## Security Considerations

### Token Security
- ✅ Use RS256 (RSA with SHA-256) — private key signs, public key verifies
- ✅ Embed public key in skills (can't be changed by users)
- ✅ Keep private key secure (only on SMF backend)
- ✅ Short expiration (30 days) with refresh
- ✅ Unique JTI for revocation tracking

### Revocation Security
- ✅ Revocation list signed/tamper-proof
- ✅ Cache locally to prevent spam
- ✅ Check on each execution (fast local check)

### User Experience
- ✅ Clear error messages with action items
- ✅ Link to subscription page
- ✅ Remind about free skills
- ✅ Grace period for expired tokens (24 hours)

---

## Implementation Steps

### Step 1: Create Auth Library
- [ ] Generate RSA key pair
- [ ] Create `shared/smf_auth.py`
- [ ] Implement token validation
- [ ] Add revocation checking

### Step 2: Backend API
- [ ] `/api/token/issue` — Issue new token
- [ ] `/api/token/refresh` — Refresh expiring token
- [ ] `/api/token/revoke` — Revoke token (on cancellation)
- [ ] `/api/revocation-list` — Get revocation list (for cache)

### Step 3: Token Distribution
- [ ] Add to subscriber onboarding flow
- [ ] CLI command: `smf login` (downloads token)
- [ ] Website: "Copy token to ~/.smf/token"

### Step 4: Skill Updates
- [ ] Add auth check to each paid skill
- [ ] Test free skills work without token
- [ ] Test paid skills fail gracefully without token

---

## Alternative: Simple API Key (MVP)

For faster MVP, could use simpler approach:

```python
# Simple API key validation
import hashlib
import requests

def validate_simple(skill_name: str, api_key: str) -> bool:
    """Simple API key validation."""
    # Hash the key locally
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    # Check against backend (cached)
    response = requests.post(
        "https://api.smf.works/v1/validate",
        json={"key_hash": key_hash, "skill": skill_name},
        timeout=2
    )
    
    return response.json().get("valid", False)
```

**Trade-off:** Simpler but requires internet connection for validation.

---

## Recommendation

**Go with JWT (Option 1)** because:
- Industry standard (well understood)
- Fast (local verification)
- Secure (cryptographic verification)
- Flexible (can encode permissions)
- Works offline (signature check is local)

**MVP Approach:**
1. Start with JWT validation (no revocation for MVP)
2. Add revocation list in Month 2
3. Optimize caching in Month 3

---

*Architecture designed: 2026-03-20*  
*Ready for implementation*  
*Next: Build auth library, then resume skill development*
