# Password Generator

> Generate cryptographically secure passwords and memorable passphrases

---

## What It Does

Password Generator creates strong, random passwords and memorable passphrases. Uses Python's `secrets` module for cryptographic security — suitable for high-security applications. Check existing password strength with detailed feedback.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install password-generator
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Generate a secure password instantly:

```bash
python main.py password
```

---

## Commands

### `password`

**What it does:** Generate a cryptographically secure random password.

**Usage:**
```bash
python main.py password [length]
```

**Arguments:**

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `length` | ❌ No | Password length (4-128) | `16` |

**Example:**
```bash
python main.py password
python main.py password 32
python main.py password 24
```

**Output:**
```
Generated password: Xk9#mP2$vL8@nQ4!
Strength: Very Strong 💪
Entropy: 95.6 bits
```

---

### `passphrase`

**What it does:** Generate a memorable XKCD-style passphrase.

**Usage:**
```bash
python main.py passphrase [word-count]
```

**Arguments:**

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `word-count` | ❌ No | Number of words (2-20) | `4` |

**Example:**
```bash
python main.py passphrase
python main.py passphrase 6
```

**Output:**
```
Generated passphrase: hotel-fig-jade-42
```

---

### `check`

**What it does:** Analyze password strength and provide improvement suggestions.

**Usage:**
```bash
python main.py check [password]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `password` | ✅ Yes | Password to check | `MyPassword123!` |

**Example:**
```bash
python main.py check "MyPassword123!"
python main.py check "Tr0ub4dor&3"
```

**Output:**
```
Password: Tr0ub4dor&3
Length: 12
Strength: Strong ✅
Score: 7/9
Entropy: 71.4 bits

Suggestions:
  - Consider using a longer password (16+ characters)
```

---

## Use Cases

- **New accounts:** Generate strong passwords for online accounts
- **Password updates:** Create new passwords when rotating accounts
- **Password manager:** Fill your password manager with secure passwords
- **Passphrases:** Create memorable passwords for less critical accounts
- **Security auditing:** Check if existing passwords meet strength requirements

---

## Tips & Tricks

- Use 16+ character passwords for important accounts
- Passphrases are easier to remember AND more secure
- Use `check` to verify passwords meet your organization's requirements
- Store generated passwords in a password manager

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "At least one character type required" | Enable at least one character type |
| Password too short/long | Use length between 4 and 128 characters |
| Passphrase not random enough | Increase word count |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- No external dependencies (uses built-in `secrets` and `string` modules)

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/password-generator)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
