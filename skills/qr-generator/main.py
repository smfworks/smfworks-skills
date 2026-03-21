#!/usr/bin/env python3
"""
QR Code Generator Skill for OpenClaw
Generate QR codes for URLs, emails, WiFi, and more.
"""

import sys
from pathlib import Path
from typing import Dict, Optional


def generate_qr(data: str, output_file: str, size: int = 10, border: int = 4) -> Dict:
    """
    Generate QR code from data.
    
    Args:
        data: Data to encode in QR code
        output_file: Output file path (PNG or SVG)
        size: Box size in pixels
        border: Border size in boxes
    
    Returns:
        Dict with operation results
    """
    try:
        import qrcode
        from PIL import Image
        
        # Create QR code instance
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=size,
            border=border,
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        # Determine format
        if output_file.lower().endswith('.svg'):
            # Generate SVG
            import qrcode.image.svg
            factory = qrcode.image.svg.SvgImage
            img = qr.make_image(image_factory=factory)
        else:
            # Generate PNG (default)
            img = qr.make_image(fill_color="black", back_color="white")
        
        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Save
        img.save(output_file)
        
        return {
            "success": True,
            "output": output_file,
            "data": data,
            "size": f"{qr.modules_count}x{qr.modules_count}"
        }
        
    except ImportError:
        return {"success": False, "error": "qrcode not installed. Run: pip install qrcode[pil]"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_wifi_qr(ssid: str, password: str, security: str = "WPA", output_file: str = "wifi.png") -> Dict:
    """
    Generate WiFi connection QR code.
    
    Args:
        ssid: WiFi network name
        password: WiFi password
        security: Security type (WPA, WEP, or nopass)
        output_file: Output file path
    
    Returns:
        Dict with operation results
    """
    # WiFi QR format: WIFI:T:security;S:ssid;P:password;;
    wifi_data = f"WIFI:T:{security};S:{ssid};P:{password};;"
    
    return generate_qr(wifi_data, output_file)


def generate_email_qr(email: str, subject: str = "", body: str = "", output_file: str = "email.png") -> Dict:
    """
    Generate email QR code.
    
    Args:
        email: Email address
        subject: Email subject
        body: Email body
        output_file: Output file path
    
    Returns:
        Dict with operation results
    """
    # Email QR format: mailto:email?subject=...&body=...
    import urllib.parse
    
    params = {}
    if subject:
        params["subject"] = subject
    if body:
        params["body"] = body
    
    if params:
        query = urllib.parse.urlencode(params)
        email_data = f"mailto:{email}?{query}"
    else:
        email_data = f"mailto:{email}"
    
    return generate_qr(email_data, output_file)


def generate_phone_qr(phone: str, output_file: str = "phone.png") -> Dict:
    """
    Generate phone number QR code.
    
    Args:
        phone: Phone number
        output_file: Output file path
    
    Returns:
        Dict with operation results
    """
    # Phone QR format: tel:number
    phone_data = f"tel:{phone}"
    
    return generate_qr(phone_data, output_file)


def generate_vcard_qr(name: str, phone: str, email: str = "", output_file: str = "vcard.png") -> Dict:
    """
    Generate vCard QR code for contact.
    
    Args:
        name: Contact name
        phone: Phone number
        email: Email address
        output_file: Output file path
    
    Returns:
        Dict with operation results
    """
    # vCard format
    vcard_lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{name}",
        f"TEL:{phone}"
    ]
    
    if email:
        vcard_lines.append(f"EMAIL:{email}")
    
    vcard_lines.append("END:VCARD")
    
    vcard_data = "\n".join(vcard_lines)
    
    return generate_qr(vcard_data, output_file)


def generate_sms_qr(phone: str, message: str = "", output_file: str = "sms.png") -> Dict:
    """
    Generate SMS QR code.
    
    Args:
        phone: Phone number
        message: Default message
        output_file: Output file path
    
    Returns:
        Dict with operation results
    """
    # SMS QR format: sms:number?body=message
    import urllib.parse
    
    if message:
        encoded_message = urllib.parse.quote(message)
        sms_data = f"sms:{phone}?body={encoded_message}"
    else:
        sms_data = f"sms:{phone}"
    
    return generate_qr(sms_data, output_file)


def main():
    """CLI interface for QR code generator."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [options]")
        print("")
        print("Commands:")
        print("  url <url> [output.png]              - Generate URL QR code")
        print("  wifi <ssid> <password> [output.png]  - Generate WiFi QR code")
        print("  email <email> [output.png]          - Generate email QR code")
        print("  phone <number> [output.png]        - Generate phone QR code")
        print("  vcard <name> <phone> [email] [output.png] - Generate vCard")
        print("  sms <number> [message] [output.png] - Generate SMS QR")
        print("")
        print("Examples:")
        print("  python main.py url https://smf.works")
        print("  python main.py wifi 'MyNetwork' 'password123'")
        print("  python main.py email hello@example.com")
        print("  python main.py vcard 'John Doe' '+1234567890' john@example.com")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "url":
        if len(sys.argv) < 3:
            print("Error: url requires URL")
            sys.exit(1)
        
        url = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else "qr-code.png"
        
        result = generate_qr(url, output)
        
        if result["success"]:
            print(f"✅ QR code generated: {result['output']}")
            print(f"   Data: {result['data']}")
            print(f"   Size: {result['size']}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    elif command == "wifi":
        if len(sys.argv) < 4:
            print("Error: wifi requires SSID and password")
            sys.exit(1)
        
        ssid = sys.argv[2]
        password = sys.argv[3]
        output = sys.argv[4] if len(sys.argv) > 4 else "wifi.png"
        
        result = generate_wifi_qr(ssid, password, output_file=output)
        
        if result["success"]:
            print(f"✅ WiFi QR code generated: {result['output']}")
            print(f"   Network: {ssid}")
            print(f"   Size: {result['size']}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    elif command == "email":
        if len(sys.argv) < 3:
            print("Error: email requires email address")
            sys.exit(1)
        
        email = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else "email.png"
        
        result = generate_email_qr(email, output_file=output)
        
        if result["success"]:
            print(f"✅ Email QR code generated: {result['output']}")
            print(f"   Email: {email}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    elif command == "phone":
        if len(sys.argv) < 3:
            print("Error: phone requires phone number")
            sys.exit(1)
        
        phone = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else "phone.png"
        
        result = generate_phone_qr(phone, output)
        
        if result["success"]:
            print(f"✅ Phone QR code generated: {result['output']}")
            print(f"   Phone: {phone}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    elif command == "vcard":
        if len(sys.argv) < 4:
            print("Error: vcard requires name and phone")
            sys.exit(1)
        
        name = sys.argv[2]
        phone = sys.argv[3]
        email = sys.argv[4] if len(sys.argv) > 4 else ""
        output = sys.argv[5] if len(sys.argv) > 5 else "vcard.png"
        
        result = generate_vcard_qr(name, phone, email, output)
        
        if result["success"]:
            print(f"✅ vCard QR code generated: {result['output']}")
            print(f"   Name: {name}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    elif command == "sms":
        if len(sys.argv) < 3:
            print("Error: sms requires phone number")
            sys.exit(1)
        
        phone = sys.argv[2]
        message = sys.argv[3] if len(sys.argv) > 3 else ""
        output = sys.argv[4] if len(sys.argv) > 4 else "sms.png"
        
        result = generate_sms_qr(phone, message, output)
        
        if result["success"]:
            print(f"✅ SMS QR code generated: {result['output']}")
            print(f"   Phone: {phone}")
        else:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)
    
    else:
        print(f"Unknown command: {command}")
        print("Run without arguments for usage help")
        sys.exit(1)


if __name__ == "__main__":
    main()
