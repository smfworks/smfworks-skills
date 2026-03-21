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
import html as html_module
from pathlib import Path
from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

# Add shared auth to path
shared_path = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from smf_auth import require_subscription, show_subscription_error

# Skill configuration
SKILL_NAME = "report-generator"
MIN_TIER = "pro"
REPORTS_DIR = Path.home() / ".smf" / "reports"
TEMPLATES_DIR = Path(__file__).parent / "templates"

# Constants for data processing
MAX_ROWS_DISPLAY = 100
MAX_ROWS_PROCESS = 10000
MAX_FILE_SIZE_MB = 50


def ensure_dirs():
    """Ensure reports directory exists."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def infer_column_type(values: List[str]) -> str:
    """
    Infer the data type of a column from sample values.
    Returns: 'numeric', 'date', 'currency', 'text'
    """
    non_empty = [v for v in values if v and v.strip()]
    if not non_empty:
        return 'text'
    
    # Sample up to 20 values for type inference
    sample = non_empty[:20]
    
    # Check for currency pattern
    currency_pattern = 0
    for v in sample:
        # Match $XX,XXX.XX or €XX.XX or £XX.XX
        clean = v.strip().replace(',', '').replace('$', '').replace('€', '').replace('£', '')
        try:
            Decimal(clean)
            currency_pattern += 1
        except InvalidOperation:
            pass
    
    if currency_pattern >= len(sample) * 0.7:
        return 'currency'
    
    # Check for numeric pattern
    numeric_count = 0
    for v in sample:
        clean = v.strip().replace(',', '')
        try:
            float(clean)
            numeric_count += 1
        except ValueError:
            pass
    
    if numeric_count >= len(sample) * 0.7:
        return 'numeric'
    
    # Check for date pattern (simple check)
    date_patterns = 0
    for v in sample:
        v_clean = v.strip()
        # Common date separators
        if '-' in v_clean or '/' in v_clean:
            parts = v_clean.replace('/', '-').split('-')
            if len(parts) == 3:
                try:
                    [int(p) for p in parts]
                    date_patterns += 1
                except ValueError:
                    pass
    
    if date_patterns >= len(sample) * 0.5:
        return 'date'
    
    return 'text'


def parse_numeric_value(value: Any, column_type: str = 'numeric') -> Optional[Decimal]:
    """Safely parse a numeric value with type awareness."""
    if value is None or value == '':
        return None
    
    str_value = str(value)
    
    if column_type == 'currency':
        # Remove currency symbols and thousands separators
        clean = str_value.replace(',', '').replace('$', '').replace('€', '').replace('£', '')
    else:
        clean = str_value.replace(',', '')
    
    try:
        return Decimal(clean)
    except (InvalidOperation, ValueError):
        return None


def format_cell(value: Any, column_type: str = 'text') -> str:
    """Format a cell value based on its inferred type."""
    if value is None or value == '':
        return ''
    
    if column_type == 'currency':
        parsed = parse_numeric_value(value, 'currency')
        if parsed is not None:
            return f"${parsed:,.2f}"
        return str(value)
    
    elif column_type == 'numeric':
        parsed = parse_numeric_value(value, 'numeric')
        if parsed is not None:
            # Format with appropriate precision
            if parsed == parsed.to_integral_value():
                return f"{int(parsed):,}"
            else:
                return f"{parsed:,.2f}"
        return str(value)
    
    elif column_type == 'date':
        # Return as-is for dates
        return str(value)
    
    else:
        # Text - ensure safe for CSV/display
        return str(value)


def validate_file_size(file_path: Path, max_mb: int = MAX_FILE_SIZE_MB) -> bool:
    """Check if file size is within acceptable limits."""
    try:
        size_mb = file_path.stat().st_size / (1024 * 1024)
        return size_mb <= max_mb
    except OSError:
        return False


def load_csv_data(file_path: str) -> List[Dict]:
    """Load data from CSV file with type inference and validation."""
    try:
        path = Path(file_path).expanduser().resolve()
        
        # Check file size
        if not validate_file_size(path):
            print(f"⚠️  Warning: Large file ({path.stat().st_size / 1024 / 1024:.1f} MB)", file=sys.stderr)
        
        # Check file exists
        if not path.exists():
            return []
        
        with open(path, 'r', encoding='utf-8-sig') as f:  # utf-8-sig handles BOM
            # Detect if file has headers
            sample = f.read(8192)
            f.seek(0)
            
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
            except csv.Error:
                dialect = csv.excel
            
            reader = csv.DictReader(f, dialect=dialect)
            
            if reader.fieldnames is None:
                return []
            
            data = []
            row_count = 0
            
            for row in reader:
                # Skip empty rows
                if not any(row.values()):
                    continue
                
                # Clean keys and values
                clean_row = {}
                for k, v in row.items():
                    if k:
                        clean_row[k.strip()] = v.strip() if v else ''
                
                data.append(clean_row)
                row_count += 1
                
                # Limit processing for very large datasets
                if row_count >= MAX_ROWS_PROCESS:
                    print(f"⚠️  Large dataset: processing first {MAX_ROWS_PROCESS} rows only", file=sys.stderr)
                    break
            
            return data
    
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}", file=sys.stderr)
        return []
    except PermissionError:
        print(f"❌ Permission denied: {file_path}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"❌ CSV load error: {e}", file=sys.stderr)
        return []


def load_json_data(file_path: str) -> List[Dict]:
    """Load data from JSON file with validation."""
    try:
        path = Path(file_path).expanduser().resolve()
        
        # Check file size
        if not validate_file_size(path):
            print(f"⚠️  Warning: Large file ({path.stat().st_size / 1024 / 1024:.1f} MB)", file=sys.stderr)
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            if isinstance(data, dict):
                # Single object - wrap in list
                return [data]
            elif isinstance(data, list):
                # Check size for large arrays
                if len(data) > MAX_ROWS_PROCESS:
                    print(f"⚠️  Large dataset: processing first {MAX_ROWS_PROCESS} rows only", file=sys.stderr)
                    return data[:MAX_ROWS_PROCESS]
                return data
            else:
                return []
    
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}", file=sys.stderr)
        return []
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"❌ JSON load error: {e}", file=sys.stderr)
        return []


def analyze_column_types(data: List[Dict]) -> Dict[str, str]:
    """Analyze columns and infer their types."""
    if not data:
        return {}
    
    columns = list(data[0].keys())
    types = {}
    
    for col in columns:
        values = [str(row.get(col, '')) for row in data]
        types[col] = infer_column_type(values)
    
    return types


def calculate_statistics(data: List[Dict], value_column: str) -> Dict:
    """Calculate statistics from data with proper type handling."""
    if not data or not value_column:
        return {}
    
    try:
        # Infer column type
        col_type = infer_column_type([str(row.get(value_column, '')) for row in data])
        
        if col_type not in ('numeric', 'currency'):
            return {"error": f"Column '{value_column}' is not numeric (detected as {col_type})"}
        
        # Parse values
        values = []
        for row in data:
            parsed = parse_numeric_value(row.get(value_column, 0), col_type)
            if parsed is not None:
                values.append(parsed)
        
        if not values:
            return {"error": "No valid numeric values found"}
        
        # Sort for percentile calculations
        values.sort()
        n = len(values)
        
        total = sum(values)
        mean = total / n
        
        # Median
        mid = n // 2
        if n % 2 == 0:
            median = (values[mid - 1] + values[mid]) / 2
        else:
            median = values[mid]
        
        # Min/Max
        min_val = values[0]
        max_val = values[-1]
        
        # Percentiles
        p25 = values[int(n * 0.25)] if n > 4 else values[0]
        p75 = values[int(n * 0.75)] if n > 4 else values[-1]
        
        return {
            "count": n,
            "total": round(total, 2),
            "mean": round(float(mean), 2),
            "median": round(float(median), 2),
            "min": round(float(min_val), 2),
            "max": round(float(max_val), 2),
            "range": round(float(max_val - min_val), 2),
            "p25": round(float(p25), 2),
            "p75": round(float(p75), 2),
            "type": col_type
        }
    
    except Exception as e:
        return {"error": str(e)}


def generate_html_report(data: List[Dict], title: str = "Report", 
                         columns: List[str] = None, stats: Dict = None) -> str:
    """Generate HTML report with XSS protection."""
    if not data:
        return "<html><body><h1>No data</h1></body></html>"
    
    if columns is None:
        columns = list(data[0].keys())
    
    # Analyze column types for formatting
    col_types = analyze_column_types(data)
    
    # Escape title
    safe_title = html_module.escape(title)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{safe_title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               max-width: 1200px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #1a1a1a; border-bottom: 3px solid #2563eb; padding-bottom: 10px; }}
        h2 {{ color: #374151; margin-top: 30px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; overflow-x: auto; display: block; }}
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
        .numeric {{ text-align: right; font-family: monospace; }}
        .currency {{ text-align: right; color: #059669; font-family: monospace; }}
    </style>
</head>
<body>
    <h1>{safe_title}</h1>
    <p>Generated: {html_module.escape(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}</p>
"""
    
    # Statistics section
    if stats and 'error' not in stats:
        html += "    <h2>Statistics</h2>\n    <div class='stats'>\n"
        for key, value in stats.items():
            if key not in ('error', 'type'):
                formatted_val = value
                if isinstance(value, (int, float)):
                    formatted_val = f"{value:,.2f}"
                html += f"""        <div class='stat-card'>
            <div class='stat-label'>{html_module.escape(key.replace('_', ' ').title())}</div>
            <div class='stat-value'>{html_module.escape(str(formatted_val))}</div>
        </div>\n"""
        html += "    </div>\n"
    elif stats and 'error' in stats:
        html += f"    <p style='color: #dc2626;'>⚠️ {html_module.escape(stats['error'])}</p>\n"
    
    # Data table
    html += "    <h2>Data</h2>\n"
    html += "    <div style='overflow-x: auto;'>\n"
    html += "    <table>\n"
    html += "        <thead><tr>"
    for col in columns:
        safe_col = html_module.escape(col)
        html += f"<th>{safe_col}</th>"
    html += "</tr></thead>\n"
    
    html += "        <tbody>\n"
    display_count = min(len(data), MAX_ROWS_DISPLAY)
    for row in data[:display_count]:
        html += "        <tr>"
        for col in columns:
            value = row.get(col, '')
            col_type = col_types.get(col, 'text')
            formatted = format_cell(value, col_type)
            safe_value = html_module.escape(str(formatted))
            css_class = f" class='{col_type}'" if col_type in ('numeric', 'currency') else ""
            html += f"<td{css_class}>{safe_value}</td>"
        html += "</tr>\n"
    html += "        </tbody>\n"
    html += "    </table>\n"
    html += "    </div>\n"
    
    if len(data) > MAX_ROWS_DISPLAY:
        html += f"    <p><em>Showing first {display_count} of {len(data)} rows.</em></p>\n"
    
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
    
    # Analyze column types
    col_types = analyze_column_types(data) if data else {}
    
    if stats:
        if 'error' not in stats:
            lines.append("STATISTICS")
            lines.append("-" * 60)
            for key, value in stats.items():
                if key not in ('error', 'type'):
                    lines.append(f"{key.replace('_', ' ').title():<20}: {value}")
            lines.append("")
        else:
            lines.append(f"STATISTICS: {stats['error']}")
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
            values = [format_cell(row.get(col, ''), col_types.get(col, 'text')) for col in columns]
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
    """Create a report from data file with proper error handling."""
    try:
        # Load data with type detection
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
            "size_kb": round(len(content) / 1024, 2),
            "columns": list(data[0].keys()) if data else []
        }
        
    except Exception as e:
        return {"success": False, "error": f"Report creation failed: {e}"}


def list_templates() -> List[str]:
    """List available report templates."""
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
            {"date": "2026-03-01", "product": "Widget A", "quantity": 5, "price": "29.99", "total": "149.95"},
            {"date": "2026-03-02", "product": "Widget B", "quantity": 3, "price": "49.99", "total": "149.97"},
            {"date": "2026-03-03", "product": "Widget A", "quantity": 2, "price": "29.99", "total": "59.98"},
            {"date": "2026-03-04", "product": "Widget C", "quantity": 1, "price": "99.99", "total": "99.99"},
        ],
        "customers": [
            {"name": "John Smith", "email": "john@example.com", "orders": 5, "revenue": "450.00"},
            {"name": "Jane Doe", "email": "jane@example.com", "orders": 3, "revenue": "275.50"},
            {"name": "Bob Johnson", "email": "bob@example.com", "orders": 8, "revenue": "890.25"},
        ],
        "inventory": [
            {"sku": "WID-001", "name": "Widget A", "stock": 45, "cost": "15.00", "price": "29.99"},
            {"sku": "WID-002", "name": "Widget B", "stock": 23, "cost": "25.00", "price": "49.99"},
            {"sku": "WID-003", "name": "Widget C", "stock": 12, "cost": "50.00", "price": "99.99"},
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

Type Detection:
  The generator automatically detects numeric, currency, date, and text columns.
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
                print(f"   Columns: {', '.join(result.get('columns', [])[:5])}")
                if len(result.get('columns', [])) > 5:
                    print(f"   ... and {len(result['columns']) - 5} more columns")
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
