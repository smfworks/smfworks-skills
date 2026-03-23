# Password Generator — Quick Reference

## Install
```bash
smfw install password-generator
```

## Commands
```bash
python main.py password                        # Generate 16-char password
python main.py password 32                     # Generate 32-char password
python main.py passphrase                       # Generate 4-word passphrase
python main.py passphrase 6                    # Generate 6-word passphrase
python main.py check "MyPassword123!"          # Check password strength
```

## Common Examples
```bash
# Generate a strong password
python main.py password

# Generate a longer password
python main.py password 24

# Generate a memorable passphrase
python main.py passphrase

# Generate a longer passphrase
python main.py passphrase 5

# Check password strength
python main.py check "Tr0ub4dor&3"
```

## Help
```bash
python main.py --help
python main.py password --help
```
