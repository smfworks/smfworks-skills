#!/usr/bin/env python3
"""
Markdown Converter Skill for OpenClaw
Convert Markdown to HTML and other formats.
"""

import sys
from pathlib import Path
from typing import Dict


def markdown_to_html(input_file: str, output_file: str = None) -> Dict:
    """
    Convert Markdown file to HTML.
    
    Args:
        input_file: Input Markdown file path
        output_file: Output HTML file path (optional)
    
    Returns:
        Dict with operation results
    """
    try:
        import markdown
        
        # Read markdown
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert to HTML
        html_content = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'toc']
        )
        
        # Wrap in basic HTML template
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{Path(input_file).stem}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.6; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 16px; overflow-x: auto; border-radius: 6px; }}
        blockquote {{ border-left: 4px solid #ddd; margin: 0; padding-left: 16px; color: #666; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #f4f4f4; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        
        # Determine output file
        if output_file is None:
            output_file = str(Path(input_file).with_suffix('.html'))
        
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return {
            "success": True,
            "input": input_file,
            "output": output_file,
            "characters": len(md_content)
        }
        
    except ImportError:
        return {"success": False, "error": "markdown not installed. Run: pip install markdown"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def markdown_to_text(input_file: str, output_file: str = None) -> Dict:
    """
    Convert Markdown to plain text (strip formatting).
    
    Args:
        input_file: Input Markdown file path
        output_file: Output text file path (optional)
    
    Returns:
        Dict with operation results
    """
    try:
        import re
        
        # Read markdown
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove markdown syntax
        text = content
        text = re.sub(r'#+\s*', '', text)  # Headers
        text = re.sub(r'\*\*|__', '', text)  # Bold
        text = re.sub(r'\*|_', '', text)  # Italic
        text = re.sub(r'`', '', text)  # Code
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # Links
        text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'[Image: \1]', text)  # Images
        text = re.sub(r'\n{3,}', '\n\n', text)  # Extra newlines
        
        # Determine output file
        if output_file is None:
            output_file = str(Path(input_file).with_suffix('.txt'))
        
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        return {
            "success": True,
            "input": input_file,
            "output": output_file,
            "characters": len(text)
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def extract_toc(input_file: str) -> Dict:
    """
    Extract table of contents from Markdown.
    
    Args:
        input_file: Input Markdown file path
    
    Returns:
        Dict with TOC
    """
    try:
        import re
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find headers
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        
        toc = []
        for level, title in headers:
            depth = len(level)
            anchor = re.sub(r'[^\w\s-]', '', title.lower()).replace(' ', '-')
            toc.append({
                "depth": depth,
                "title": title.strip(),
                "anchor": anchor
            })
        
        return {
            "success": True,
            "headings": len(toc),
            "toc": toc
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def count_markdown_stats(input_file: str) -> Dict:
    """
    Count words, lines, and other stats in Markdown file.
    
    Args:
        input_file: Input Markdown file path
    
    Returns:
        Dict with stats
    """
    try:
        import re
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count various elements
        words = len(re.findall(r'\b\w+\b', content))
        lines = content.count('\n') + 1
        
        headers = len(re.findall(r'^#{1,6}\s+', content, re.MULTILINE))
        code_blocks = len(re.findall(r'```', content)) // 2
        links = len(re.findall(r'\[([^\]]+)\]\([^\)]+\)', content))
        images = len(re.findall(r'!\[([^\]]*)\]\([^\)]+\)', content))
        
        return {
            "success": True,
            "words": words,
            "characters": len(content),
            "lines": lines,
            "headers": headers,
            "code_blocks": code_blocks,
            "links": links,
            "images": images
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    """CLI interface for markdown converter."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [options]")
        print("Commands:")
        print("  to-html <input.md> [output.html]    - Convert to HTML")
        print("  to-text <input.md> [output.txt]     - Convert to plain text")
        print("  toc <input.md>                       - Extract table of contents")
        print("  stats <input.md>                     - Count stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "to-html":
        if len(sys.argv) < 3:
            print("Error: to-html requires input file")
            sys.exit(1)
        output = sys.argv[3] if len(sys.argv) > 3 else None
        result = markdown_to_html(sys.argv[2], output)
    elif command == "to-text":
        if len(sys.argv) < 3:
            print("Error: to-text requires input file")
            sys.exit(1)
        output = sys.argv[3] if len(sys.argv) > 3 else None
        result = markdown_to_text(sys.argv[2], output)
    elif command == "toc":
        if len(sys.argv) < 3:
            print("Error: toc requires input file")
            sys.exit(1)
        result = extract_toc(sys.argv[2])
        if result["success"]:
            print("Table of Contents:")
            for item in result["toc"]:
                indent = "  " * (item["depth"] - 1)
                print(f"{indent}- {item['title']}")
            return
    elif command == "stats":
        if len(sys.argv) < 3:
            print("Error: stats requires input file")
            sys.exit(1)
        result = count_markdown_stats(sys.argv[2])
        if result["success"]:
            print(f"Words: {result['words']}")
            print(f"Lines: {result['lines']}")
            print(f"Headers: {result['headers']}")
            print(f"Code blocks: {result['code_blocks']}")
            print(f"Links: {result['links']}")
            print(f"Images: {result['images']}")
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
