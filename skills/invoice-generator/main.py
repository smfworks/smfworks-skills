#!/usr/bin/env python3
"""
Invoice Generator - SMF Works Pro Skill
Create professional invoices, track payments, and manage billing.

Usage:
    smf run invoice-generator create --client "Acme Corp" --amount 1500 --description "Website redesign"
    smf run invoice-generator list
    smf run invoice-generator pay INV-001 --amount 1500 --method "bank-transfer"
    smf run invoice-generator report --month 2026-03
"""

import sys
import json
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from decimal import Decimal, ROUND_HALF_UP

# Add shared auth to path
shared_path = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from smf_auth import require_subscription, show_subscription_error

# Skill configuration
SKILL_NAME = "invoice-generator"
MIN_TIER = "pro"
INVOICES_DIR = Path.home() / ".smf" / "invoices"
CLIENTS_FILE = INVOICES_DIR / "clients.json"

# Invoice statuses
STATUSES = ["draft", "sent", "paid", "overdue", "cancelled"]


def ensure_dirs():
    """Ensure invoice directories exist."""
    INVOICES_DIR.mkdir(parents=True, exist_ok=True)
    if not CLIENTS_FILE.exists():
        CLIENTS_FILE.write_text(json.dumps({"clients": []}, indent=2))


def generate_invoice_number() -> str:
    """Generate unique invoice number."""
    timestamp = datetime.now().strftime("%Y%m")
    unique = uuid.uuid4().hex[:4].upper()
    return f"INV-{timestamp}-{unique}"


def format_currency(amount: Decimal, currency: str = "USD") -> str:
    """Format amount as currency string."""
    if currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "EUR":
        return f"€{amount:,.2f}"
    elif currency == "GBP":
        return f"£{amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"


def load_clients() -> List[Dict]:
    """Load all clients."""
    ensure_dirs()
    try:
        data = json.loads(CLIENTS_FILE.read_text())
        return data.get("clients", [])
    except:
        return []


def save_clients(clients: List[Dict]):
    """Save clients list."""
    ensure_dirs()
    CLIENTS_FILE.write_text(json.dumps({"clients": clients}, indent=2))


def get_client(client_name: str) -> Optional[Dict]:
    """Get client by name or ID."""
    clients = load_clients()
    for c in clients:
        if c["name"].lower() == client_name.lower() or c.get("id") == client_name:
            return c
    return None


def create_client(name: str, email: str = "", address: str = "", 
                  tax_id: str = "", payment_terms: int = 30) -> Dict:
    """Create a new client."""
    try:
        clients = load_clients()
        
        # Check if exists
        for c in clients:
            if c["name"].lower() == name.lower():
                return {"success": False, "error": f"Client '{name}' already exists"}
        
        client = {
            "id": f"client-{uuid.uuid4().hex[:8]}",
            "name": name,
            "email": email,
            "address": address,
            "tax_id": tax_id,
            "payment_terms": payment_terms,  # days
            "created_at": datetime.now().isoformat()
        }
        
        clients.append(client)
        save_clients(clients)
        
        return {"success": True, "client": client}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_invoice(client_name: str, items: List[Dict], 
                   tax_rate: Decimal = Decimal("0"),
                   discount: Decimal = Decimal("0"),
                   notes: str = "", 
                   due_days: int = 30) -> Dict:
    """Create a new invoice."""
    try:
        ensure_dirs()
        
        # Get or create client
        client = get_client(client_name)
        if not client:
            # Create client automatically
            result = create_client(client_name)
            if result["success"]:
                client = result["client"]
            else:
                return {"success": False, "error": f"Client not found: {client_name}"}
        
        # Calculate totals
        subtotal = Decimal("0")
        for item in items:
            qty = Decimal(str(item.get("quantity", 1)))
            price = Decimal(str(item.get("unit_price", 0)))
            item_total = qty * price
            item["total"] = float(item_total)
            subtotal += item_total
        
        # Apply discount
        discount_amount = subtotal * (discount / Decimal("100"))
        after_discount = subtotal - discount_amount
        
        # Calculate tax
        tax_amount = after_discount * (tax_rate / Decimal("100"))
        
        # Total
        total = after_discount + tax_amount
        
        invoice = {
            "id": generate_invoice_number(),
            "invoice_number": generate_invoice_number(),
            "client_id": client["id"],
            "client_name": client["name"],
            "client_email": client.get("email", ""),
            "client_address": client.get("address", ""),
            "items": items,
            "subtotal": float(subtotal),
            "discount_percent": float(discount),
            "discount_amount": float(discount_amount),
            "tax_percent": float(tax_rate),
            "tax_amount": float(tax_amount),
            "total": float(total),
            "currency": "USD",
            "status": "draft",
            "created_at": datetime.now().isoformat(),
            "due_date": (datetime.now() + timedelta(days=due_days)).strftime("%Y-%m-%d"),
            "paid_at": None,
            "payment_method": None,
            "notes": notes,
            "payments": []
        }
        
        # Save invoice
        invoice_file = INVOICES_DIR / f"{invoice['id']}.json"
        invoice_file.write_text(json.dumps(invoice, indent=2))
        
        return {"success": True, "invoice": invoice}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def load_invoice(invoice_id: str) -> Optional[Dict]:
    """Load invoice by ID."""
    invoice_file = INVOICES_DIR / f"{invoice_id}.json"
    if invoice_file.exists():
        try:
            return json.loads(invoice_file.read_text())
        except:
            pass
    return None


def load_invoices(client_id: str = None, status: str = None) -> List[Dict]:
    """Load invoices with optional filters."""
    ensure_dirs()
    
    invoices = []
    for invoice_file in INVOICES_DIR.glob("INV-*.json"):
        try:
            invoice = json.loads(invoice_file.read_text())
            
            # Apply filters
            if client_id and invoice.get("client_id") != client_id:
                continue
            if status and invoice.get("status") != status:
                continue
            
            invoices.append(invoice)
        except:
            continue
    
    # Sort by date (newest first)
    invoices.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return invoices


def update_invoice(invoice_id: str, updates: Dict) -> Dict:
    """Update invoice fields."""
    invoice = load_invoice(invoice_id)
    if not invoice:
        return {"success": False, "error": "Invoice not found"}
    
    # Apply updates
    for key, value in updates.items():
        if key in ["status", "paid_at", "payment_method", "notes"]:
            invoice[key] = value
    
    # Save back
    invoice_file = INVOICES_DIR / f"{invoice_id}.json"
    invoice_file.write_text(json.dumps(invoice, indent=2))
    
    return {"success": True, "invoice": invoice}


def record_payment(invoice_id: str, amount: float, method: str = "",
                  notes: str = "") -> Dict:
    """Record a payment on an invoice."""
    invoice = load_invoice(invoice_id)
    if not invoice:
        return {"success": False, "error": "Invoice not found"}
    
    # Add payment
    payment = {
        "amount": amount,
        "method": method,
        "notes": notes,
        "paid_at": datetime.now().isoformat()
    }
    
    if "payments" not in invoice:
        invoice["payments"] = []
    
    invoice["payments"].append(payment)
    
    # Calculate total paid
    total_paid = sum(p["amount"] for p in invoice["payments"])
    
    # Update status
    if total_paid >= invoice["total"]:
        invoice["status"] = "paid"
        invoice["paid_at"] = datetime.now().isoformat()
    elif total_paid > 0:
        invoice["status"] = "partial"
    
    invoice["payment_method"] = method if not invoice.get("payment_method") else invoice["payment_method"]
    
    # Save
    invoice_file = INVOICES_DIR / f"{invoice_id}.json"
    invoice_file.write_text(json.dumps(invoice, indent=2))
    
    return {"success": True, "invoice": invoice, "total_paid": total_paid}


def generate_invoice_html(invoice: Dict) -> str:
    """Generate HTML invoice for viewing/printing."""
    items_html = ""
    for item in invoice["items"]:
        items_html += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{item.get('description', '')}</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">{item.get('quantity', 1)}</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">${item.get('unit_price', 0):.2f}</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">${item.get('total', 0):.2f}</td>
        </tr>
        """
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Invoice {invoice['invoice_number']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
        .invoice {{ max-width: 800px; margin: 0 auto; }}
        .header {{ border-bottom: 3px solid #2563eb; padding-bottom: 20px; margin-bottom: 30px; }}
        .company {{ font-size: 24px; font-weight: bold; color: #2563eb; }}
        .invoice-title {{ font-size: 32px; color: #333; margin: 20px 0; }}
        .details {{ display: flex; justify-content: space-between; margin-bottom: 30px; }}
        .client-info {{ background: #f9fafb; padding: 20px; border-radius: 8px; }}
        .invoice-info {{ text-align: right; }}
        table {{ width: 100%; border-collapse: collapse; margin: 30px 0; }}
        th {{ background: #2563eb; color: white; padding: 12px; text-align: left; }}
        .totals {{ margin-left: auto; width: 300px; }}
        .total-row {{ display: flex; justify-content: space-between; padding: 8px 0; }}
        .total-row.grand {{ font-size: 20px; font-weight: bold; border-top: 2px solid #333; padding-top: 10px; margin-top: 10px; }}
        .status {{ display: inline-block; padding: 8px 16px; border-radius: 20px; font-weight: bold; }}
        .status-paid {{ background: #10b981; color: white; }}
        .status-draft {{ background: #6b7280; color: white; }}
        .status-sent {{ background: #3b82f6; color: white; }}
        .status-overdue {{ background: #ef4444; color: white; }}
        .notes {{ margin-top: 40px; padding: 20px; background: #f9fafb; border-radius: 8px; }}
        .footer {{ margin-top: 60px; text-align: center; color: #6b7280; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="invoice">
        <div class="header">
            <div class="company">YOUR COMPANY NAME</div>
            <div class="invoice-title">INVOICE</div>
            <div style="margin-top: 10px;">
                <span class="status status-{invoice['status']}">{invoice['status'].upper()}</span>
            </div>
        </div>
        
        <div class="details">
            <div class="client-info">
                <strong>Bill To:</strong><br>
                {invoice['client_name']}<br>
                {invoice.get('client_email', '')}<br>
                {invoice.get('client_address', '').replace(chr(10), '<br>')}
            </div>
            <div class="invoice-info">
                <strong>Invoice Number:</strong> {invoice['invoice_number']}<br>
                <strong>Date:</strong> {invoice['created_at'][:10]}<br>
                <strong>Due Date:</strong> {invoice['due_date']}<br>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Description</th>
                    <th style="text-align: right;">Qty</th>
                    <th style="text-align: right;">Unit Price</th>
                    <th style="text-align: right;">Total</th>
                </tr>
            </thead>
            <tbody>
                {items_html}
            </tbody>
        </table>
        
        <div class="totals">
            <div class="total-row">
                <span>Subtotal:</span>
                <span>${invoice['subtotal']:.2f}</span>
            </div>
            
            {f'''<div class="total-row">
                <span>Discount ({invoice["discount_percent"]}%):</span>
                <span>-${invoice["discount_amount"]:.2f}</span>
            </div>
            ''' if invoice.get('discount_amount', 0) > 0 else ''}
            
            {f'''<div class="total-row">
                <span>Tax ({invoice["tax_percent"]}%):</span>
                <span>${invoice["tax_amount"]:.2f}</span>
            </div>
            ''' if invoice.get('tax_amount', 0) > 0 else ''}
            
            <div class="total-row grand">
                <span>Total:</span>
                <span>${invoice['total']:.2f}</span>
            </div>
        </div>
        
        {f'''
        <div class="notes">
            <strong>Notes:</strong><br>
            {invoice["notes"]}
        </div>
        ''' if invoice.get('notes') else ''}
        
        <div class="footer">
            <p>Thank you for your business!</p>
            <p>Payment terms: Net 30 days</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def export_invoice(invoice_id: str, format: str = "html") -> Dict:
    """Export invoice to file."""
    invoice = load_invoice(invoice_id)
    if not invoice:
        return {"success": False, "error": "Invoice not found"}
    
    try:
        if format == "html":
            html = generate_invoice_html(invoice)
            output_file = INVOICES_DIR / f"{invoice_id}.html"
            output_file.write_text(html)
            return {"success": True, "file": str(output_file)}
        
        elif format == "json":
            output_file = INVOICES_DIR / f"{invoice_id}-export.json"
            output_file.write_text(json.dumps(invoice, indent=2))
            return {"success": True, "file": str(output_file)}
        
        else:
            return {"success": False, "error": f"Unsupported format: {format}"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_financial_report(year_month: str = None) -> Dict:
    """Generate financial report for period."""
    invoices = load_invoices()
    
    if year_month:
        # Filter by month
        invoices = [i for i in invoices if i.get("created_at", "").startswith(year_month)]
    
    # Calculate totals
    total_invoiced = sum(i["total"] for i in invoices)
    total_paid = sum(i["total"] for i in invoices if i["status"] == "paid")
    total_outstanding = sum(i["total"] - sum(p["amount"] for p in i.get("payments", [])) 
                           for i in invoices if i["status"] != "paid")
    
    # Count by status
    by_status = {}
    for status in STATUSES:
        count = len([i for i in invoices if i.get("status") == status])
        if count > 0:
            by_status[status] = count
    
    # Top clients
    by_client = {}
    for invoice in invoices:
        client = invoice["client_name"]
        by_client[client] = by_client.get(client, 0) + invoice["total"]
    
    top_clients = sorted(by_client.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "period": year_month or "all time",
        "total_invoices": len(invoices),
        "total_invoiced": total_invoiced,
        "total_paid": total_paid,
        "total_outstanding": total_outstanding,
        "collection_rate": (total_paid / total_invoiced * 100) if total_invoiced > 0 else 0,
        "by_status": by_status,
        "top_clients": top_clients
    }


def display_invoice_list(invoices: List[Dict], title: str = "Invoices"):
    """Display invoices in formatted list."""
    if not invoices:
        print(f"\nNo {title.lower()} found.")
        return
    
    print(f"\n📄 {title} ({len(invoices)})")
    print("-" * 90)
    print(f"{'Number':<20} {'Client':<25} {'Date':<12} {'Amount':<12} {'Status':<12}")
    print("-" * 90)
    
    for inv in invoices[:20]:
        number = inv['invoice_number']
        client = inv['client_name'][:23]
        date = inv['created_at'][:10]
        amount = f"${inv['total']:.2f}"
        
        status_icon = {
            "paid": "✅",
            "sent": "📤",
            "draft": "📝",
            "overdue": "⚠️",
            "cancelled": "❌"
        }.get(inv['status'], "•")
        
        status = f"{status_icon} {inv['status']}"
        
        print(f"{number:<20} {client:<25} {date:<12} {amount:<12} {status:<12}")
    
    if len(invoices) > 20:
        print(f"\n... and {len(invoices) - 20} more")
    
    print("-" * 90)


def interactive_create_invoice():
    """Interactive invoice creation."""
    print("\n📄 Create Invoice")
    print("-" * 40)
    
    # Get client
    client_name = input("Client name: ").strip()
    if not client_name:
        print("❌ Client name required")
        return {"success": False, "error": "Client required"}
    
    # Build items list
    items = []
    print("\nEnter invoice items (blank description to finish):")
    
    while True:
        print(f"\nItem {len(items) + 1}:")
        desc = input("Description: ").strip()
        if not desc:
            break
        
        qty_str = input("Quantity [1]: ").strip() or "1"
        try:
            qty = float(qty_str)
        except:
            qty = 1
        
        price_str = input("Unit price: ").strip()
        try:
            price = float(price_str)
        except:
            print("❌ Invalid price, skipping item")
            continue
        
        items.append({
            "description": desc,
            "quantity": qty,
            "unit_price": price
        })
    
    if not items:
        print("❌ At least one item required")
        return {"success": False, "error": "Items required"}
    
    # Tax and discount
    tax_str = input("\nTax rate % [0]: ").strip() or "0"
    try:
        tax_rate = Decimal(tax_str)
    except:
        tax_rate = Decimal("0")
    
    discount_str = input("Discount % [0]: ").strip() or "0"
    try:
        discount = Decimal(discount_str)
    except:
        discount = Decimal("0")
    
    notes = input("Notes (optional): ").strip()
    
    return create_invoice(client_name, items, tax_rate, discount, notes)


def show_help():
    """Show help message."""
    print("""📄 Invoice Generator

Create professional invoices and track payments.

Commands:
  client add "Name"            Add new client
  client list                  List all clients
  create                       Create invoice (interactive)
  create --client NAME         Create for client
  list                         List all invoices
  list --status STATUS         Filter by status
  show INV-ID                  Show invoice details
  pay INV-ID                   Record payment
  export INV-ID --html         Export as HTML
  report                       Financial report
  report --month YYYY-MM       Monthly report
  help                         Show this help

Examples:
  smf run invoice-generator client add "Acme Corp"
  smf run invoice-generator create --client "Acme" --item "Design:1500"
  smf run invoice-generator list
  smf run invoice-generator pay INV-202603-ABC123 --amount 1500
  smf run invoice-generator export INV-202603-ABC123
  smf run invoice-generator report --month 2026-03
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
        
        print(f"📄 Invoice Generator")
        print(f"   Subscription: {subscription['tier']}")
        print("")
    
    # Parse command
    if len(sys.argv) < 2:
        show_help()
        return 0
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "client":
        if len(args) < 1:
            print("❌ Client command required (add, list)")
            return 1
        
        subcommand = args[0]
        
        if subcommand == "add":
            if len(args) < 2:
                print("❌ Client name required")
                return 1
            
            name = args[1]
            result = create_client(name)
            
            if result["success"]:
                print(f"✅ Client added: {result['client']['name']}")
                print(f"   ID: {result['client']['id']}")
            else:
                print(f"❌ {result['error']}")
                return 1
        
        elif subcommand == "list":
            clients = load_clients()
            
            if not clients:
                print("No clients found.")
                return 0
            
            print(f"\n👥 {len(clients)} Client(s)")
            print("-" * 60)
            
            for c in clients:
                print(f"• {c['name']}")
                if c.get('email'):
                    print(f"  Email: {c['email']}")
        
        else:
            print(f"Unknown client command: {subcommand}")
            return 1
    
    elif command == "create":
        if "--client" in args:
            # Quick create mode
            idx = args.index("--client")
            if idx + 1 >= len(args):
                print("❌ --client requires a name")
                return 1
            
            client_name = args[idx + 1]
            
            # Parse items
            items = []
            i = 0
            while i < len(args):
                if args[i] == "--item" and i + 1 < len(args):
                    # Format: "Description:100" or "Description:2:50" (qty:price)
                    item_str = args[i + 1]
                    parts = item_str.split(":")
                    
                    if len(parts) == 2:
                        desc, price = parts
                        qty = 1
                    elif len(parts) == 3:
                        desc, qty, price = parts
                        qty = float(qty)
                    else:
                        desc = parts[0]
                        price = parts[-1]
                        qty = 1
                    
                    try:
                        price = float(price)
                    except:
                        price = 0
                    
                    items.append({
                        "description": desc,
                        "quantity": qty,
                        "unit_price": price
                    })
                    i += 2
                else:
                    i += 1
            
            if not items:
                # Default item
                items = [{"description": "Services", "quantity": 1, "unit_price": 100}]
            
            result = create_invoice(client_name, items)
        else:
            # Interactive mode
            result = interactive_create_invoice()
        
        if result["success"]:
            print(f"\n✅ Invoice created: {result['invoice']['invoice_number']}")
            print(f"   Client: {result['invoice']['client_name']}")
            print(f"   Total: ${result['invoice']['total']:.2f}")
            print(f"   Due: {result['invoice']['due_date']}")
            print(f"\n   Export: smf run invoice-generator export {result['invoice']['id']}")
        else:
            print(f"❌ {result['error']}")
            return 1
    
    elif command == "list":
        status_filter = None
        if "--status" in args:
            idx = args.index("--status")
            if idx + 1 < len(args):
                status_filter = args[idx + 1]
        
        invoices = load_invoices(status=status_filter)
        display_invoice_list(invoices, f"Invoices")
    
    elif command == "show":
        if len(args) < 1:
            print("❌ Invoice ID required")
            return 1
        
        invoice_id = args[0]
        invoice = load_invoice(invoice_id)
        
        if not invoice:
            print(f"❌ Invoice not found: {invoice_id}")
            return 1
        
        print(f"\n📄 Invoice {invoice['invoice_number']}")
        print("=" * 60)
        print(f"Status: {invoice['status'].upper()}")
        print(f"Client: {invoice['client_name']}")
        print(f"Date: {invoice['created_at'][:10]}")
        print(f"Due: {invoice['due_date']}")
        print(f"\nItems:")
        for item in invoice['items']:
            print(f"  • {item['description']}: {item['quantity']} x ${item['unit_price']:.2f} = ${item['total']:.2f}")
        
        print(f"\nSubtotal: ${invoice['subtotal']:.2f}")
        if invoice.get('discount_amount', 0) > 0:
            print(f"Discount: -${invoice['discount_amount']:.2f}")
        if invoice.get('tax_amount', 0) > 0:
            print(f"Tax: ${invoice['tax_amount']:.2f}")
        print(f"Total: ${invoice['total']:.2f}")
    
    elif command == "pay":
        if len(args) < 1:
            print("❌ Invoice ID required")
            return 1
        
        invoice_id = args[0]
        
        # Get payment details
        amount_str = input("Payment amount: ").strip()
        try:
            amount = float(amount_str)
        except:
            print("❌ Invalid amount")
            return 1
        
        method = input("Payment method [bank-transfer]: ").strip() or "bank-transfer"
        notes = input("Notes: ").strip()
        
        result = record_payment(invoice_id, amount, method, notes)
        
        if result["success"]:
            print(f"✅ Payment recorded: ${amount:.2f}")
            print(f"   Total paid: ${result['total_paid']:.2f}")
            print(f"   Status: {result['invoice']['status']}")
        else:
            print(f"❌ {result['error']}")
            return 1
    
    elif command == "export":
        if len(args) < 1:
            print("❌ Invoice ID required")
            return 1
        
        invoice_id = args[0]
        format_type = "html"
        
        if "--json" in args:
            format_type = "json"
        
        result = export_invoice(invoice_id, format_type)
        
        if result["success"]:
            print(f"✅ Invoice exported: {result['file']}")
        else:
            print(f"❌ {result['error']}")
            return 1
    
    elif command == "report":
        month = None
        if "--month" in args:
            idx = args.index("--month")
            if idx + 1 < len(args):
                month = args[idx + 1]
        
        report = get_financial_report(month)
        
        print(f"\n💰 Financial Report: {report['period']}")
        print("=" * 50)
        print(f"\nTotal Invoices: {report['total_invoices']}")
        print(f"Total Invoiced: ${report['total_invoiced']:.2f}")
        print(f"Total Paid: ${report['total_paid']:.2f}")
        print(f"Outstanding: ${report['total_outstanding']:.2f}")
        print(f"Collection Rate: {report['collection_rate']:.1f}%")
        
        if report['top_clients']:
            print(f"\nTop Clients:")
            for client, amount in report['top_clients']:
                print(f"  • {client}: ${amount:.2f}")
    
    elif command in ("help", "--help", "-h"):
        show_help()
    
    else:
        print(f"Unknown command: {command}")
        print("Run 'smf run invoice-generator help' for usage.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
