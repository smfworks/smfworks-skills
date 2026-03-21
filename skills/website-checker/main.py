#!/usr/bin/env python3
"""
Website Checker Skill for OpenClaw
Check website status, response time, and SSL certificates.
"""

import sys
import ssl
import socket
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse


def check_url(url: str, timeout: int = 10) -> Dict:
    """
    Check if URL is accessible.
    
    Args:
        url: URL to check
        timeout: Request timeout in seconds
    
    Returns:
        Dict with check results
    """
    try:
        import requests
        
        # Ensure URL has scheme
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
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
            "error": str(e)
        }
    except ImportError:
        return {"success": False, "error": "requests not installed. Run: pip install requests"}


def check_ssl_certificate(domain: str, port: int = 443) -> Dict:
    """
    Check SSL certificate information.
    
    Args:
        domain: Domain to check
        port: Port number (default: 443)
    
    Returns:
        Dict with SSL certificate info
    """
    try:
        # Remove scheme if present
        domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
        
        context = ssl.create_default_context()
        with socket.create_connection((domain, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                version = ssock.version()
                
                # Parse dates
                not_after = cert.get('notAfter')
                not_before = cert.get('notBefore')
                
                expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                days_until_expiry = (expiry_date - datetime.now()).days
                
                return {
                    "success": True,
                    "domain": domain,
                    "subject": cert.get('subject'),
                    "issuer": cert.get('issuer'),
                    "not_before": not_before,
                    "not_after": not_after,
                    "days_until_expiry": days_until_expiry,
                    "expiry_status": "critical" if days_until_expiry < 7 else "warning" if days_until_expiry < 30 else "good",
                    "tls_version": version,
                    "cipher": cipher[0] if cipher else "unknown"
                }
                
    except ssl.SSLError as e:
        return {"success": False, "domain": domain, "error": f"SSL Error: {str(e)}"}
    except socket.error as e:
        return {"success": False, "domain": domain, "error": f"Connection Error: {str(e)}"}
    except Exception as e:
        return {"success": False, "domain": domain, "error": str(e)}


def check_bulk_urls(urls: List[str]) -> List[Dict]:
    """
    Check multiple URLs at once.
    
    Args:
        urls: List of URLs to check
    
    Returns:
        List of check results
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
        return f"❌ {url} - DOWN ({result.get('error', 'Unknown error')})"
    
    status_icon = "✅" if result["status"] == "up" else "⚠️"
    return f"{status_icon} {url} - {result['status_code']} ({result['response_time_ms']}ms)"


def main():
    """CLI interface for website checker."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [options]")
        print("")
        print("Commands:")
        print("  check <url>                           - Check single URL")
        print("  ssl <domain>                          - Check SSL certificate")
        print("  bulk <url1> <url2> ...                 - Check multiple URLs")
        print("")
        print("Examples:")
        print("  python main.py check https://google.com")
        print("  python main.py ssl smf.works")
        print("  python main.py bulk https://google.com https://github.com")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        if len(sys.argv) < 3:
            print("Error: check requires URL")
            sys.exit(1)
        
        url = sys.argv[2]
        result = check_url(url)
        
        if result["success"]:
            status_icon = "✅" if result["status"] == "up" else "⚠️"
            print(f"{status_icon} {result['url']}")
            print(f"   Status: {result['status_code']}")
            print(f"   Response time: {result['response_time_ms']}ms")
            if result['final_url'] != result['url']:
                print(f"   Redirected to: {result['final_url']}")
        else:
            print(f"❌ Failed to check {url}")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    
    elif command == "ssl":
        if len(sys.argv) < 3:
            print("Error: ssl requires domain")
            sys.exit(1)
        
        domain = sys.argv[2]
        result = check_ssl_certificate(domain)
        
        if result["success"]:
            status_icon = "✅" if result["expiry_status"] == "good" else "⚠️" if result["expiry_status"] == "warning" else "🔴"
            print(f"{status_icon} SSL Certificate: {result['domain']}")
            print(f"   Issuer: {result['issuer']}")
            print(f"   Expires: {result['not_after']}")
            print(f"   Days until expiry: {result['days_until_expiry']}")
            print(f"   TLS Version: {result['tls_version']}")
        else:
            print(f"❌ SSL Check Failed")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    
    elif command == "bulk":
        if len(sys.argv) < 4:
            print("Error: bulk requires at least 2 URLs")
            sys.exit(1)
        
        urls = sys.argv[2:]
        print(f"Checking {len(urls)} URLs...")
        print("")
        
        for url in urls:
            print(get_status_summary(url))
    
    else:
        print(f"Unknown command: {command}")
        print("Run without arguments for usage help")
        sys.exit(1)


if __name__ == "__main__":
    main()
