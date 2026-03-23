# Password Generator — How-To Guide

**Prerequisites:** Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Generate a Secure Random Password](#1-how-to-generate-a-secure-random-password)
2. [How to Generate a Memorable Passphrase](#2-how-to-generate-a-memorable-passphrase)
3. [How to Check an Existing Password's Strength](#3-how-to-check-an-existing-passwords-strength)
4. [How to Generate Passwords for Different Situations](#4-how-to-generate-passwords-for-different-situations)
5. [Automating with Cron](#5-automating-with-cron)
6. [Combining with Other Skills](#6-combining-with-other-skills)
7. [Troubleshooting Common Issues](#7-troubleshooting-common-issues)
8. [Tips & Best Practices](#8-tips--best-practices)

---

## 1. How to Generate a Secure Random Password

**What this does:** Creates a random password using Python's cryptographically secure `secrets` module. Guarantees at least one uppercase letter, one lowercase letter, one digit, and one special character.

**When to use it:** Creating a new account, changing an old weak password, or generating an API key or token.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/password-generator
```

**Step 2 — Generate a password at the default length (16 characters).**

```bash
python3 main.py password
```

Output:
```
Generated password: K7#mX2@pQ9vR!nLw
Strength: Strong ✅
Entropy: 104.8 bits
```

**Step 3 — Generate a longer password if needed.**

For high-security accounts (banking, email, password manager master password), use a longer length:

```bash
python3 main.py password 24
```

Output:
```
Generated password: Xr9@mKp2#vQ7!nLwB4$tYc8&
Strength: Very Strong 💪
Entropy: 157.2 bits
```

**Step 4 — Copy and store it.**

Copy the password to your password manager (1Password, Bitwarden, KeePass, etc.) immediately. The skill doesn't save it anywhere.

**Result:** A cryptographically secure random password — the same quality as what dedicated password managers generate.

---

## 2. How to Generate a Memorable Passphrase

**What this does:** Creates a sequence of random common words (XKCD style) with a random number appended. Easier to remember and type than a random character string.

**When to use it:** Computer login passwords, passwords you need to type by hand, WiFi passwords you'll read aloud to guests.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/password-generator
```

**Step 2 — Generate a 4-word passphrase (default).**

```bash
python3 main.py passphrase
```

Output:
```
Generated passphrase: sunset-falcon-azure-mountain-47
```

**Step 3 — Generate a longer passphrase for higher security.**

```bash
python3 main.py passphrase 6
```

Output:
```
Generated passphrase: ocean-castle-blue-swift-jungle-crystal-83
```

**Step 4 — Use it.**

`sunset-falcon-azure-mountain-47` is 30 characters — longer and more memorable than most random passwords. Type it in, add it to your password manager with the site name.

**Result:** A passphrase that's both secure and human-friendly.

---

## 3. How to Check an Existing Password's Strength

**What this does:** Analyzes a password and returns a score (0–9), entropy in bits, strength rating, and specific suggestions for improvement.

**When to use it:** Auditing existing passwords you haven't changed in a while, or checking a password you created manually before using it.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/password-generator
```

**Step 2 — Run the check command.**

Always wrap the password in quotes, especially if it contains special characters.

```bash
python3 main.py check "MyPassword123!"
```

Output:
```
Password: MyPassword123!
Length: 14
Strength: Strong ✅
Score: 7/9
Entropy: 91.8 bits
```

**Step 3 — Check a weak password.**

```bash
python3 main.py check "password"
```

Output:
```
Password: password
Length: 8
Strength: Weak ❌
Score: 2/9
Entropy: 37.6 bits

Suggestions:
  - Password is too short (minimum 8 characters)
  - Add uppercase letters
  - Add digits
  - Add special characters
```

**Step 4 — Follow the suggestions to improve it.**

Each suggestion tells you exactly what's missing. A "Very Strong" password needs all four character types and should be at least 16 characters.

**Result:** You know exactly how strong your password is and what to change to make it stronger.

---

## 4. How to Generate Passwords for Different Situations

**What this does:** Different password contexts call for different types. Here's the right approach for each.

### High-security accounts (banking, email, password manager)

Use a long random password — 20+ characters:

```bash
python3 main.py password 24
```

```
Generated password: Xr9@mKp2#vQ7!nLwB4$tYc8&
Strength: Very Strong 💪
Entropy: 157.2 bits
```

### Computer login (typed regularly)

Use a passphrase — easier to type, equally secure:

```bash
python3 main.py passphrase 5
```

```
Generated passphrase: swift-harbor-crimson-falcon-blue-62
```

### WiFi password (guests will type it)

Use a 5-word passphrase — easy to read aloud:

```bash
python3 main.py passphrase 5
```

### API keys and tokens (never typed by hand)

Use a maximum-length random password — 32 characters:

```bash
python3 main.py password 32
```

---

## 5. Automating with Cron

You can automate periodic password generation reminders or batch generation for system accounts.

### Example: Generate and log a new service account password monthly

```bash
0 9 1 * * python3 /home/yourname/smfworks-skills/skills/password-generator/main.py password 24 >> /home/yourname/logs/password-generator.log 2>&1
```

**Note:** Logging passwords to files is only appropriate for service accounts that you immediately configure and rotate. Never store personal passwords in plain-text log files.

### Example: Weekly strength reminder

Add a reminder to audit your passwords once a week by using a cron job that prints a reminder:

```bash
0 9 * * 1 echo "Reminder: Check your passwords at $(date)" >> /home/yourname/logs/security-reminders.log
```

---

## 6. Combining with Other Skills

**Password Generator + QR Generator:** Generate a passphrase for WiFi, then create a QR code for guests:

```bash
# Generate the passphrase
python3 ~/smfworks-skills/skills/password-generator/main.py passphrase 4
# Output: sunset-falcon-azure-mountain-47

# Create the WiFi QR code using that passphrase
python3 ~/smfworks-skills/skills/qr-generator/main.py wifi 'MyNetwork' 'sunset-falcon-azure-mountain-47' ~/Desktop/wifi-qr.png
```

---

## 7. Troubleshooting Common Issues

### `Error: check requires password`

You ran `check` without a password argument.  
**Fix:** `python3 main.py check "your-password-here"`

---

### The generated password was rejected by a website

Some websites have odd character restrictions (no `!`, no `@`, etc.).  
**Fix:** Just run `password` again — each run generates a completely different password.

---

### I can't remember which password I generated

The skill doesn't store anything.  
**Fix:** Always copy passwords directly into your password manager immediately after generating them. Never rely on scrollback in your terminal.

---

### `Unknown command: generate`

You used the wrong command name.  
**Fix:** The correct commands are `password`, `passphrase`, and `check`.

---

## 8. Tips & Best Practices

**Never use `password` or `passphrase` for sensitive data in shell scripts that log to files.** Passwords in log files are a security risk. Only use this skill interactively and copy the result directly to your password manager.

**Use `check` to audit your important passwords now.** Run `check` on your banking, email, and password manager master passwords. If any score below 6, change them.

**Passphrases are underrated.** A 5-word passphrase like `swift-harbor-crimson-falcon-blue-62` is 35 characters long — stronger than most random 16-character passwords, and you can actually type it.

**Generate longer passwords when it doesn't matter if you remember them.** If you're storing a password in a manager anyway, use 24–32 characters. Length is free.

**The skill uses `secrets`, not `random`.** Python's `random` module is not suitable for security use — it's predictable. This skill uses `secrets.choice()` and `secrets.SystemRandom()` which are designed for cryptographic applications.

**Double-check the password before closing your terminal.** The skill doesn't save anything. If you close the window before copying, the password is gone.
