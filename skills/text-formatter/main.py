#!/usr/bin/env python3
"""
Text Formatter Skill for OpenClaw
Format, clean, and transform text.

Examples:
    python main.py case upper "hello world"
    python main.py case camel "hello world" 
    python main.py clean --aggressive < input.txt
    python main.py count < document.txt
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# Module-level constants
MAX_INPUT_SIZE = 10 * 1024 * 1024  # 10MB max input
MAX_OUTPUT_SIZE = 50 * 1024 * 1024  # 50MB max output
MAX_WORDS = 10_000_000  # Max words to process
VALID_CASES = ["upper", "lower", "title", "sentence", "camel", "snake", "kebab"]
ERROR_PREFIX = "Error:"


def validate_input(text: str, source: str = "input") -> Tuple[bool, str]:
    """
    Validate input text for security and resource limits.
    
    Args:
        text: Text to validate
        source: Source description for error messages
    
    Returns:
        (is_valid, error_message)
    
    Example:
        >>> validate_input("hello", "input")
        (True, "")
        >>> validate_input("a" * 100_000_000, "input")
        (False, "input too large: ...")
    """
    if not isinstance(text, str):
        return False, f"{source} must be a string"
    
    if len(text) > MAX_INPUT_SIZE:
        return False, f"{source} too large: {len(text)} bytes (max: {MAX_INPUT_SIZE})"
    
    # Check for potential encoding issues
    try:
        text.encode('utf-8')
    except UnicodeEncodeError:
        return False, f"{source} contains invalid UTF-8 characters"
    
    return True, ""


def read_input_text(arg_index: int, args: List[str]) -> Tuple[str, Optional[str]]:
    """
    Read input text from file or command argument.
    
    Args:
        arg_index: Index in args to check
        args: Command line arguments
    
    Returns:
        (text, error_message)
    
    Example:
        >>> read_input_text(0, ["hello"])
        ("hello", None)
    """
    if arg_index >= len(args):
        # Read from stdin
        try:
            text = sys.stdin.read()
        except OSError as e:
            return "", f"Error reading from stdin: {e}"
    else:
        input_arg = args[arg_index]
        try:
            input_path = Path(input_arg).resolve()
        except (OSError, ValueError):
            return "", f"Invalid path: {input_arg}"
        
        # Check for path traversal
        if ".." in Path(input_arg).parts:
            return "", "Path traversal detected"
        
        if input_path.exists():
            # Read from file
            try:
                # Check file size before reading
                size = input_path.stat().st_size
                if size == 0:
                    return "", f"File is empty: {input_arg}"
                if size > MAX_INPUT_SIZE:
                    return "", f"File too large: {size} bytes (max: {MAX_INPUT_SIZE})"
                
                with open(input_path, 'r', encoding='utf-8', errors='strict') as f:
                    text = f.read()
            except UnicodeDecodeError:
                return "", f"File is not valid UTF-8 text: {input_arg}"
            except OSError as e:
                return "", f"Error reading file: {e}"
        else:
            # Use as literal text
            text = input_arg
    
    return text, None


def convert_case(text: str, case_type: str) -> str:
    """
    Convert text case.
    
    Args:
        text: Input text
        case_type: One of upper, lower, title, sentence, camel, snake, kebab
    
    Returns:
        Text with converted case
    
    Example:
        >>> convert_case("hello world", "upper")
        'HELLO WORLD'
        >>> convert_case("hello world", "camel")
        'helloWorld'
    """
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
        if not words:
            return text
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
    """
    Clean up whitespace in text.
    
    Args:
        text: Input text
        aggressive: If True, collapses all whitespace to single spaces
    
    Returns:
        Cleaned text
    
    Example:
        >>> clean_whitespace("  hello   world  ")
        'hello   world'
        >>> clean_whitespace("  hello   world  ", aggressive=True)
        'hello world'
    """
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


def word_count(text: str) -> Dict[str, Union[int, str]]:
    """
    Count words, characters, lines in text.
    
    Implements memory-efficient counting with limits.
    
    Args:
        text: Input text to analyze
    
    Returns:
        Dict with word statistics
    
    Example:
        >>> word_count("Hello world")
        {'words': 2, 'characters': 11, ...}
    """
    words = len(text.split())
    
    # Check word count limit
    if words > MAX_WORDS:
        return {
            "error": f"Too many words: {words} (max: {MAX_WORDS})",
            "words": words
        }
    
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
        print("")
        print("Examples:")
        print('  python main.py case upper "hello world"')
        print('  python main.py case camel "hello world"')
        print("  python main.py clean < input.txt")
        print("  python main.py clean --aggressive < messy.txt")
        print("  python main.py count < document.txt")
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "case":
        if len(args) < 1:
            print(f"{ERROR_PREFIX} case requires case_type")
            print(f"Valid types: {', '.join(VALID_CASES)}")
            sys.exit(1)
        
        case_type = args[0].lower()
        if case_type not in VALID_CASES:
            print(f"{ERROR_PREFIX} case_type must be one of: {', '.join(VALID_CASES)}")
            sys.exit(1)
        
        text, error = read_input_text(1, args)
        if error:
            print(f"{ERROR_PREFIX} {error}")
            sys.exit(1)
        
        # Validate input
        is_valid, error = validate_input(text)
        if not is_valid:
            print(f"{ERROR_PREFIX} {error}")
            sys.exit(1)
        
        result = convert_case(text, case_type)
        
        # Validate output size
        if len(result) > MAX_OUTPUT_SIZE:
            print(f"{ERROR_PREFIX} Output too large: {len(result)} bytes")
            sys.exit(1)
        
        print(result)
    
    elif command == "clean":
        text, error = read_input_text(0, args)
        if error:
            print(f"{ERROR_PREFIX} {error}")
            sys.exit(1)
        
        # Validate input
        is_valid, error = validate_input(text)
        if not is_valid:
            print(f"{ERROR_PREFIX} {error}")
            sys.exit(1)
        
        aggressive = "--aggressive" in args
        result = clean_whitespace(text, aggressive)
        
        # Validate output size
        if len(result) > MAX_OUTPUT_SIZE:
            print(f"{ERROR_PREFIX} Output too large: {len(result)} bytes")
            sys.exit(1)
        
        print(result)
    
    elif command == "count":
        text, error = read_input_text(0, args)
        if error:
            print(f"{ERROR_PREFIX} {error}")
            sys.exit(1)
        
        # Validate input
        is_valid, error = validate_input(text)
        if not is_valid:
            print(f"{ERROR_PREFIX} {error}")
            sys.exit(1)
        
        result = word_count(text)
        
        if "error" in result:
            print(f"{ERROR_PREFIX} {result['error']}")
            print(f"Words: {result['words']}")
        else:
            print(f"Words: {result['words']}")
            print(f"Characters: {result['characters']}")
            print(f"Characters (no spaces): {result['characters_no_spaces']}")
            print(f"Lines: {result['lines']}")
            print(f"Sentences: {result['sentences']}")
            print(f"Reading time: {result['reading_time_formatted']}")
    
    else:
        print(f"{ERROR_PREFIX} Unknown command: {command}")
        print("Commands: case, clean, count")
        sys.exit(1)


if __name__ == "__main__":
    main()
