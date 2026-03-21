#!/usr/bin/env python3
"""
Email Campaign Manager - SMF Works Pro Skill
Create, manage, and send email campaigns with tracking.

Usage:
    smf run email-campaign create --name "Newsletter March"
    smf run email-campaign list
    smf run email-campaign send --campaign newsletter-march --list subscribers.csv
    smf run email-campaign stats --campaign newsletter-march
"""

import sys
import csv
import json
import smtplib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add shared auth to path
shared_path = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from smf_auth import require_subscription, show_subscription_error

# Skill configuration
SKILL_NAME = "email-campaign"
MIN_TIER = "pro"
CAMPAIGNS_DIR = Path.home() / ".smf" / "campaigns"
LISTS_DIR = Path.home() / ".smf" / "lists"
LOGS_DIR = Path.home() / ".smf" / "logs"


def ensure_dirs():
    """Ensure campaign directories exist."""
    CAMPAIGNS_DIR.mkdir(parents=True, exist_ok=True)
    LISTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def generate_campaign_id(name: str) -> str:
    """Generate unique campaign ID."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_name = name.lower().replace(" ", "-").replace("_", "-")[:30]
    return f"{safe_name}-{timestamp}"


def create_campaign(name: str, subject: str, from_email: str, 
                   template: str = None) -> Dict:
    """Create a new email campaign."""
    try:
        ensure_dirs()
        
        campaign_id = generate_campaign_id(name)
        campaign_dir = CAMPAIGNS_DIR / campaign_id
        campaign_dir.mkdir(parents=True, exist_ok=True)
        
        campaign = {
            "id": campaign_id,
            "name": name,
            "subject": subject,
            "from_email": from_email,
            "created_at": datetime.now().isoformat(),
            "status": "draft",
            "template": template or "default",
            "sent_count": 0,
            "open_count": 0,
            "click_count": 0
        }
        
        # Save campaign config
        config_file = campaign_dir / "config.json"
        config_file.write_text(json.dumps(campaign, indent=2))
        
        # Create email body template
        body_file = campaign_dir / "body.html"
        if template == "newsletter":
            body_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #2563eb; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .footer { background: #f3f4f6; padding: 20px; text-align: center; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{CAMPAIGN_NAME}}</h1>
        </div>
        <div class="content">
            <p>Hello {{FIRST_NAME}},</p>
            <p>Your content here...</p>
        </div>
        <div class="footer">
            <p>You're receiving this because you subscribed to our newsletter.</p>
            <p><a href="{{UNSUBSCRIBE_URL}}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>"""
        else:
            body_content = """<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <p>Hello {{FIRST_NAME}},</p>
        <p>Your email content here...</p>
        <p>Best regards,<br>{{FROM_NAME}}</p>
        <hr>
        <p style="font-size: 12px; color: #666;">
            <a href="{{UNSUBSCRIBE_URL}}">Unsubscribe</a>
        </p>
    </div>
</body>
</html>"""
        
        body_file.write_text(body_content)
        
        return {
            "success": True,
            "campaign_id": campaign_id,
            "name": name,
            "config_file": str(config_file),
            "body_file": str(body_file)
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_campaigns() -> List[Dict]:
    """List all campaigns."""
    ensure_dirs()
    
    campaigns = []
    for campaign_dir in CAMPAIGNS_DIR.iterdir():
        if campaign_dir.is_dir():
            config_file = campaign_dir / "config.json"
            if config_file.exists():
                try:
                    campaign = json.loads(config_file.read_text())
                    campaigns.append(campaign)
                except:
                    pass
    
    # Sort by creation date
    campaigns.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return campaigns


def load_campaign(campaign_id: str) -> Optional[Dict]:
    """Load campaign by ID."""
    campaign_dir = CAMPAIGNS_DIR / campaign_id
    config_file = campaign_dir / "config.json"
    
    if config_file.exists():
        try:
            return json.loads(config_file.read_text())
        except:
            pass
    return None


def load_email_body(campaign_id: str) -> str:
    """Load email body template."""
    campaign_dir = CAMPAIGNS_DIR / campaign_id
    body_file = campaign_dir / "body.html"
    
    if body_file.exists():
        return body_file.read_text()
    return "<p>Hello {{FIRST_NAME}},</p><p>Email content here...</p>"


def load_mailing_list(list_file: str) -> List[Dict]:
    """Load mailing list from CSV."""
    try:
        list_path = Path(list_file).expanduser()
        
        if not list_path.exists():
            return []
        
        with open(list_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
            
    except Exception as e:
        return []


def validate_email_list(email_list: List[Dict]) -> List[Dict]:
    """Validate and clean email list."""
    valid = []
    seen = set()
    
    for row in email_list:
        email = row.get("email", "").strip().lower()
        
        # Basic validation
        if "@" in email and "." in email.split("@")[-1]:
            if email not in seen:
                seen.add(email)
                valid.append(row)
    
    return valid


def personalize_email(template: str, recipient: Dict, campaign: Dict) -> str:
    """Personalize email template with recipient data."""
    email = template
    
    # Replace variables
    email = email.replace("{{FIRST_NAME}}", recipient.get("first_name", "Friend"))
    email = email.replace("{{LAST_NAME}}", recipient.get("last_name", ""))
    email = email.replace("{{EMAIL}}", recipient.get("email", ""))
    email = email.replace("{{CAMPAIGN_NAME}}", campaign.get("name", ""))
    email = email.replace("{{FROM_NAME}}", campaign.get("from_email", "").split("@")[0])
    email = email.replace("{{UNSUBSCRIBE_URL}}", f"#unsubscribe-{recipient.get('email', '')}")
    
    # Replace custom fields
    for key, value in recipient.items():
        placeholder = f"{{{{{key.upper()}}}}}"
        email = email.replace(placeholder, str(value))
    
    return email


def send_email_smtp(to_email: str, subject: str, body: str, from_email: str,
                   smtp_host: str, smtp_port: int, smtp_user: str, smtp_pass: str) -> bool:
    """Send single email via SMTP."""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        
        html_part = MIMEText(body, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to send to {to_email}: {e}")
        return False


def send_campaign(campaign_id: str, list_file: str, 
                 smtp_config: Dict = None, dry_run: bool = True) -> Dict:
    """Send campaign to mailing list."""
    try:
        campaign = load_campaign(campaign_id)
        if not campaign:
            return {"success": False, "error": "Campaign not found"}
        
        # Load email list
        email_list = load_mailing_list(list_file)
        if not email_list:
            return {"success": False, "error": "No valid recipients found"}
        
        # Validate emails
        valid_list = validate_email_list(email_list)
        
        print(f"\n📧 Sending Campaign: {campaign['name']}")
        print(f"   Recipients: {len(valid_list)}")
        print(f"   Subject: {campaign['subject']}")
        print(f"   From: {campaign['from_email']}")
        
        if dry_run:
            print(f"\n🔧 DRY RUN MODE - No emails sent")
            print(f"   Would send to: {len(valid_list)} recipients")
            print(f"\n   First 3 recipients:")
            for i, recipient in enumerate(valid_list[:3], 1):
                print(f"     {i}. {recipient.get('email')}")
            
            print(f"\n✅ Dry run complete. To actually send, use --send")
            return {"success": True, "dry_run": True, "recipients": len(valid_list)}
        
        # Check for SMTP config
        if not smtp_config:
            return {"success": False, "error": "SMTP configuration required"}
        
        # Load email template
        template = load_email_body(campaign_id)
        
        # Send emails
        sent = 0
        failed = 0
        
        print(f"\n🚀 Sending emails...")
        
        for i, recipient in enumerate(valid_list, 1):
            # Personalize
            personalized_body = personalize_email(template, recipient, campaign)
            
            # Send
            success = send_email_smtp(
                recipient.get("email"),
                campaign['subject'],
                personalized_body,
                campaign['from_email'],
                smtp_config['host'],
                smtp_config['port'],
                smtp_config['user'],
                smtp_config['pass']
            )
            
            if success:
                sent += 1
                print(f"  ✅ {i}/{len(valid_list)}: {recipient.get('email')}")
            else:
                failed += 1
                print(f"  ❌ {i}/{len(valid_list)}: {recipient.get('email')}")
        
        # Update campaign stats
        campaign['sent_count'] = sent
        campaign['status'] = 'sent'
        campaign['sent_at'] = datetime.now().isoformat()
        
        config_file = CAMPAIGNS_DIR / campaign_id / "config.json"
        config_file.write_text(json.dumps(campaign, indent=2))
        
        # Log results
        log_file = LOGS_DIR / f"{campaign_id}-send.log"
        with open(log_file, 'w') as f:
            f.write(f"Campaign: {campaign['name']}\n")
            f.write(f"Sent: {sent}\n")
            f.write(f"Failed: {failed}\n")
            f.write(f"Time: {datetime.now().isoformat()}\n")
        
        return {
            "success": True,
            "sent": sent,
            "failed": failed,
            "total": len(valid_list)
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_campaign_stats(campaign_id: str) -> Dict:
    """Get campaign statistics."""
    campaign = load_campaign(campaign_id)
    
    if not campaign:
        return {"error": "Campaign not found"}
    
    # Load send log if exists
    log_file = LOGS_DIR / f"{campaign_id}-send.log"
    send_log = {}
    if log_file.exists():
        try:
            content = log_file.read_text()
            for line in content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    send_log[key.strip().lower()] = value.strip()
        except:
            pass
    
    return {
        "campaign_id": campaign_id,
        "name": campaign.get("name"),
        "status": campaign.get("status"),
        "created_at": campaign.get("created_at"),
        "sent_at": campaign.get("sent_at"),
        "sent_count": campaign.get("sent_count", 0),
        "open_count": campaign.get("open_count", 0),
        "click_count": campaign.get("click_count", 0),
        "template": campaign.get("template")
    }


def edit_campaign_body(campaign_id: str) -> Dict:
    """Open campaign body in editor."""
    campaign_dir = CAMPAIGNS_DIR / campaign_id
    body_file = campaign_dir / "body.html"
    
    if not body_file.exists():
        return {"success": False, "error": "Campaign not found"}
    
    # Open in default editor
    import subprocess
    editor = os.environ.get('EDITOR', 'nano')
    
    try:
        subprocess.run([editor, str(body_file)])
        return {"success": True, "file": str(body_file)}
    except Exception as e:
        return {"success": False, "error": f"Could not open editor: {e}"}


def create_sample_list(output_file: str) -> Dict:
    """Create sample mailing list."""
    try:
        samples = [
            {"email": "john@example.com", "first_name": "John", "last_name": "Smith", "company": "Acme Corp"},
            {"email": "jane@example.com", "first_name": "Jane", "last_name": "Doe", "company": "Tech Inc"},
            {"email": "bob@example.com", "first_name": "Bob", "last_name": "Johnson", "company": "Startup LLC"},
        ]
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["email", "first_name", "last_name", "company"])
            writer.writeheader()
            writer.writerows(samples)
        
        return {"success": True, "file": output_file, "recipients": len(samples)}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def interactive_create():
    """Interactive campaign creation."""
    print("\n📧 Email Campaign Manager")
    print("=" * 40)
    
    name = input("\nCampaign name: ").strip()
    if not name:
        print("❌ Campaign name required")
        return {"success": False, "error": "Name required"}
    
    subject = input("Email subject: ").strip()
    from_email = input("From email: ").strip()
    
    print("\nTemplate:")
    print("  1. Default (simple)")
    print("  2. Newsletter (styled)")
    
    template_choice = input("Choice [1]: ").strip() or "1"
    template = "newsletter" if template_choice == "2" else "default"
    
    return create_campaign(name, subject, from_email, template)


def show_help():
    """Show help message."""
    print("""📧 Email Campaign Manager

Create and send email campaigns with personalization.

Commands:
  create                    Create new campaign (interactive)
  create --name NAME        Create with name
  list                      List all campaigns
  edit --campaign ID        Edit campaign body
  send --campaign ID        Send campaign (dry run)
  send --campaign ID --send Actually send emails
  stats --campaign ID       Show campaign statistics
  sample-list               Create sample mailing list
  help                      Show this help

Examples:
  smf run email-campaign create
  smf run email-campaign list
  smf run email-campaign send --campaign newsletter-20260320 --list subscribers.csv
  smf run email-campaign stats --campaign newsletter-20260320
  smf run email-campaign sample-list --output test-list.csv

Setup SMTP:
  Set environment variables:
  export SMTP_HOST=smtp.gmail.com
  export SMTP_PORT=587
  export SMTP_USER=your-email@gmail.com
  export SMTP_PASS=your-app-password
""")


def main():
    """CLI entry point."""
    # Check for test mode
    if "--test-mode" in sys.argv:
        sys.argv.remove("--test-mode")
        print("🔧 TEST MODE: Subscription check skipped")
        subscription = {"valid": True, "tier": "test"}
    else:
        # Check subscription
        subscription = require_subscription(SKILL_NAME, MIN_TIER)
        
        if not subscription["valid"]:
            show_subscription_error(subscription)
            return 1
        
        print(f"📧 Email Campaign Manager")
        print(f"   Subscription: {subscription['tier']}")
        print("")
    
    # Parse command
    if len(sys.argv) < 2:
        show_help()
        return 0
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "create":
        if "--name" in args:
            idx = args.index("--name")
            name = args[idx + 1] if idx + 1 < len(args) else "New Campaign"
            subject = ""
            from_email = ""
            
            if "--subject" in args:
                s_idx = args.index("--subject")
                subject = args[s_idx + 1] if s_idx + 1 < len(args) else "Subject"
            
            if "--from" in args:
                f_idx = args.index("--from")
                from_email = args[f_idx + 1] if f_idx + 1 < len(args) else ""
            
            template = "newsletter" if "--template" in args and "newsletter" in args else "default"
            
            result = create_campaign(name, subject, from_email, template)
        else:
            result = interactive_create()
        
        if result["success"]:
            print(f"✅ Campaign created: {result['campaign_id']}")
            print(f"   Edit body: smf run email-campaign edit --campaign {result['campaign_id']}")
        else:
            print(f"❌ Failed: {result.get('error')}")
            return 1
    
    elif command == "list":
        campaigns = list_campaigns()
        
        if not campaigns:
            print("No campaigns found.")
            return 0
        
        print(f"\n📧 {len(campaigns)} Campaign(s)")
        print("-" * 80)
        print(f"{'ID':<40} {'Name':<25} {'Status':<10}")
        print("-" * 80)
        
        for camp in campaigns[:20]:
            name = camp.get('name', 'Untitled')[:23]
            status = camp.get('status', 'unknown')
            print(f"{camp['id']:<40} {name:<25} {status:<10}")
    
    elif command == "edit":
        if "--campaign" not in args:
            print("❌ --campaign ID required")
            return 1
        
        idx = args.index("--campaign")
        campaign_id = args[idx + 1] if idx + 1 < len(args) else None
        
        if not campaign_id:
            print("❌ Campaign ID required")
            return 1
        
        result = edit_campaign_body(campaign_id)
        
        if result["success"]:
            print(f"✅ Opened: {result['file']}")
        else:
            print(f"❌ {result.get('error')}")
            return 1
    
    elif command == "send":
        if "--campaign" not in args:
            print("❌ --campaign ID required")
            return 1
        
        idx = args.index("--campaign")
        campaign_id = args[idx + 1] if idx + 1 < len(args) else None
        
        if not campaign_id:
            print("❌ Campaign ID required")
            return 1
        
        # Get list file
        list_file = None
        if "--list" in args:
            l_idx = args.index("--list")
            list_file = args[l_idx + 1] if l_idx + 1 < len(args) else None
        
        if not list_file:
            print("❌ --list FILE required")
            return 1
        
        # Check for --send flag (actual send vs dry run)
        dry_run = "--send" not in args
        
        # Get SMTP config from environment
        import os
        smtp_config = None
        if not dry_run:
            smtp_config = {
                'host': os.environ.get('SMTP_HOST', ''),
                'port': int(os.environ.get('SMTP_PORT', 587)),
                'user': os.environ.get('SMTP_USER', ''),
                'pass': os.environ.get('SMTP_PASS', '')
            }
            
            if not all([smtp_config['host'], smtp_config['user'], smtp_config['pass']]):
                print("❌ SMTP configuration required")
                print("   Set: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS")
                return 1
        
        result = send_campaign(campaign_id, list_file, smtp_config, dry_run)
        
        if result["success"]:
            if not dry_run:
                print(f"\n✅ Campaign sent!")
                print(f"   Sent: {result['sent']}")
                print(f"   Failed: {result['failed']}")
        else:
            print(f"❌ Failed: {result.get('error')}")
            return 1
    
    elif command == "stats":
        if "--campaign" not in args:
            print("❌ --campaign ID required")
            return 1
        
        idx = args.index("--campaign")
        campaign_id = args[idx + 1] if idx + 1 < len(args) else None
        
        if not campaign_id:
            print("❌ Campaign ID required")
            return 1
        
        stats = get_campaign_stats(campaign_id)
        
        if "error" in stats:
            print(f"❌ {stats['error']}")
            return 1
        
        print(f"\n📊 Campaign Statistics")
        print("=" * 40)
        print(f"Name: {stats['name']}")
        print(f"Status: {stats['status']}")
        print(f"Created: {stats['created_at'][:10] if stats['created_at'] else 'N/A'}")
        if stats.get('sent_at'):
            print(f"Sent: {stats['sent_at'][:10]}")
        print(f"")
        print(f"Sent: {stats['sent_count']}")
        print(f"Opens: {stats['open_count']}")
        print(f"Clicks: {stats['click_count']}")
    
    elif command == "sample-list":
        output = "sample-list.csv"
        if "--output" in args:
            o_idx = args.index("--output")
            output = args[o_idx + 1] if o_idx + 1 < len(args) else output
        
        result = create_sample_list(output)
        
        if result["success"]:
            print(f"✅ Sample list created: {result['file']}")
            print(f"   Recipients: {result['recipients']}")
        else:
            print(f"❌ Failed: {result.get('error')}")
            return 1
    
    elif command in ("help", "--help", "-h"):
        show_help()
    
    else:
        print(f"Unknown command: {command}")
        print("Run 'smf run email-campaign help' for usage.")
        return 1
    
    return 0


if __name__ == "__main__":
    import os
    sys.exit(main())
