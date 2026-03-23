# Invoice Generator — Quick Reference

## Install
```bash
smfw install invoice-generator
```

## Commands
```bash
python main.py create --client "Client Name" --items "Service,100,1"    # Create invoice
python main.py list                                                    # List invoices
python main.py show INV-001                                           # View invoice
python main.py pdf INV-001                                            # Export to PDF
python main.py mark INV-001 --paid                                    # Mark as paid
```

## Common Examples
```bash
# Create a new invoice
python main.py create --client "Acme Corp" --items "Consulting,150,10"

# List all invoices
python main.py list

# View invoice details
python main.py show INV-001

# Export to PDF
python main.py pdf INV-001 --output invoice.pdf

# Mark as paid
python main.py mark INV-001 --paid
```

## Help
```bash
python main.py --help
python main.py create --help
```
