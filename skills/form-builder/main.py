#!/usr/bin/env python3
"""
Form Builder - SMF Works Pro Skill
Create forms, collect responses, and export submissions.

Usage:
    smf run form-builder create --name "Contact Form" --fields name,email,message
    smf run form-builder serve FORM-ID --port 8080
    smf run form-builder responses FORM-ID
    smf run form-builder export FORM-ID --format csv
"""

import sys
import json
import uuid
import hmac
import hashlib
import secrets
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Add shared auth to path
shared_path = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from smf_auth import require_subscription, show_subscription_error

# Skill configuration
SKILL_NAME = "form-builder"
MIN_TIER = "pro"
FORMS_DIR = Path.home() / ".smf" / "forms"
RESPONSES_DIR = Path.home() / ".smf" / "form-responses"
CONFIG_FILE = Path.home() / ".smf" / "form-config.json"

# Field types
FIELD_TYPES = ["text", "email", "number", "textarea", "select", "checkbox", "radio", "date", "tel", "url"]

# Security
CSRF_TOKEN_HEADER = "X-CSRF-Token"
MAX_FIELD_COUNT = 50
MAX_RESPONSE_SIZE = 1024 * 1024  # 1MB


def ensure_dirs():
    """Ensure form directories exist."""
    FORMS_DIR.mkdir(parents=True, exist_ok=True)
    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)


def generate_csrf_secret():
    """Generate a CSRF secret for the server."""
    if not CONFIG_FILE.exists():
        secret = secrets.token_hex(32)
        CONFIG_FILE.write_text(json.dumps({"csrf_secret": secret}))
        return secret
    
    try:
        config = json.loads(CONFIG_FILE.read_text())
        return config.get("csrf_secret", secrets.token_hex(32))
    except:
        return secrets.token_hex(32)


def generate_csrf_token(secret: str, form_id: str) -> str:
    """Generate a CSRF token for a form."""
    timestamp = datetime.now().strftime("%Y%m%d%H")
    data = f"{form_id}:{timestamp}"
    return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()[:32]


def verify_csrf_token(token: str, secret: str, form_id: str) -> bool:
    """Verify a CSRF token."""
    # Check current hour and previous hour (allow 1 hour drift)
    for hour_offset in [0, -1]:
        check_time = datetime.now() + timedelta(hours=hour_offset)
        timestamp = check_time.strftime("%Y%m%d%H")
        data = f"{form_id}:{timestamp}"
        expected = hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()[:32]
        if hmac.compare_digest(token, expected):
            return True
    return False


def generate_form_id() -> str:
    """Generate unique form ID."""
    return f"FORM-{uuid.uuid4().hex[:8].upper()}"


def generate_response_id() -> str:
    """Generate unique response ID."""
    return f"RESP-{uuid.uuid4().hex[:8].upper()}"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal."""
    return re.sub(r'[^\w\-_.]', '_', filename)


def validate_field_name(name: str) -> bool:
    """Validate field name is safe."""
    if not name or len(name) > 100:
        return False
    # Allow alphanumeric, underscore, hyphen
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', name))


def validate_response_data(data: Dict, fields: List[Dict]) -> tuple[bool, str]:
    """Validate submitted response data."""
    # Check total size
    data_size = len(json.dumps(data))
    if data_size > MAX_RESPONSE_SIZE:
        return False, "Response too large"
    
    allowed_fields = {f["name"] for f in fields}
    
    # Check for unexpected fields
    for key in data.keys():
        if key not in allowed_fields and key != "csrf_token":
            return False, f"Unexpected field: {key}"
    
    # Validate each field
    for field in fields:
        field_name = field.get("name")
        value = data.get(field_name, "")
        field_type = field.get("type", "text")
        required = field.get("required", False)
        
        if required and not value:
            return False, f"Required field missing: {field_name}"
        
        if value:
            # Type validation
            if field_type == "email":
                if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', value):
                    return False, f"Invalid email in {field_name}"
            elif field_type == "number":
                try:
                    float(value)
                except ValueError:
                    return False, f"Invalid number in {field_name}"
            elif field_type == "url":
                if not re.match(r'^https?://[^\s]+$', value):
                    return False, f"Invalid URL in {field_name}"
            elif field_type == "tel":
                # Basic phone validation
                if not re.match(r'^[\d\s\-\+\(\)]+$', value):
                    return False, f"Invalid phone in {field_name}"
    
    return True, "OK"


def create_form(name: str, description: str = "", fields: List[Dict] = None) -> Dict:
    """Create a new form with validation."""
    try:
        ensure_dirs()
        
        # Validate name
        if not name or len(name) > 200:
            return {"success": False, "error": "Name required (max 200 chars)"}
        
        # Validate field count
        if fields and len(fields) > MAX_FIELD_COUNT:
            return {"success": False, "error": f"Maximum {MAX_FIELD_COUNT} fields allowed"}
        
        # Validate field names
        if fields:
            for field in fields:
                if not validate_field_name(field.get("name", "")):
                    return {"success": False, "error": f"Invalid field name: {field.get('name')}"}
        
        form_id = generate_form_id()
        
        form = {
            "id": form_id,
            "name": name.strip(),
            "description": description[:500] if description else "",  # Limit length
            "fields": fields or [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "active",
            "response_count": 0,
            "auth_required": False  # For future auth feature
        }
        
        # Save form
        form_file = FORMS_DIR / f"{form_id}.json"
        form_file.write_text(json.dumps(form, indent=2))
        
        return {
            "success": True,
            "form": form,
            "form_file": str(form_file)
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def load_form(form_id: str) -> Optional[Dict]:
    """Load form by ID with sanitization."""
    # Sanitize form_id
    safe_id = sanitize_filename(form_id)
    form_file = FORMS_DIR / f"{safe_id}.json"
    
    if form_file.exists():
        try:
            return json.loads(form_file.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    return None


def load_forms() -> List[Dict]:
    """Load all forms."""
    ensure_dirs()
    
    forms = []
    for form_file in FORMS_DIR.glob("FORM-*.json"):
        try:
            form = json.loads(form_file.read_text())
            forms.append(form)
        except (json.JSONDecodeError, IOError):
            continue
    
    # Sort by creation date
    forms.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return forms


def update_form(form_id: str, updates: Dict) -> Dict:
    """Update form fields."""
    form = load_form(form_id)
    if not form:
        return {"success": False, "error": "Form not found"}
    
    # Apply updates
    for key, value in updates.items():
        if key in ["name", "description", "fields", "status"]:
            form[key] = value
    
    form["updated_at"] = datetime.now().isoformat()
    
    # Save
    form_file = FORMS_DIR / f"{form_id}.json"
    form_file.write_text(json.dumps(form, indent=2))
    
    return {"success": True, "form": form}


def add_field(form_id: str, field: Dict) -> Dict:
    """Add a field to form."""
    form = load_form(form_id)
    if not form:
        return {"success": False, "error": "Form not found"}
    
    # Check field limit
    if len(form.get("fields", [])) >= MAX_FIELD_COUNT:
        return {"success": False, "error": f"Maximum {MAX_FIELD_COUNT} fields reached"}
    
    # Validate field
    if "name" not in field or "type" not in field:
        return {"success": False, "error": "Field must have name and type"}
    
    if not validate_field_name(field["name"]):
        return {"success": False, "error": f"Invalid field name: {field['name']}"}
    
    if field["type"] not in FIELD_TYPES:
        return {"success": False, "error": f"Invalid field type. Use: {', '.join(FIELD_TYPES)}"}
    
    # Add field
    if "fields" not in form:
        form["fields"] = []
    
    field["id"] = f"field-{len(form['fields'])}"
    form["fields"].append(field)
    form["updated_at"] = datetime.now().isoformat()
    
    # Save
    form_file = FORMS_DIR / f"{form_id}.json"
    form_file.write_text(json.dumps(form, indent=2))
    
    return {"success": True, "form": form}


def submit_response(form_id: str, data: Dict, client_ip: str = None) -> Dict:
    """Submit a form response with validation."""
    form = load_form(form_id)
    if not form:
        return {"success": False, "error": "Form not found"}
    
    if form.get("status") != "active":
        return {"success": False, "error": "Form is not accepting responses"}
    
    # Validate data
    valid, message = validate_response_data(data, form.get("fields", []))
    if not valid:
        return {"success": False, "error": message}
    
    try:
        ensure_dirs()
        
        response_id = generate_response_id()
        
        # Sanitize submitted data
        safe_data = {}
        for key, value in data.items():
            if key == "csrf_token":
                continue  # Don't store CSRF token
            if isinstance(value, str):
                # Basic XSS prevention
                value = value.replace('<', '&lt;').replace('>', '&gt;')
            safe_data[key] = value
        
        response = {
            "id": response_id,
            "form_id": form_id,
            "data": safe_data,
            "submitted_at": datetime.now().isoformat(),
            "ip_address": client_ip,
            "user_agent": None  # Could capture if needed
        }
        
        # Save response
        response_file = RESPONSES_DIR / f"{response_id}.json"
        response_file.write_text(json.dumps(response, indent=2))
        
        # Update form response count
        form["response_count"] = form.get("response_count", 0) + 1
        form_file = FORMS_DIR / f"{form_id}.json"
        form_file.write_text(json.dumps(form, indent=2))
        
        return {"success": True, "response_id": response_id}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def load_responses(form_id: str = None) -> List[Dict]:
    """Load form responses."""
    ensure_dirs()
    
    responses = []
    for response_file in RESPONSES_DIR.glob("RESP-*.json"):
        try:
            response = json.loads(response_file.read_text())
            
            # Filter by form
            if form_id and response.get("form_id") != form_id:
                continue
            
            responses.append(response)
        except (json.JSONDecodeError, IOError):
            continue
    
    # Sort by date
    responses.sort(key=lambda x: x.get("submitted_at", ""), reverse=True)
    return responses


def get_response(response_id: str) -> Optional[Dict]:
    """Get specific response."""
    response_file = RESPONSES_DIR / f"{sanitize_filename(response_id)}.json"
    if response_file.exists():
        try:
            return json.loads(response_file.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    return None


def export_responses(form_id: str, format: str = "csv", output_file: str = None) -> Dict:
    """Export form responses with path validation."""
    form = load_form(form_id)
    if not form:
        return {"success": False, "error": "Form not found"}
    
    responses = load_responses(form_id)
    
    if not responses:
        return {"success": False, "error": "No responses to export"}
    
    try:
        if format == "csv":
            # Determine CSV headers from form fields
            headers = [f["name"] for f in form.get("fields", [])]
            headers.append("submitted_at")
            
            if not output_file:
                output_file = f"{form_id}-responses.csv"
            
            # Validate output path
            output_path = Path(output_file).resolve()
            cwd = Path.cwd().resolve()
            try:
                output_path.relative_to(cwd)
            except ValueError:
                return {"success": False, "error": "Output path must be within current directory"}
            
            import csv
            with open(output_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
                writer.writeheader()
                
                for response in responses:
                    row = response["data"].copy()
                    row["submitted_at"] = response.get("submitted_at", "")
                    # Sanitize for CSV injection prevention
                    for key, value in row.items():
                        if value and str(value).startswith(('=', '+', '-', '@', '\t', '\r')):
                            row[key] = "'" + str(value)
                    writer.writerow(row)
            
            return {"success": True, "file": str(output_path), "count": len(responses)}
        
        elif format == "json":
            if not output_file:
                output_file = f"{form_id}-responses.json"
            
            output_path = Path(output_file).resolve()
            cwd = Path.cwd().resolve()
            try:
                output_path.relative_to(cwd)
            except ValueError:
                return {"success": False, "error": "Output path must be within current directory"}
            
            with open(output_path, 'w') as f:
                json.dump(responses, f, indent=2)
            
            return {"success": True, "file": str(output_path), "count": len(responses)}
        
        else:
            return {"success": False, "error": f"Unsupported format: {format}"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_html_form(form: Dict, action_url: str = "#", csrf_token: str = "") -> str:
    """Generate HTML form with CSRF protection."""
    fields_html = ""
    
    for field in form.get("fields", []):
        field_type = field.get("type", "text")
        field_name = field.get("name", "")
        field_label = field.get("label", field_name)
        required = "required" if field.get("required", False) else ""
        placeholder = field.get("placeholder", "")
        placeholder = placeholder.replace('"', '&quot;')  # Escape quotes
        
        if field_type == "textarea":
            fields_html += f"""
            <div style="margin-bottom: 15px;">
                <label style="display: block; margin-bottom: 5px; font-weight: bold;">{field_label}</label>
                <textarea name="{field_name}" {required} placeholder="{placeholder}" 
                    style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; min-height: 100px;"></textarea>
            </div>
            """
        elif field_type == "select":
            options = field.get("options", [])
            options_html = "".join([f'<option value="{opt}">{opt}</option>' for opt in options])
            fields_html += f"""
            <div style="margin-bottom: 15px;">
                <label style="display: block; margin-bottom: 5px; font-weight: bold;">{field_label}</label>
                <select name="{field_name}" {required} style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                    <option value="">Select...</option>
                    {options_html}
                </select>
            </div>
            """
        elif field_type == "checkbox":
            fields_html += f"""
            <div style="margin-bottom: 15px;">
                <label style="display: flex; align-items: center; cursor: pointer;">
                    <input type="checkbox" name="{field_name}" {required} style="margin-right: 8px;">
                    <span>{field_label}</span>
                </label>
            </div>
            """
        elif field_type == "radio":
            options = field.get("options", [])
            options_html = ""
            for opt in options:
                options_html += f"""
                <label style="display: block; margin: 5px 0;">
                    <input type="radio" name="{field_name}" value="{opt}" {required}>
                    {opt}
                </label>
                """
            fields_html += f"""
            <div style="margin-bottom: 15px;">
                <label style="display: block; margin-bottom: 5px; font-weight: bold;">{field_label}</label>
                {options_html}
            </div>
            """
        else:
            input_type = "email" if field_type == "email" else field_type
            fields_html += f"""
            <div style="margin-bottom: 15px;">
                <label style="display: block; margin-bottom: 5px; font-weight: bold;">{field_label}</label>
                <input type="{input_type}" name="{field_name}" {required} placeholder="{placeholder}"
                    style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
            </div>
            """
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{form.get('name', 'Form')}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               max-width: 600px; margin: 40px auto; padding: 20px; background: #f5f5f5; }}
        .form-container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; margin-bottom: 10px; }}
        .description {{ color: #666; margin-bottom: 30px; }}
        button {{ background: #2563eb; color: white; padding: 12px 24px; border: none; 
                  border-radius: 4px; cursor: pointer; font-size: 16px; }}
        button:hover {{ background: #1d4ed8; }}
    </style>
</head>
<body>
    <div class="form-container">
        <h1>{form.get('name', 'Form')}</h1>
        {f'<p class="description">{form.get("description")}</p>' if form.get('description') else ''}
        
        <form action="{action_url}" method="POST">
            <input type="hidden" name="csrf_token" value="{csrf_token}">
            {fields_html}
            <button type="submit">Submit</button>
        </form>
    </div>
</body>
</html>"""
    
    return html


def display_forms(forms: List[Dict]):
    """Display forms list."""
    if not forms:
        print("\nNo forms found.")
        return
    
    print(f"\n📝 Forms ({len(forms)})")
    print("-" * 80)
    print(f"{'ID':<20} {'Name':<30} {'Status':<12} {'Responses':<10}")
    print("-" * 80)
    
    for form in forms:
        form_id = form['id']
        name = form.get('name', 'Untitled')[:28]
        status = form.get('status', 'active')
        responses = form.get('response_count', 0)
        
        status_icon = "✅" if status == "active" else "⏸️"
        
        print(f"{form_id:<20} {name:<30} {status_icon} {status:<10} {responses:<10}")
    
    print("-" * 80)


def display_responses(responses: List[Dict], form_id: str):
    """Display form responses."""
    if not responses:
        print(f"\nNo responses for form {form_id}.")
        return
    
    form = load_form(form_id)
    form_name = form.get('name', form_id) if form else form_id
    
    print(f"\n📊 Responses for '{form_name}' ({len(responses)})")
    print("-" * 80)
    
    for i, response in enumerate(responses[:10], 1):
        print(f"\n{i}. Response {response['id']}")
        print(f"   Submitted: {response.get('submitted_at', 'Unknown')}")
        
        data = response.get("data", {})
        for key, value in data.items():
            value_str = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
            print(f"   {key}: {value_str}")
    
    if len(responses) > 10:
        print(f"\n... and {len(responses) - 10} more responses")
    
    print("-" * 80)


def display_form_details(form_id: str):
    """Display form details."""
    form = load_form(form_id)
    
    if not form:
        print(f"❌ Form {form_id} not found")
        return
    
    print(f"\n📝 Form Details")
    print("=" * 60)
    print(f"ID: {form['id']}")
    print(f"Name: {form.get('name', 'Untitled')}")
    print(f"Status: {form.get('status', 'active')}")
    print(f"Responses: {form.get('response_count', 0)}")
    print(f"Created: {form.get('created_at', 'Unknown')[:10]}")
    
    if form.get('description'):
        print(f"\nDescription: {form['description']}")
    
    print(f"\nFields ({len(form.get('fields', []))}):")
    for i, field in enumerate(form.get('fields', []), 1):
        required = " (required)" if field.get('required') else ""
        print(f"  {i}. {field.get('label', field['name'])} [{field['type']}]{required}")


def interactive_create_form():
    """Interactive form creation."""
    print("\n📝 Create New Form")
    print("-" * 40)
    
    name = input("Form name: ").strip()
    if not name:
        print("❌ Form name required")
        return {"success": False, "error": "Name required"}
    
    description = input("Description (optional): ").strip()
    
    # Add fields
    fields = []
    print("\nAdd fields (leave name blank to finish):")
    
    field_num = 1
    while True:
        print(f"\nField {field_num}:")
        
        field_name = input("Field name (or blank to finish): ").strip()
        if not field_name:
            break
        
        if not validate_field_name(field_name):
            print("❌ Invalid field name (use alphanumeric, underscore, hyphen)")
            continue
        
        field_label = input("Label (or blank to use name): ").strip() or field_name
        
        print("Field type:")
        for i, ft in enumerate(FIELD_TYPES, 1):
            print(f"  {i}. {ft}")
        
        type_choice = input("Choice [1]: ").strip() or "1"
        try:
            field_type = FIELD_TYPES[int(type_choice) - 1]
        except:
            field_type = "text"
        
        required = input("Required? (y/n) [n]: ").strip().lower() == "y"
        placeholder = input("Placeholder (optional): ").strip()
        
        field = {
            "name": field_name,
            "label": field_label,
            "type": field_type,
            "required": required
        }
        
        if placeholder:
            field["placeholder"] = placeholder
        
        # Add options for select/radio
        if field_type in ["select", "radio"]:
            print("Enter options (comma-separated):")
            options_str = input("Options: ").strip()
            if options_str:
                field["options"] = [opt.strip() for opt in options_str.split(",")]
        
        fields.append(field)
        field_num += 1
        
        if len(fields) >= MAX_FIELD_COUNT:
            print(f"Maximum {MAX_FIELD_COUNT} fields reached")
            break
    
    if not fields:
        print("❌ At least one field required")
        return {"success": False, "error": "Fields required"}
    
    return create_form(name, description, fields)


class FormHandler(BaseHTTPRequestHandler):
    """HTTP request handler for serving forms with CSRF protection."""
    
    csrf_secret = None
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
    
    def get_client_ip(self):
        """Get client IP address."""
        return self.client_address[0]
    
    def do_GET(self):
        """Handle GET requests."""
        # Extract form ID from path
        path_parts = self.path.strip('/').split('/')
        form_id = path_parts[0] if path_parts else None
        
        if not form_id or not form_id.startswith("FORM-"):
            self.send_error(404, "Form not found")
            return
        
        form = load_form(form_id)
        if not form:
            self.send_error(404, "Form not found")
            return
        
        # Generate CSRF token
        csrf_token = generate_csrf_token(self.csrf_secret, form_id)
        
        # Generate HTML
        html = generate_html_form(form, f"/submit/{form_id}", csrf_token)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def do_POST(self):
        """Handle POST requests (form submissions) with CSRF validation."""
        if not self.path.startswith("/submit/"):
            self.send_error(404, "Not found")
            return
        
        form_id = self.path[8:]  # Remove /submit/
        
        if not form_id.startswith("FORM-"):
            self.send_error(404, "Form not found")
            return
        
        form = load_form(form_id)
        if not form:
            self.send_error(404, "Form not found")
            return
        
        # Read form data
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > MAX_RESPONSE_SIZE:
                self.send_error(413, "Payload too large")
                return
            
            post_data = self.rfile.read(content_length).decode('utf-8')
        except Exception:
            self.send_error(400, "Invalid request")
            return
        
        # Parse form data
        from urllib.parse import parse_qs
        parsed_data = parse_qs(post_data, keep_blank_values=True)
        
        # Convert to simple dict
        data = {}
        for key, values in parsed_data.items():
            data[key] = values[0] if len(values) == 1 else values
        
        # Verify CSRF token
        csrf_token = data.get('csrf_token', '')
        if not verify_csrf_token(csrf_token, self.csrf_secret, form_id):
            self.send_response(403)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Error</h1><p>Invalid security token. Please refresh the page and try again.</p>")
            return
        
        # Submit response
        result = submit_response(form_id, data, self.get_client_ip())
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if result["success"]:
            success_html = """<!DOCTYPE html>
<html>
<head><title>Thank You</title></head>
<body style="font-family: sans-serif; text-align: center; padding: 50px;">
    <h1>Thank You!</h1>
    <p>Your response has been submitted.</p>
    <a href="javascript:history.back()">Back to form</a>
</body>
</html>"""
            self.wfile.write(success_html.encode())
        else:
            self.wfile.write(f"<h1>Error</h1><p>{result.get('error', 'Submission failed')}</p>".encode())


def serve_form(form_id: str, port: int = 8080) -> Dict:
    """Start HTTP server to serve form with security."""
    form = load_form(form_id)
    if not form:
        return {"success": False, "error": "Form not found"}
    
    # Initialize CSRF secret
    FormHandler.csrf_secret = generate_csrf_secret()
    
    try:
        server = HTTPServer(('localhost', port), FormHandler)
        
        print(f"\n🌐 Serving form '{form.get('name', form_id)}'")
        print(f"   URL: http://localhost:{port}/{form_id}")
        print(f"   CSRF Protection: Enabled")
        print(f"   Press Ctrl+C to stop\n")
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n✅ Server stopped")
            server.shutdown()
        
        return {"success": True}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def show_help():
    """Show help message."""
    print("""📝 Form Builder

Create forms, collect responses, and export data.

Commands:
  create                       Create form (interactive)
  create --name "Name"         Create with name
  list                         List all forms
  show FORM-ID                 Show form details
  add-field FORM-ID            Add field to form
  serve FORM-ID                Serve form via HTTP
  responses FORM-ID            Show responses
  export FORM-ID               Export to CSV/JSON
  help                         Show this help

Security Features:
  • CSRF protection on all form submissions
  • XSS prevention on submitted data
  • CSV injection prevention on exports
  • Input validation on all fields

Field Types:
  text, email, number, textarea, select, checkbox, radio, date, tel, url

Examples:
  smf run form-builder create
  smf run form-builder create --name "Contact Form" --fields name,email,message
  smf run form-builder serve FORM-ABC123 --port 8080
  smf run form-builder responses FORM-ABC123
  smf run form-builder export FORM-ABC123 --format csv

Serving Forms:
  The 'serve' command starts a local web server with CSRF protection.
  Access the form at: http://localhost:8080/FORM-ID
  Submissions are validated and saved automatically.
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
        
        print(f"📝 Form Builder")
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
            name = args[idx + 1] if idx + 1 < len(args) else "New Form"
            
            # Parse fields
            fields = []
            if "--fields" in args:
                f_idx = args.index("--fields")
                if f_idx + 1 < len(args):
                    field_names = args[f_idx + 1].split(",")
                    for fn in field_names:
                        if validate_field_name(fn):
                            fields.append({"name": fn, "type": "text", "label": fn.title()})
            
            result = create_form(name, "", fields)
        else:
            result = interactive_create_form()
        
        if result["success"]:
            print(f"\n✅ Form created: {result['form']['id']}")
            print(f"   Name: {result['form']['name']}")
            print(f"\n   Serve: smf run form-builder serve {result['form']['id']}")
            print(f"   View: smf run form-builder show {result['form']['id']}")
        else:
            print(f"❌ Failed: {result.get('error')}")
            return 1
    
    elif command == "list":
        forms = load_forms()
        display_forms(forms)
    
    elif command == "show":
        if len(args) < 1:
            print("❌ Form ID required")
            return 1
        
        display_form_details(args[0])
    
    elif command == "add-field":
        if len(args) < 1:
            print("❌ Form ID required")
            return 1
        
        form_id = args[0]
        
        # Interactive field addition
        print(f"\n➕ Add field to {form_id}")
        
        field_name = input("Field name: ").strip()
        if not field_name:
            print("❌ Field name required")
            return 1
        
        if not validate_field_name(field_name):
            print("❌ Invalid field name (use alphanumeric, underscore, hyphen)")
            return 1
        
        field_label = input("Label: ").strip() or field_name
        
        print("Field types:")
        for i, ft in enumerate(FIELD_TYPES, 1):
            print(f"  {i}. {ft}")
        
        type_choice = input("Choice [1]: ").strip() or "1"
        try:
            field_type = FIELD_TYPES[int(type_choice) - 1]
        except:
            field_type = "text"
        
        required = input("Required? (y/n) [n]: ").strip().lower() == "y"
        
        field = {
            "name": field_name,
            "label": field_label,
            "type": field_type,
            "required": required
        }
        
        result = add_field(form_id, field)
        
        if result["success"]:
            print(f"✅ Field added. Total fields: {len(result['form']['fields'])}")
        else:
            print(f"❌ Failed: {result.get('error')}")
            return 1
    
    elif command == "serve":
        if len(args) < 1:
            print("❌ Form ID required")
            return 1
        
        form_id = args[0]
        
        port = 8080
        if "--port" in args:
            idx = args.index("--port")
            if idx + 1 < len(args):
                try:
                    port = int(args[idx + 1])
                except:
                    pass
        
        serve_form(form_id, port)
    
    elif command == "responses":
        if len(args) < 1:
            print("❌ Form ID required")
            return 1
        
        form_id = args[0]
        responses = load_responses(form_id)
        display_responses(responses, form_id)
    
    elif command == "export":
        if len(args) < 1:
            print("❌ Form ID required")
            return 1
        
        form_id = args[0]
        
        format_type = "csv"
        if "--format" in args:
            idx = args.index("--format")
            if idx + 1 < len(args):
                format_type = args[idx + 1]
        
        output = None
        if "--output" in args:
            idx = args.index("--output")
            if idx + 1 < len(args):
                output = args[idx + 1]
        
        result = export_responses(form_id, format_type, output)
        
        if result["success"]:
            print(f"✅ Exported {result['count']} responses to {result['file']}")
        else:
            print(f"❌ Failed: {result.get('error')}")
            return 1
    
    elif command in ("help", "--help", "-h"):
        show_help()
    
    else:
        print(f"Unknown command: {command}")
        print("Run 'smf run form-builder help' for usage.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
