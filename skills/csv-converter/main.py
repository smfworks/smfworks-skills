#!/usr/bin/env python3
"""
CSV Converter Skill for OpenClaw
Convert between CSV, JSON, and Excel formats.
"""

import csv
import json
import sys
from pathlib import Path
from typing import Dict, List


def csv_to_json(input_file: str, output_file: str) -> Dict:
    """
    Convert CSV to JSON.
    
    Args:
        input_file: Input CSV file path
        output_file: Output JSON file path
    
    Returns:
        Dict with operation results
    """
    try:
        data = []
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(dict(row))
        
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "rows": len(data),
            "output": output_file
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def json_to_csv(input_file: str, output_file: str) -> Dict:
    """
    Convert JSON to CSV.
    
    Args:
        input_file: Input JSON file path
        output_file: Output CSV file path
    
    Returns:
        Dict with operation results
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both single object and array
        if isinstance(data, dict):
            data = [data]
        
        if not data:
            return {"success": False, "error": "No data found in JSON"}
        
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        return {
            "success": True,
            "rows": len(data),
            "columns": len(data[0].keys()),
            "output": output_file
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def csv_to_excel(input_file: str, output_file: str) -> Dict:
    """
    Convert CSV to Excel.
    
    Args:
        input_file: Input CSV file path
        output_file: Output Excel file path
    
    Returns:
        Dict with operation results
    """
    try:
        import pandas as pd
        
        df = pd.read_csv(input_file)
        
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        df.to_excel(output_file, index=False)
        
        return {
            "success": True,
            "rows": len(df),
            "columns": len(df.columns),
            "output": output_file
        }
    except ImportError:
        return {"success": False, "error": "pandas not installed. Run: pip install pandas openpyxl"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def excel_to_csv(input_file: str, output_file: str, sheet_name: str = None) -> Dict:
    """
    Convert Excel to CSV.
    
    Args:
        input_file: Input Excel file path
        output_file: Output CSV file path
        sheet_name: Specific sheet to convert (optional)
    
    Returns:
        Dict with operation results
    """
    try:
        import pandas as pd
        
        if sheet_name:
            df = pd.read_excel(input_file, sheet_name=sheet_name)
        else:
            df = pd.read_excel(input_file)
        
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_file, index=False)
        
        return {
            "success": True,
            "rows": len(df),
            "columns": len(df.columns),
            "output": output_file
        }
    except ImportError:
        return {"success": False, "error": "pandas not installed. Run: pip install pandas openpyxl"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def preview_csv(input_file: str, rows: int = 5) -> Dict:
    """
    Preview CSV file contents.
    
    Args:
        input_file: Input CSV file path
        rows: Number of rows to preview
    
    Returns:
        Dict with preview data
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            
            data = []
            for i, row in enumerate(reader):
                if i >= rows:
                    break
                data.append(row)
        
        return {
            "success": True,
            "headers": headers,
            "preview": data,
            "total_rows": sum(1 for _ in csv.reader(open(input_file))) - 1
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    """CLI interface for CSV converter."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [options]")
        print("Commands:")
        print("  csv-to-json <input.csv> <output.json>")
        print("  json-to-csv <input.json> <output.csv>")
        print("  csv-to-excel <input.csv> <output.xlsx>")
        print("  excel-to-csv <input.xlsx> <output.csv>")
        print("  preview <input.csv> [rows]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "csv-to-json":
        if len(sys.argv) < 4:
            print("Error: Requires input and output files")
            sys.exit(1)
        result = csv_to_json(sys.argv[2], sys.argv[3])
    elif command == "json-to-csv":
        if len(sys.argv) < 4:
            print("Error: Requires input and output files")
            sys.exit(1)
        result = json_to_csv(sys.argv[2], sys.argv[3])
    elif command == "csv-to-excel":
        if len(sys.argv) < 4:
            print("Error: Requires input and output files")
            sys.exit(1)
        result = csv_to_excel(sys.argv[2], sys.argv[3])
    elif command == "excel-to-csv":
        if len(sys.argv) < 4:
            print("Error: Requires input and output files")
            sys.exit(1)
        result = excel_to_csv(sys.argv[2], sys.argv[3])
    elif command == "preview":
        if len(sys.argv) < 3:
            print("Error: Requires input file")
            sys.exit(1)
        rows = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        result = preview_csv(sys.argv[2], rows)
        
        if result["success"]:
            print("Headers:", result["headers"])
            print("Preview:")
            for row in result["preview"]:
                print("  ", row)
            print(f"Total rows: {result['total_rows']}")
            return
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
    
    if result["success"]:
        print(f"✅ Success: {result}")
    else:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
