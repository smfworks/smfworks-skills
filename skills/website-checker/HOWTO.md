# Website Checker — Quick Reference

## Install
```bash
smfw install website-checker
```

## Commands
```bash
python main.py check https://example.com                 # Check URL status
python main.py check https://example.com --timeout 30   # Custom timeout
python main.py ssl example.com                          # Check SSL certificate
python main.py ssl example.com 8443                     # Custom port
python main.py bulk https://google.com https://github.com  # Check multiple
```

## Common Examples
```bash
# Check if website is up
python main.py check https://google.com

# Check with longer timeout
python main.py check https://slow-site.com --timeout 30

# Check SSL certificate
python main.py ssl smf.works

# Check multiple sites
python main.py bulk https://google.com https://github.com https://twitter.com
```

## Help
```bash
python main.py --help
python main.py check --help
```
