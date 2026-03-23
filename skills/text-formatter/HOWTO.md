# Text Formatter — Quick Reference

## Install
```bash
smfw install text-formatter
```

## Commands
```bash
python main.py case upper "hello world"         # Convert to uppercase
python main.py case lower "HELLO"               # Convert to lowercase
python main.py case title "hello world"         # Title case
python main.py case camel "hello world"         # camelCase
python main.py case snake "hello world"         # snake_case
python main.py case kebab "hello world"         # kebab-case
python main.py clean < input.txt               # Clean whitespace
python main.py clean --aggressive < input.txt  # Aggressive clean
python main.py count < document.txt            # Word count
```

## Common Examples
```bash
# Convert text case
python main.py case upper "hello world"
python main.py case camel "hello world"

# Clean up messy text
python main.py clean < messy.txt
python main.py clean --aggressive < messy.txt

# Count words
python main.py count < document.txt
```

## Help
```bash
python main.py --help
```
