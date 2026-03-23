# Form Builder — Quick Reference

## Install
```bash
smfw install form-builder
```

## Commands
```bash
python main.py create "My Form"                        # Create form interactively
python main.py create "Contact" --fields name,email    # With fields
python main.py list                                    # List forms
python main.py render contact-form                     # Generate HTML
python main.py export contact-form --format json        # Export form
```

## Common Examples
```bash
# Create a new form interactively
python main.py create "Contact Form"

# Create with predefined fields
python main.py create "Survey" --fields name,email,feedback

# List all forms
python main.py list

# Generate HTML for a form
python main.py render contact-form

# Export form definition
python main.py export contact-form --format json
```

## Help
```bash
python main.py --help
python main.py create --help
```
