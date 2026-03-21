# Password Generator

A security utility skill for OpenClaw. Generate strong passwords and passphrases.

## Features

- **Random Passwords**: Generate cryptographically secure passwords
- **Memorable Passphrases**: XKCD-style word-based passphrases
- **Strength Checking**: Analyze password security
- **Entropy Calculation**: Estimate password complexity in bits

## Usage

### Generate Password
```bash
# Default 16-character password
python main.py password

# Custom length
python main.py password 20
```

Generates passwords with:
- Uppercase letters
- Lowercase letters
- Digits
- Special characters

### Generate Passphrase
```bash
# Default 4 words + number
python main.py passphrase

# Custom word count
python main.py passphrase 6
```

Example output: `hotel-fig-jade-42`

### Check Password Strength
```bash
python main.py check "MyPassword123!"
```

Shows:
- Strength rating (Weak/Moderate/Strong/Very Strong)
- Entropy in bits
- Character variety analysis
- Improvement suggestions

## Input Validation Limits

| Parameter | Limit |
|-----------|-------|
| Password length | 4-128 characters |
| Passphrase words | 2-20 words |
| Character types | At least one must be enabled |

## Security Considerations

- **Cryptographically Secure**: Uses Python's `secrets` module (not random)
- **Memory Safe**: Doesn't store generated passwords
- **No Logging**: Passwords are not written to logs
- **Character Variety**: Ensures at least one character from each enabled type
- **SystemRandom**: Uses OS-level entropy source

## Error Handling

Errors are categorized:
- **ValueError**: Invalid length or missing character types
- **RuntimeError**: System entropy unavailable

## Known Limitations

- Word list is fixed (100 common words)
- Strength estimation is algorithmic (not real-world crack time)
- No dictionary checking for common passwords
- Maximum password length of 128 characters

## Examples

```bash
# Generate strong password
python main.py password 32

# Create memorable passphrase
python main.py passphrase 5

# Check existing password
python main.py check "Tr0ub4dor&"
```
