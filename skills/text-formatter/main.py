#!/usr/bin/env python3
"""
Text Formatter Skill for OpenClaw
Format, clean, and transform text.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


def convert_case(text: str, case_type: str) -> str:
    """Convert text case."""
    if case_type == "upper":
        return text.upper()
    elif case_type == "lower":
        return text.lower()
    elif case_type == "title":
        return text.title()
    elif case_type == "sentence":
        sentences = re.split(r'([.!?]+\s+)', text)
        result = ""
        for i, sentence in enumerate(sentences):
            if i % 2 == 0:
                result += sentence.capitalize()
            else:
                result += sentence
        return result
    elif case_type == "camel":
        words = re.findall(r'[A-Za-z0-9]+', text)
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    elif case_type == "snake":
        words = re.findall(r'[A-Za-z0-9]+', text)
        return '_'.join(word.lower() for word in words)
    elif case_type == "kebab":
        words = re.findall(r'[A-Za-z0-9]+', text)
        return '-'.join(word.lower() for word in words)
    else:
        return text


def clean_whitespace(text: str, aggressive: bool = False) -> str:
    """Clean up whitespace in text."""
    if aggressive:
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
    else:
        lines = text.split('\n')
        cleaned_lines = []
        prev_empty = False
        
        for line in lines:
            stripped = line.strip()
            if stripped == '':
                if not prev_empty:
                    cleaned_lines.append('')
                    prev_empty = True
            else:
                cleaned_lines.append(stripped)
                prev_empty = False
        
        text = '\n'.join(cleaned_lines)
    
    return text


def word_count(text: str) -> Dict:
    """Count words, characters, lines in text."""
    words = len(text.split())
    characters = len(text)
    characters_no_spaces = len(text.replace(' ', '').replace('\n', ''))
    lines = text.count('\n') + 1 if text else 0
    sentences = len(re.findall(r'[.!?]+', text))
    
    reading_time_minutes = words / 200
    
    return {
        "words": words,
        "characters": characters,
        "characters_no_spaces": characters_no_spaces,
        "lines": lines,
        "sentences": sentences,
        "reading_time_seconds": int(reading_time_minutes * 60),
        "reading_time_formatted": f"{int(reading_time_minutes)} min {int((reading_time_minutes % 1) * 60)} sec"
    }


def main():
    """CLI interface for text formatter."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [options]")
        print("Commands: case, clean, count")
        sys.exit(1)
    
    command = sys.argv[1]
    
    def get_input_text(arg_index: int) -> str:
        if arg_index >= len(sys.argv):
            return sys.stdin.read()
        
        input_arg = sys.argv[arg_index]
        if Path(input_arg).exists():
            with open(input_arg, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return input_arg
    
    if command == "case":
        if len(sys.argv) < 3:
            print("Error: case requires case_type (upper, lower, title, camel)")
            sys.exit(1)
        
        case_type = sys.argv[2].lower()
        text = get_input_text(3) if len(sys.argv) > 3 else sys.stdin.read()
        print(convert_case(text, case_type))
    
    elif command == "clean":
        text = get_input_text(2) if len(sys.argv) > 2 else sys.stdin.read()
        result = clean_whitespace(text)
        print(result)
    
    elif command == "count":
        text = get_input_text(2) if len(sys.argv) > 2 else sys.stdin.read()
        result = word_count(text)
        print(f"Words: {result['words']}")
        print(f"Characters: {result['characters']}")
        print(f"Reading time: {result['reading_time_formatted']}")


if __name__ == "__main__":
    main()
