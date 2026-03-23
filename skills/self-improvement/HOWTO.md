# Self-Improvement — Quick Reference

## Install
```bash
smfw install self-improvement
```

## Commands
```bash
smf run self-improvement log-error "Error description"                 # Log an error
smf run self-improvement log-learning "What I learned"               # Log a learning
smf run self-improvement list                                           # List all items
smf run self-improvement list --type error                            # List errors only
smf run self-improvement search "keyword"                              # Search items
smf run self-improvement show ITEM-ID                                  # Show item details
smf run self-improvement promote ITEM-ID                               # Promote to memory
smf run self-improvement stats                                         # Show statistics
```

## Common Examples
```bash
# Log an error with context
smf run self-improvement log-error "File not found" --context "Reading config.json"

# Log a learning
smf run self-improvement log-learning "Always check file exists first"

# List all items
smf run self-improvement list

# Search for related items
smf run self-improvement search "json"

# Promote important item to memory
smf run self-improvement promote LRN-20260320-ABC123

# View statistics
smf run self-improvement stats
```

## Help
```bash
smf run self-improvement help
```
