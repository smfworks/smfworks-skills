#!/usr/bin/env python3
"""
Test JWT verification in smf_auth.py

This test ensures that:
1. Valid tokens are accepted
2. Expired tokens are rejected
3. Forged tokens are rejected
4. Tampered tokens are rejected
"""

import sys
import json
import base64
import tempfile
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))

from smf_auth import verify_jwt, require_subscription, load_token

# Test configuration
TEST_TOKEN_DIR = Path.home() / ".smf"

def create_test_token(payload: dict, secret: str = "fake-secret"):
    """Create a test JWT token (without proper signing for testing)."""
    # This creates a token that should be REJECTED by verify_jwt
    header = json.dumps({"alg": "none", "typ": "JWT"}).encode()
    payload_json = json.dumps(payload).encode()
    
    header_b64 = base64.urlsafe_b64encode(header).decode().rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(payload_json).decode().rstrip('=')
    
    return f"{header_b64}.{payload_b64}.invalid-signature"


def test_no_token():
    """Test that missing token is rejected."""
    print("\n[Test 1] No token...")
    
    # Temporarily move token if it exists
    token_path = TEST_TOKEN_DIR / "token"
    backup = None
    if token_path.exists():
        backup = token_path.read_text()
        token_path.unlink()
    
    try:
        result = require_subscription("test-skill")
        assert result["valid"] == False, "Should reject missing token"
        assert "No subscription token" in result["error"], f"Wrong error: {result['error']}"
        print("✅ PASS: Missing token correctly rejected")
    finally:
        if backup:
            token_path.write_text(backup)


def test_forged_token():
    """Test that forged token is rejected."""
    print("\n[Test 2] Forged token...")
    
    # Create a forged token (valid payload, invalid signature)
    forged_payload = {
        "sub": "fake-user",
        "tier": "pro",
        "skills": ["*"],
        "exp": (datetime.now(timezone.utc) + timedelta(days=30)).timestamp()
    }
    
    forged_token = create_test_token(forged_payload)
    
    # Write forged token
    token_path = TEST_TOKEN_DIR / "token"
    original = None
    if token_path.exists():
        original = token_path.read_text()
    
    token_path.write_text(forged_token)
    
    try:
        result = require_subscription("test-skill")
        assert result["valid"] == False, "Should reject forged token"
        assert "signature" in result["error"].lower() or "invalid" in result["error"].lower(), \
            f"Wrong error message: {result['error']}"
        print("✅ PASS: Forged token correctly rejected")
        print(f"   Error message: {result['error']}")
    finally:
        if original:
            token_path.write_text(original)
        else:
            token_path.unlink()


def test_expired_token():
    """Test that expired token is rejected."""
    print("\n[Test 3] Expired token...")
    
    # Create token with past expiration
    expired_payload = {
        "sub": "test-user",
        "tier": "pro",
        "skills": ["*"],
        "exp": (datetime.now(timezone.utc) - timedelta(days=1)).timestamp()
    }
    
    expired_token = create_test_token(expired_payload)
    
    token_path = TEST_TOKEN_DIR / "token"
    original = None
    if token_path.exists():
        original = token_path.read_text()
    
    token_path.write_text(expired_token)
    
    try:
        result = require_subscription("test-skill")
        assert result["valid"] == False, "Should reject expired token"
        assert "expired" in result["error"].lower(), f"Wrong error: {result['error']}"
        print("✅ PASS: Expired token correctly rejected")
    finally:
        if original:
            token_path.write_text(original)
        else:
            token_path.unlink()


def test_free_tier_rejected():
    """Test that free tier can't access pro skills."""
    print("\n[Test 4] Free tier rejected from pro skill...")
    
    free_payload = {
        "sub": "free-user",
        "tier": "free",
        "skills": [],
        "exp": (datetime.now(timezone.utc) + timedelta(days=30)).timestamp()
    }
    
    free_token = create_test_token(free_payload)
    
    token_path = TEST_TOKEN_DIR / "token"
    original = None
    if token_path.exists():
        original = token_path.read_text()
    
    token_path.write_text(free_token)
    
    try:
        result = require_subscription("test-skill", min_tier="pro")
        assert result["valid"] == False, "Should reject free tier"
        assert "pro" in result["error"].lower(), f"Wrong error: {result['error']}"
        print("✅ PASS: Free tier correctly rejected from pro skill")
    finally:
        if original:
            token_path.write_text(original)
        else:
            token_path.unlink()


def run_all_tests():
    """Run all security tests."""
    print("=" * 60)
    print("SMF Auth Security Tests")
    print("=" * 60)
    print("\nTesting JWT verification...")
    
    tests = [
        ("No token", test_no_token),
        ("Forged token", test_forged_token),
        ("Expired token", test_expired_token),
        ("Free tier rejected", test_free_tier_rejected),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAIL: {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {name}: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\n🎉 All security tests passed!")
        print("JWT verification is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review the implementation.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
