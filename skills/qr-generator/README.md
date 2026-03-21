# QR Code Generator

A QR code generation skill for OpenClaw. Create QR codes for URLs, WiFi, emails, and more.

## Features

- **URL QR Codes**: Link to websites
- **WiFi QR Codes**: Share network credentials
- **Email QR Codes**: Pre-filled email messages
- **Contact QR Codes**: vCard format
- **Phone/SMS QR Codes**: Quick dial or text
- **Multiple Formats**: PNG, SVG, JPEG output

## Installation

```bash
pip install qrcode[pil]
```

## Usage

### URL QR Code
```bash
python main.py url https://smf.works
python main.py url https://smf.works qr-code.png
```

### WiFi QR Code
```bash
python main.py wifi "MyNetwork" "password123"
python main.py wifi "MyNetwork" "password123" wifi-qr.png
```

### Email QR Code
```bash
python main.py email hello@example.com
python main.py email hello@example.com contact-email.png
```

### Phone QR Code
```bash
python main.py phone "+1234567890"
```

### vCard Contact
```bash
python main.py vcard "John Doe" "+1234567890"
python main.py vcard "John Doe" "+1234567890" "john@example.com"
```

### SMS QR Code
```bash
python main.py sms "+1234567890"
python main.py sms "+1234567890" "Hello!"
```

## Input Validation Limits

| Parameter | Limit |
|-----------|-------|
| Maximum data length | 2,000 characters |
| Maximum QR size | 40 (box_size) |
| Maximum border | 10 boxes |
| SSID length | 32 characters |
| WiFi password | 63 characters |
| Output formats | PNG, SVG, JPG, JPEG |
| Phone validation | Digits, +, -, spaces, parentheses |

## Security Considerations

- **Data Sanitization**: Removes shell metacharacters from input
- **Path Traversal Protection**: Sanitizes output filenames
- **URL Validation**: Only allows http, https, mailto, tel schemes
- **Command Injection Prevention**: Blocks dangerous characters
- **Filename Sanitization**: Removes non-alphanumeric characters
- **Null Byte Protection**: Rejects null bytes in data

## Error Handling

Errors are categorized:
- **ImportError**: qrcode library not installed
- **ValueError**: Invalid URL format or data
- **OSError**: Cannot create output directory
- **Security Error**: Dangerous patterns detected

## Known Limitations

- Maximum 2,000 characters of data
- Requires qrcode library with PIL support
- Large data results in dense QR codes
- WiFi format follows de facto standard (not officially standardized)
- SSID/password escaping for WiFi may vary by device

## Examples

```bash
# Share your website
python main.py url https://smf.works

# Share WiFi credentials
python main.py wifi "GuestNetwork" "Welcome2024!"

# Create contact card
python main.py vcard "Jane Smith" "+15551234567" "jane@example.com"

# Quick SMS
python main.py sms "+15551234567" "Call me back!"
```
