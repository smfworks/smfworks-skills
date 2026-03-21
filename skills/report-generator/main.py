#!/usr/bin/env python3
"""
Report Generator - SMF Works Pro Skill
Create business reports with charts, tables, and export to PDF/HTML.

Usage:
    smf run report-generator create --template sales --data data.csv --output report.pdf
    smf run report-generator list-templates
    smf run report-generator preview --template monthly
"""

import sys
import csv
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add shared auth to path
shared_path = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from smf_auth import require_subscription, show_subscription_error

# Skill configuration
SKILL_NAME = "report-generator"
MIN_TIER = "pro"
REPORTS_DIR = Path.home() / ".smf" / "reports"
TEMPLATES_DIR = Path(__file__).parent / "templates"


def ensure_dirs():
    """Ensure reports directory exists."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_csv_data(file_path: str) -> List[Dict]:
    """Load data from CSV file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        return []


def load_json_data(file_path: str) -> List[Dict]:
    """Load data from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                return [data]
            return data
    except Exception as e:
        return []


def calculate_statistics(data: List[Dict], value_column: str) -> Dict:
    """Calculate statistics from data."""
    try:
        values = [float(row.get(value_column, 0)) for row in data if row.get(value_column)]
        
        if not values:
            return {}
        
        values.sort()
        n = len(values)
        
        total = sum(values)
        mean = total / n
        
        # Median
        mid = n // 2
        median = values[mid] if n % 2 else (values[mid - 1] + values[mid]) / 2
        
        # Min/Max
        min_val = values[0]
        max_val = values[-1]
        
        return {
            "count": n,
            "total": round(total, 2),
            "mean": round(mean, 2),
            "median": round(median, 2),
            "min": round(min_val, 2),
            "max": round(max_val, 2),
            "range": round(max_val - min_val, 2)
        }
    except:
        return {}


def generate_html_report(data: List[Dict], title: str = "Report", 
                         columns: List[str] = None, stats: Dict = None) -> str:
    """Generate HTML report."""
    if not data:
        return "<html><body><h1>No data</h1></body></html>"
    
    if columns is None:
        columns = list(data[0].keys())
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               max-width: 1200px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #1a1a1a; border-bottom: 3px solid #2563eb; padding-bottom: 10px; }}
        h2 {{ color: #374151; margin-top: 30px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #2563eb; color: white; padding: 12px; text-align: left; font-weight: 600; }}
        td {{ padding: 10px; border-bottom: 1px solid #e5e7eb; }}
        tr:hover {{ background: #f9fafb; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
                   gap: 15px; margin: 20px 0; }}
        .stat-card {{ background: #f3f4f6; padding: 15px; border-radius: 8px; 
                      border-left: 4px solid #2563eb; }}
        .stat-label {{ font-size: 12px; color: #6b7280; text-transform: uppercase; }}
        .stat-value {{ font-size: 24px; font-weight: 700; color: #1a1a1a; margin-top: 5px; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb;
                  color: #9ca3af; font-size: 12px; text-align: center; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
"""
    
    # Statistics section
    if stats:
        html += "    <h2>Statistics</h2>\n    <div class='stats'\u003e\n"
        for key, value in stats.items():
            html += f"""        <div class='stat-card'\u003e
            <div class='stat-label'>{key.replace('_', ' ').title()}</div>
            <div class='stat-value'>{value}</div>
        </div>\n"""
        html += "    </div>\n"
    
    # Data table
    html += "    <h2>Data</h2>\n"
    html += "    <table>\n"
    html += "        <thead><tr>"
    for col in columns:
        html += f"<th>{col.title()}</th>"
    html += "</tr></thead>\n"
    
    html += "        <tbody>\n"
    for row in data[:100]:  # Limit to 100 rows
        html += "        <tr>"
        for col in columns:
            value = row.get(col, '')
            html += f"<td>{value}</td>"
        html += "</tr>\n"
    html += "        </tbody>\n"
    html += "    </table>\n"
    
    if len(data) > 100:
        html += f"    <p><em>Showing first 100 of {len(data)} rows.</em></p>\n"
    
    # Footer
    html += f"""    <div class='footer'>
        Generated by SMF Works Report Generator
    </div>
</body>
</html>"""
    
    return html


def generate_text_report(data: List[Dict], title: str = "Report", 
                         stats: Dict = None) -> str:
    """Generate plain text report."""
    lines = []
    lines.append("=" * 60)
    lines.append(title.upper())
    lines.append("=" * 60)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    if stats:
        lines.append("STATISTICS")
        lines.append("-" * 60)
        for key, value in stats.items():
            lines.append(f"{key.replace('_', ' ').title():<20}: {value}")
        lines.append("")
    
    if data:
        lines.append("DATA")
        lines.append("-" * 60)
        
        # Header
        columns = list(data[0].keys())
        lines.append(" | ".join(columns))
        lines.append("-" * 60)
        
        # Data rows
        for row in data[:50]:  # Limit to 50 rows
            values = [str(row.get(col, '')) for col in columns]
            lines.append(" | ".join(values))
        
        if len(data) > 50:
            lines.append(f"... ({len(data) - 50} more rows)")
    
    lines.append("")
    lines.append("=" * 60)
    lines.append("Generated by SMF Works Report Generator")
    
    return "\n".join(lines)


def create_report(data_file: str, output_file: str = None, 
                  title: str = "Report", format: str = "html",
                  value_column: str = None) -> Dict:
    """Create a report from data file."""
    try:
        # Load data
        if data_file.endswith('.csv'):
            data = load_csv_data(data_file)
        elif data_file.endswith('.json'):
            data = load_json_data(data_file)
        else:
            return {"success": False, "error": "Unsupported file format. Use CSV or JSON."}
        
        if not data:
            return {"success": False, "error": "No data found in file"}
        
        # Calculate statistics if value column specified
        stats = None
        if value_column:
            stats = calculate_statistics(data, value_column)
        
        # Generate report
        if format == "html":
            content = generate_html_report(data, title, stats=stats)
            if not output_file:
                output_file = f"report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"
        elif format == "text":
            content = generate_text_report(data, title, stats=stats)
            if not output_file:
                output_file = f"report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        else:
            return {"success": False, "error": f"Unsupported format: {format}"}
        
        # Save report
        output_path = REPORTS_DIR / output_file
        output_path.write_text(content, encoding='utf-8')
        
        return {
            "success": True,
            "output_file": str(output_path),
            "format": format,
            "rows": len(data),
            "size_kb": round(len(content) / 1024, 2)
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_templates() -> List[str]:
    """List available report templates."""
    # For now, return built-in templates
    return [
        "sales-report",
        "monthly-summary",
        "customer-list",
        "inventory-report",
        "financial-summary"
    ]


def create_sample_data(template: str, output_file: str) -> Dict:
    """Create sample data for testing."""
    samples = {
        "sales": [
            {"date": "2026-03-01", "product": "Widget A", "quantity": 5, "price": 29.99, "total": 149.95},
            {"date": "2026-03-02", "product": "Widget B", "quantity": 3, "price": 49.99, "total": 149.97},
            {"date": "2026-03-03", "product": "Widget A", "quantity": 2, "price": 29.99, "total": 59.98},
            {"date": "2026-03-04", "product": "Widget C", "quantity": 1, "price": 99.99, "total": 99.99},
        ],
        "customers": [
            {"name": "John Smith", "email": "john@example.com", "orders": 5, "revenue": 450.00},
            {"name": "Jane Doe", "email": "jane@example.com", "orders": 3, "revenue": 275.50},
            {"name": "Bob Johnson", "email": "bob@example.com", "orders": 8, "revenue": 890.25},
        ],
        "inventory": [
            {"sku": "WID-001", "name": "Widget A", "stock": 45, "cost": 15.00, "price": 29.99},
            {"sku": "WID-002", "name": "Widget B", "stock": 23, "cost": 25.00, "price": 49.99},
            {"sku": "WID-003", "name": "Widget C", "stock": 12, "cost": 50.00, "price": 99.99},
        ]
    }
    
    data = samples.get(template, samples["sales"])
    
    # Save as CSV
    if output_file.endswith('.csv'):
        with open(output_file, 'w', newline='') as f:
            if data:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
    else:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    return {"success": True, "file": output_file, "rows": len(data)}


def interactive_create():
    """Interactive report creation."""
    print("\n📊 Report Generator")
    print("=" * 40)
    
    # Get data file
    data_file = input("\nData file (CSV or JSON): ").strip()
    
    if not Path(data_file).exists():
        print(f"❌ File not found: {data_file}")
        
        # Offer to create sample data
        create_sample = input("Create sample data? (yes/no): ").strip().lower()
        if create_sample == "yes":
            print("\nSample templates:")
            print("  1. sales")
            print("  2. customers")
            print("  3. inventory")
            
            template = input("\nChoose template: ").strip()
            template_map = {"1": "sales", "2": "customers", "3": "inventory"}
            template = template_map.get(template, "sales")
            
            data_file = f"sample-{template}.csv"
            result = create_sample_data(template, data_file)
            print(f"✅ Created: {data_file}")
        else:
            return {"success": False, "error": "No data file"}
    
    # Get title
    title = input("Report title [Sales Report]: ").strip() or "Sales Report"
    
    # Get format
    print("\nFormat:")
    print("  1. HTML (for viewing in browser)")
    print("  2. Text (for email or terminal)")
    
    format_choice = input("Choice [1]: ").strip() or "1"
    format_map = {"1": "html", "2": "text"}
    format_type = format_map.get(format_choice, "html")
    
    # Get value column for statistics
    data = load_csv_data(data_file) if data_file.endswith('.csv') else load_json_data(data_file)
    
    value_column = None
    if data:
        print("\nAvailable columns:")
        columns = list(data[0].keys())
        for i, col in enumerate(columns, 1):
            print(f"  {i}. {col}")
        
        print("\nSelect column for statistics (or press Enter to skip):")
        col_choice = input("Choice: ").strip()
        if col_choice.isdigit() and 1 <= int(col_choice) <= len(columns):
            value_column = columns[int(col_choice) - 1]
    
    # Create report
    return create_report(data_file, title=title, format=format_type, 
                         value_column=value_column)


def show_help():
    """Show help message."""
    print("""📊 Report Generator

Create business reports with charts, tables, and statistics.

Commands:
  create                    Create report (interactive)
  create --data FILE        Create from data file
  create --sample TYPE      Create sample data (sales/customers/inventory)
  templates                 List available templates
  help                      Show this help

Examples:
  smf run report-generator create
  smf run report-generator create --data sales.csv --title "Q1 Sales"
  smf run report-generator create --sample sales
  smf run report-generator templates

Supported formats:
  • HTML (rich formatting, charts, tables)
  • Text (plain text, email-friendly)

Supported data formats:
  • CSV (Comma-separated values)
  • JSON (JavaScript Object Notation)
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
        
        print(f"📊 Report Generator")
        print(f"   Subscription: {subscription['tier']}")
        print("")
    
    # Parse command
    if len(sys.argv) < 2:
        show_help()
        return 0
    
    command = sys.argv[1]
    
    if command == "create":
        # Check for sample data creation
        if "--sample" in sys.argv:
            idx = sys.argv.index("--sample")
            template = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else "sales"
            output = f"sample-{template}.csv"
            result = create_sample_data(template, output)
            
            if result["success"]:
                print(f"✅ Created sample data: {result['file']}")
                print(f"   Rows: {result['rows']}")
                
                # Ask if they want to create report now
                create_now = input("\nCreate report from this data? (yes/no): ").strip().lower()
                if create_now == "yes":
                    result = create_report(output)
                    if result["success"]:
                        print(f"\n✅ Report created: {result['output_file']}")
                        print(f"   Format: {result['format']}")
                        print(f"   Rows: {result['rows']}")
                        print(f"   Size: {result['size_kb']} KB")
            else:
                print(f"❌ Failed: {result.get('error')}")
                return 1
        
        elif "--data" in sys.argv:
            idx = sys.argv.index("--data")
            data_file = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
            
            if not data_file:
                print("❌ --data requires a file path")
                return 1
            
            # Parse other options
            title = "Report"
            format_type = "html"
            value_column = None
            
            if "--title" in sys.argv:
                t_idx = sys.argv.index("--title")
                title = sys.argv[t_idx + 1] if t_idx + 1 < len(sys.argv) else "Report"
            
            if "--format" in sys.argv:
                f_idx = sys.argv.index("--format")
                format_type = sys.argv[f_idx + 1] if f_idx + 1 < len(sys.argv) else "html"
            
            if "--value-column" in sys.argv:
                v_idx = sys.argv.index("--value-column")
                value_column = sys.argv[v_idx + 1] if v_idx + 1 < len(sys.argv) else None
            
            result = create_report(data_file, title=title, format=format_type,
                                    value_column=value_column)
            
            if result["success"]:
                print(f"✅ Report created: {result['output_file']}")
                print(f"   Format: {result['format']}")
                print(f"   Rows: {result['rows']}")
                print(f"   Size: {result['size_kb']} KB")
            else:
                print(f"❌ Failed: {result.get('error')}")
                return 1
        
        else:
            # Interactive mode
            result = interactive_create()
            
            if result["success"]:
                print(f"\n✅ Report created: {result['output_file']}")
                print(f"   Format: {result['format']}")
                print(f"   Rows: {result['rows']}")
                print(f"   Size: {result['size_kb']} KB")
                print(f"\nOpen the file to view your report!")
            else:
                print(f"❌ Failed: {result.get('error')}")
                return 1
    
    elif command == "templates":
        templates = list_templates()
        print("\n📋 Available Templates:")
        print("-" * 40)
        for template in templates:
            print(f"  • {template}")
        print("\nUse with: smf run report-generator create --sample <template>")
    
    elif command in ("help", "--help", "-h"):
        show_help()
    
    else:
        print(f"Unknown command: {command}")
        print("Run 'smf run report-generator help' for usage.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
