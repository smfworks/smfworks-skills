#!/usr/bin/env python3
"""
Website Checker Skill for OpenClaw
Check website status, response time, and SSL certificates.

Examples:
    python main.py check https://example.com
    python main.py check https://example.com --timeout 30
    python main.py ssl smf.works
    python main.py bulk https://google.com https://github.com
"""

import sys
import ssl
import socket
import ipaddress
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse

# Module-level constants
DEFAULT_TIMEOUT = 10
MIN_TIMEOUT = 1
MAX_TIMEOUT = 300
MIN_PORT = 1
MAX_PORT = 65535
CRITICAL_DAYS = 7
WARNING_DAYS = 30
LOCALHOST_NAMES = {'localhost', '127.0.0.1', '0.0.0.0', '::1', '[::1]'}
VALID_SCHEMES = {'http', 'https'}
ERROR_PREFIX = "❌"
SUCCESS_PREFIX = "✅"
WARNING_PREFIX = "⚠️"


def validate_positive_int(value: str, name: str, min_val: int = 0, max_val: int = 999999) -> Tuple[bool, int, str]:
    """
    Validate that a value is a positive integer within range.
    
    Args:
        value: The value to validate
        name: Name of the parameter (for error messages)
        min_val: Minimum allowed value
        max_val: Maximum allowed value
    
    Returns:
        (is_valid, int_value, error_message)
    
    Example:
        >>> validate_positive_int("30", "timeout", 1, 300)
        (True, 30, "")
        >>> validate_positive_int("abc", "timeout")
        (False, 0, "timeout must be an integer, got: abc")
    """
    try:
        int_val = int(value)
    except ValueError:
        return False, 0, f"{name} must be an integer, got: {value}"
    
    if int_val < min_val:
        return False, 0, f"{name} must be at least {min_val}, got: {int_val}"
    
    if int_val > max_val:
        return False, 0, f"{name} must be at most {max_val}, got: {int_val}"
    
    return True, int_val, ""


def _is_safe_url(url: str) -> Tuple[bool, str]:
    """
    Validate URL to prevent SSRF attacks.
    Blocks private IP ranges, localhost, and file:// URLs.
    
    Args:
        url: URL to validate
    
    Returns:
        Tuple of (is_safe, error_message)
    
    Example:
        >>> _is_safe_url("https://example.com")
        (True, "")
        >>> _is_safe_url("http://localhost/admin")
        (False, "Access to localhost is not allowed")
    """
    try:
        parsed = urlparse(url)
        
        # Block file:// and other non-http schemes
        if parsed.scheme and parsed.scheme not in VALID_SCHEMES:
            return False, f"URL scheme '{parsed.scheme}' is not allowed"
        
        # Get hostname
        hostname = parsed.hostname or ''
        
        # Block localhost variants
        if hostname.lower() in LOCALHOST_NAMES or hostname.startswith('127.') or hostname.startswith('0.'):
            return False, "Access to localhost is not allowed"
        
        # Block private/internal IP ranges
        try:
            # Try to parse as IP address
            ip = ipaddress.ip_address(hostname)
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
                return False, "Access to internal IP addresses is not allowed"
        except ValueError:
            # Not an IP address, it's a hostname - that's fine
            pass
        
        return True, ""
    except Exception as e:
        return False, f"URL validation error: {type(e).__name__}: {e}"


def check_url(url: str, timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Union[bool, str, int, float]]:
    """
    Check if URL is accessible.
    
    Args:
        url: URL to check
        timeout: Request timeout in seconds
    
    Returns:
        Dict with check results
    
    Example:
        >>> check_url("https://example.com")
        {'success': True, 'url': 'https://example.com', 'status_code': 200, ...}
    """
    try:
        import requests
        
        # Ensure URL has scheme
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # SSRF Protection: Validate URL before requesting
        is_safe, error_msg = _is_safe_url(url)
        if not is_safe:
            return {
                "success": False,
                "url": url,
                "status": "blocked",
                "error": f"SSRF Protection: {error_msg}"
            }
        
        start_time = datetime.now()
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        end_time = datetime.now()
        
        response_time = (end_time - start_time).total_seconds() * 1000  # milliseconds
        
        return {
            "success": True,
            "url": url,
            "status_code": response.status_code,
            "status": "up" if response.status_code < 400 else "error",
            "response_time_ms": round(response_time, 2),
            "final_url": response.url,
            "headers": dict(response.headers)
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "url": url,
            "status": "down",
            "error": f"Request failed: {type(e).__name__}: {e}"
        }
    except ImportError:
        return {"success": False, "error": "requests not installed. Run: pip install requests"}


def check_ssl_certificate(domain: str, port: int = 443) -> Dict[str, Union[bool, str, int]]:
    """
    Check SSL certificate information.
    
    Args:
        domain: Domain to check
        port: Port number (default: 443)
    
    Returns:
        Dict with SSL certificate info
    
    Example:
        >>> check_ssl_certificate("example.com")
        {'success': True, 'domain': 'example.com', 'days_until_expiry': 365, ...}
    """
    try:
        # Properly parse domain using urlparse
        if '://' in domain:
            parsed = urlparse(domain)
        else:
            parsed = urlparse(f"https://{domain}")
        
        hostname = parsed.hostname
        if not hostname:
            return {"success": False, "domain": domain, "error": "Invalid domain"}
        
        # Validate port using the validation helper
        is_valid, port, error = validate_positive_int(str(port), "port", MIN_PORT, MAX_PORT)
        if not is_valid:
            return {"success": False, "domain": hostname, "error": error}
        
        # SSRF Protection: Check if hostname is safe
        is_safe, error_msg = _is_safe_url(f"https://{hostname}")
        if not is_safe:
            return {
                "success": False,
                "domain": hostname,
                "error": f"SSRF Protection: {error_msg}"
            }
        
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                version = ssock.version()
                
                # Parse dates
                not_after = cert.get('notAfter')
                not_before = cert.get('notBefore')
                
                expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                days_until_expiry = (expiry_date - datetime.now()).days
                
                if days_until_expiry < CRITICAL_DAYS:
                    expiry_status = "critical"
                elif days_until_expiry < WARNING_DAYS:
                    expiry_status = "warning"
                else:
                    expiry_status = "good"
                
                return {
                    "success": True,
                    "domain": domain,
                    "subject": cert.get('subject'),
                    "issuer": cert.get('issuer'),
                    "not_before": not_before,
                    "not_after": not_after,
                    "days_until_expiry": days_until_expiry,
                    "expiry_status": expiry_status,
                    "tls_version": version,
                    "cipher": cipher[0] if cipher else "unknown"
                }
                
    except ssl.SSLError as e:
        return {"success": False, "domain": domain, "error": f"SSL Error: {type(e).__name__}: {e}"}
    except socket.timeout:
        return {"success": False, "domain": domain, "error": "Connection timeout"}
    except socket.error as e:
        return {"success": False, "domain": domain, "error": f"Connection Error: {type(e).__name__}: {e}"}
    except Exception as e:
        return {"success": False, "domain": domain, "error": f"Unexpected error: {type(e).__name__}: {e}"}


def check_bulk_urls(urls: List[str]) -> List[Dict]:
    """
    Check multiple URLs at once.
    
    Args:
        urls: List of URLs to check
    
    Returns:
        List of check results
    
    Example:
        >>> check_bulk_urls(["https://example.com", "https://test.com"])
        [{'success': True, ...}, {'success': True, ...}]
    """
    results = []
    for url in urls:
        result = check_url(url)
        results.append(result)
    return results


def get_status_summary(url: str) -> str:
    """
    Get a human-readable status summary.
    
    Args:
        url: URL to check
    
    Returns:
        Status summary string
    """
    result = check_url(url)
    
    if not result["success"]:
        return f"{ERROR_PREFIX} {url} - DOWN ({result.get('error', 'Unknown error')})"
    
    status_icon = SUCCESS_PREFIX if result["status"] == "up" else WARNING_PREFIX
    return f"{status_icon} {url} - {result['status_code']} ({result['response_time_ms']}ms)"


def main():
    """CLI interface for website checker."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [options]")
        print("")
        print("Commands:")
        print("  check <url> [--timeout N]            - Check single URL")
        print("  ssl <domain> [port]                  - Check SSL certificate")
        print("  bulk <url1> <url2> ...               - Check multiple URLs")
        print("")
        print("Examples:")
        print("  python main.py check https://google.com")
        print("  python main.py check https://google.com --timeout 30")
        print("  python main.py ssl smf.works")
        print("  python main.py ssl smf.works 8443")
        print("  python main.py bulk https://google.com https://github.com")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        if len(sys.argv) < 3:
            print(f"{ERROR_PREFIX} Error: check requires URL")
            sys.exit(1)
        
        url = sys.argv[2]
        timeout = DEFAULT_TIMEOUT
        
        # Parse optional --timeout flag
        if "--timeout" in sys.argv:
            timeout_idx = sys.argv.index("--timeout")
            if timeout_idx + 1 < len(sys.argv):
                is_valid, timeout, error = validate_positive_int(
                    sys.argv[timeout_idx + 1], "timeout", MIN_TIMEOUT, MAX_TIMEOUT
                )
                if not is_valid:
                    print(f"{ERROR_PREFIX} {error}")
                    sys.exit(1)
            else:
                print(f"{ERROR_PREFIX} Error: --timeout requires a value")
                sys.exit(1)
        
        result = check_url(url, timeout)
        
        if result["success"]:
            status_icon = SUCCESS_PREFIX if result["status"] == "up" else WARNING_PREFIX
            print(f"{status_icon} {result['url']}")
            print(f"   Status: {result['status_code']}")
            print(f"   Response time: {result['response_time_ms']}ms")
            if result['final_url'] != result['url']:
                print(f"   Redirected to: {result['final_url']}")
        else:
            print(f"{ERROR_PREFIX} Failed to check {url}")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    
    elif command == "ssl":
        if len(sys.argv) < 3:
            print(f"{ERROR_PREFIX} Error: ssl requires domain")
            sys.exit(1)
        
        domain = sys.argv[2]
        port = 443
        
        # Optional port argument with validation
        if len(sys.argv) >= 4:
            is_valid, port, error = validate_positive_int(
                sys.argv[3], "port", MIN_PORT, MAX_PORT
            )
            if not is_valid:
                print(f"{ERROR_PREFIX} {error}")
                sys.exit(1)
        
        result = check_ssl_certificate(domain, port)
        
        if result["success"]:
            if result["expiry_status"] == "good":
                status_icon = SUCCESS_PREFIX
            elif result["expiry_status"] == "warning":
                status_icon = WARNING_PREFIX
            else:
                status_icon = "🔴"
            print(f"{status_icon} SSL Certificate: {result['domain']}")
            print(f"   Issuer: {result['issuer']}")
            print(f"   Expires: {result['not_after']}")
            print(f"   Days until expiry: {result['days_until_expiry']}")
            print(f"   TLS Version: {result['tls_version']}")
        else:
            print(f"{ERROR_PREFIX} SSL Check Failed")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    
    elif command == "bulk":
        if len(sys.argv) < 4:
            print(f"{ERROR_PREFIX} Error: bulk requires at least 2 URLs")
            sys.exit(1)
        
        urls = sys.argv[2:]
        print(f"Checking {len(urls)} URLs...")
        print("")
        
        for url in urls:
            print(get_status_summary(url))
    
    else:
        print(f"{ERROR_PREFIX} Unknown command: {command}")
        print("Run without arguments for usage help")
        sys.exit(1)


if __name__ == "__main__":
    main()
