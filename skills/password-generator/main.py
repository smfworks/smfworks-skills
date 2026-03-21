#!/usr/bin/env python3
"""
Password Generator Skill for OpenClaw
Generate strong passwords, passphrases, and check password strength.
"""

import secrets
import string
import sys
import math
from pathlib import Path
from typing import Dict


def generate_password(length: int = 16, use_uppercase: bool = True, 
                       use_lowercase: bool = True, use_digits: bool = True, 
                       use_special: bool = True) -> str:
    """
    Generate a strong random password.
    
    Args:
        length: Password length
        use_uppercase: Include uppercase letters
        use_lowercase: Include lowercase letters
        use_digits: Include digits
        use_special: Include special characters
    
    Returns:
        Generated password
    """
    alphabet = ""
    if use_lowercase:
        alphabet += string.ascii_lowercase
    if use_uppercase:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_special:
        alphabet += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not alphabet:
        raise ValueError("At least one character type must be enabled")
    
    # Ensure at least one of each type
    password = []
    if use_lowercase:
        password.append(secrets.choice(string.ascii_lowercase))
    if use_uppercase:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        password.append(secrets.choice(string.digits))
    if use_special:
        password.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
    
    # Fill remaining length
    for _ in range(length - len(password)):
        password.append(secrets.choice(alphabet))
    
    # Shuffle
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)


def generate_passphrase(word_count: int = 4, separator: str = "-") -> str:
    """
    Generate a memorable passphrase (XKCD style).
    
    Args:
        word_count: Number of words
        separator: Word separator
    
    Returns:
        Generated passphrase
    """
    # Common English words
    words = [
        "alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
        "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa",
        "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey", "xray",
        "yankee", "zulu", "apple", "banana", "cherry", "date", "elderberry", "fig",
        "grape", "honeydew", "kiwi", "lemon", "mango", "orange", "papaya", "quince",
        "raspberry", "strawberry", "tangerine", "ugli", "vanilla", "watermelon",
        "azure", "blue", "crimson", "dark", "emerald", "fuchsia", "green", "honey",
        "ivory", "jade", "khaki", "lime", "magenta", "navy", "olive", "pink",
        "quick", "rapid", "swift", "turbo", "ultra", "vivid", "wild", "xenon",
        "yellow", "zeal", "anchor", "bridge", "castle", "dragon", "eagle", "falcon",
        "garden", "harbor", "island", "jungle", "knight", "lagoon", "mountain",
        "nebula", "ocean", "palace", "quest", "river", "sunset", "temple", "unicorn",
        "valley", "waterfall", "zenith"
    ]
    
    passphrase_words = [secrets.choice(words) for _ in range(word_count)]
    
    # Add random number for extra security
    passphrase_words.append(str(secrets.randbelow(100)))
    
    return separator.join(passphrase_words)


def check_password_strength(password: str) -> Dict:
    """
    Check password strength.
    
    Args:
        password: Password to check
    
    Returns:
        Dict with strength analysis
    """
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 16:
        score += 3
    elif len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password is too short (minimum 8 characters)")
    
    # Character variety
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    if has_lower:
        score += 1
    else:
        feedback.append("Add lowercase letters")
    
    if has_upper:
        score += 1
    else:
        feedback.append("Add uppercase letters")
    
    if has_digit:
        score += 1
    else:
        feedback.append("Add digits")
    
    if has_special:
        score += 2
    else:
        feedback.append("Add special characters")
    
    # Calculate entropy (bits)
    charset_size = 0
    if has_lower:
        charset_size += 26
    if has_upper:
        charset_size += 26
    if has_digit:
        charset_size += 10
    if has_special:
        charset_size += 20
    
    entropy = len(password) * math.log2(charset_size) if charset_size > 0 else 0
    
    # Strength rating
    if score >= 8:
        strength = "very-strong"
        strength_text = "Very Strong 💪"
    elif score >= 6:
        strength = "strong"
        strength_text = "Strong ✅"
    elif score >= 4:
        strength = "moderate"
        strength_text = "Moderate ⚠️"
    else:
        strength = "weak"
        strength_text = "Weak ❌"
    
    return {
        "password": password,
        "length": len(password),
        "score": score,
        "max_score": 9,
        "strength": strength,
        "strength_text": strength_text,
        "entropy": entropy,
        "has_lower": has_lower,
        "has_upper": has_upper,
        "has_digit": has_digit,
        "has_special": has_special,
        "feedback": feedback
    }


def main():
    """CLI interface for password generator."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [options]")
        print("Commands:")
        print("  password [length]                  - Generate random password")
        print("  passphrase [word_count]            - Generate passphrase")
        print("  check <password>                  - Check password strength")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "password":
        length = int(sys.argv[2]) if len(sys.argv) > 2 else 16
        password = generate_password(length)
        print(f"Generated password: {password}")
        
        # Also show strength
        strength = check_password_strength(password)
        print(f"Strength: {strength['strength_text']}")
        print(f"Entropy: {strength['entropy']} bits")
    
    elif command == "passphrase":
        word_count = int(sys.argv[2]) if len(sys.argv) > 2 else 4
        passphrase = generate_passphrase(word_count)
        print(f"Generated passphrase: {passphrase}")
    
    elif command == "check":
        if len(sys.argv) < 3:
            print("Error: check requires password")
            sys.exit(1)
        
        password = sys.argv[2]
        result = check_password_strength(password)
        
        print(f"Password: {result['password']}")
        print(f"Length: {result['length']}")
        print(f"Strength: {result['strength_text']}")
        print(f"Score: {result['score']}/{result['max_score']}")
        print(f"Entropy: {result['entropy']} bits")
        
        if result['feedback']:
            print("\nSuggestions:")
            for suggestion in result['feedback']:
                print(f"  - {suggestion}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
