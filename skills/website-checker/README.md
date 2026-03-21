# Website Checker

A website monitoring skill for OpenClaw. Check URL accessibility, response times, and SSL certificate status.

## Features

- **URL Check**: Test if websites are accessible and measure response times
- **SSL Certificate Check**: Verify SSL certificates and check expiration dates
- **Bulk Checking**: Check multiple URLs at once

## Installation

```bash
# Install requests dependency
pip install requests
```

## Usage

### Check Single URL
```bash
python main.py check https://example.com

# With custom timeout (1-300 seconds)
python main.py check https://example.com --timeout 30
```

Output:
```
✅ https://example.com
   Status: 200
   Response time: 245.67ms
   Redirected to: https://www.example.com (if applicable)
```

### Check SSL Certificate
```bash
# Default port (443)
python main.py ssl example.com

# Custom port
python main.py ssl example.com 8443
```

Output:
```
✅ SSL Certificate: example.com
   Issuer: (('organizationName', "Let's Encrypt"), ...)
   Expires: Mar 20 12:00:00 2025 GMT
   Days until expiry: 365
   TLS Version: TLSv1.3
```

### Check Multiple URLs
```bash
python main.py bulk https://google.com https://github.com https://stackoverflow.com
```

Output:
```
✅ https://google.com - 200 (45.23ms)
✅ https://github.com - 200 (123.45ms)
❌ https://broken-site.com - DOWN (Connection timeout)
```

## Input Validation Limits

| Parameter | Limit |
|-----------|-------|
| Default timeout | 10 seconds |
| Minimum timeout | 1 second |
| Maximum timeout | 300 seconds (5 minutes) |
| Port range | 1-65535 |

## Security Considerations

- **SSRF Protection**: Blocks access to:
  - Localhost (127.0.0.1, ::1, localhost)
  - Private IP ranges (10.x.x.x, 192.168.x.x, etc.)
  - Loopback addresses
  - Link-local addresses
  - Non-HTTP schemes (file://, ftp://, etc.)

- **URL Validation**: All URLs are validated before making requests
- **Port Validation**: Custom ports must be within valid range (1-65535)
- **Timeout Protection**: Prevents indefinite hanging on slow connections

## Error Handling

The tool provides categorized error messages:
- **SSL Error**: Certificate or TLS negotiation issues
- **Connection Timeout**: Server not responding
- **Connection Error**: Network or DNS issues
- **SSRF Protection**: Blocked for security reasons

## Known Limitations

- Self-signed certificates will show SSL errors
- Some sites may block automated requests
- Response time includes DNS resolution and connection establishment
- Certificate information requires successful SSL handshake

## SSL Status Indicators

| Icon | Status | Days Until Expiry |
|------|--------|-------------------|
| ✅ | Good | 30+ days |
| ⚠️ | Warning | 7-30 days |
| 🔴 | Critical | < 7 days |
