# Password Generator

> Generate cryptographically secure passwords and memorable passphrases, and check the strength of existing passwords.

**Tier:** Free — no subscription required  
**Version:** 1.0  
**Category:** Security / Productivity

---

## What It Does

Password Generator is an OpenClaw skill that creates strong, random passwords and passphrases using Python's `secrets` module — the cryptographically secure random generator. You can generate a random password at any length, create a memorable multi-word passphrase (XKCD style), or analyze an existing password's strength with a score, entropy calculation, and specific improvement suggestions.

**What it does NOT do:** It does not store passwords, integrate with password managers, auto-fill forms, or generate passwords with custom character sets beyond enabling/disabling the four built-in character classes.

---

## Prerequisites

- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed**
- [ ] **No subscription required** — free tier skill
- [ ] **No external packages** — uses Python stdlib only

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/password-generator
python3 main.py
```

Expected output:
```
Usage: python main.py <command> [options]
Commands:
  password [length]                  - Generate random password
  passphrase [word_count]            - Generate passphrase
  check <password>                  - Check password strength
```

---

## Quick Start

Generate a 16-character secure password:

```bash
python3 main.py password
```

Output:
```
Generated password: K7#mX2@pQ9vR!nLw
Strength: Strong ✅
Entropy: 104.8 bits
```

---

## Command Reference

### `password`

Generates a random password using Python's `secrets` module (cryptographically secure). The default length is 16 characters and includes uppercase, lowercase, digits, and special characters. At least one character from each enabled class is guaranteed.

**Usage:**
```bash
python3 main.py password [length]
```

**Arguments:**

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `length` | ❌ No | Password length in characters | `16` |

**Examples:**

```bash
python3 main.py password
```
```
Generated password: K7#mX2@pQ9vR!nLw
Strength: Strong ✅
Entropy: 104.8 bits
```

```bash
python3 main.py password 24
```
```
Generated password: Xr9@mKp2#vQ7!nLwB4$tYc8&
Strength: Very Strong 💪
Entropy: 157.2 bits
```

---

### `passphrase`

Generates a passphrase from a list of common English words, separated by `-`. A random 2-digit number is appended for extra entropy. Passphrases are easier to remember than random character strings while still being secure.

**Usage:**
```bash
python3 main.py passphrase [word_count]
```

**Arguments:**

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `word_count` | ❌ No | Number of words in the passphrase | `4` |

**Examples:**

```bash
python3 main.py passphrase
```
```
Generated passphrase: sunset-falcon-azure-mountain-47
```

```bash
python3 main.py passphrase 6
```
```
Generated passphrase: ocean-castle-blue-swift-jungle-crystal-83
```

---

### `check`

Analyzes the strength of a password you provide. Reports length, character variety, score out of 9, entropy in bits, a strength rating, and specific improvement suggestions.

**Usage:**
```bash
python3 main.py check <password>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `password` | ✅ Yes | Password to analyze (wrap in quotes) | `"MyP@ss123"` |

**Strength levels:**

| Rating | Score | Entropy | Meaning |
|--------|-------|---------|---------|
| Very Strong 💪 | 8–9/9 | 80+ bits | Excellent — use it |
| Strong ✅ | 6–7/9 | 60–79 bits | Good — acceptable |
| Moderate ⚠️ | 4–5/9 | 40–59 bits | Needs improvement |
| Weak ❌ | 0–3/9 | < 40 bits | Change this password |

**Example — weak password:**
```bash
python3 main.py check "password123"
```
```
Password: password123
Length: 11
Strength: Moderate ⚠️
Score: 4/9
Entropy: 58.2 bits

Suggestions:
  - Add uppercase letters
  - Add special characters
```

**Example — strong password:**
```bash
python3 main.py check "K7#mX2@pQ9vR!nLw"
```
```
Password: K7#mX2@pQ9vR!nLw
Length: 16
Strength: Very Strong 💪
Score: 9/9
Entropy: 104.8 bits
```

---

## Use Cases

### 1. Generate a new account password

```bash
python3 main.py password 20
```

Copy the output and paste it into your password manager.

---

### 2. Generate a WiFi password that's easy to share aloud

```bash
python3 main.py passphrase 4
```

`sunset-falcon-azure-mountain-47` is much easier to read aloud or type than `K7#mX2@pQ9vR!nLw`.

---

### 3. Audit an existing password

```bash
python3 main.py check "MyOldPassword!"
```

Get a score and specific tips for what's weak.

---

### 4. Generate a batch of passwords for a list of accounts

```bash
for i in {1..10}; do python3 main.py password 16 | head -1; done
```

---

### 5. Generate a long, highly secure master password

```bash
python3 main.py password 32
```

---

## Configuration

No configuration file or environment variables needed. All behavior is set by command arguments.

**Built-in character sets:**

| Class | Characters |
|-------|------------|
| Uppercase | A–Z |
| Lowercase | a–z |
| Digits | 0–9 |
| Special | !@#$%^&*()_+-=[]{}|;:,.<>? |

---

## Troubleshooting

### `At least one character type must be enabled`
If you edit the code to disable all character classes, this error appears.  
**Fix:** At least one character class must be enabled.

### `Error: check requires password`
You ran `check` without providing a password.  
**Fix:** `python3 main.py check "yourpassword"`

### `Unknown command: xxx`
Typo in command name.  
**Fix:** Valid commands are `password`, `passphrase`, and `check`.

### Password contains characters my system doesn't accept

Some systems reject certain special characters (e.g., shell special chars or fields that reject quotes).  
**Fix:** Use the `passphrase` command for passwords that need to be typed by hand, or regenerate until you get one your target system accepts.

---

## FAQ

**Q: Is this cryptographically secure?**  
A: Yes. The skill uses Python's `secrets` module which is designed for cryptographic use. It is not suitable to use `random` for security-sensitive applications; `secrets` is.

**Q: What's entropy and why does it matter?**  
A: Entropy (in bits) measures how hard a password is to guess. 80+ bits is generally considered very secure against brute-force attacks. Each bit added doubles the guessing work.

**Q: What's the difference between `password` and `passphrase`?**  
A: `password` generates a random character string — very secure but hard to remember. `passphrase` generates a sequence of common words — slightly lower entropy but much easier to remember and type.

**Q: Should I use a passphrase or a password?**  
A: For passwords you type regularly (e.g., computer login), passphrases are better — they're equally secure and far easier to type. For passwords stored in a manager, use `password` with the highest length you can.

**Q: Does this skill store my passwords anywhere?**  
A: No. Passwords are generated in memory and printed to stdout. Nothing is written to disk.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| OpenClaw | Any version |
| Operating System | Linux, macOS |
| Subscription Tier | Free |
| External APIs | None |
| External Packages | None (stdlib only) |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/password-generator)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
