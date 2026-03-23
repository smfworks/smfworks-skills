# Skill Manager — Quick Reference

## Install
```bash
smfw install skill-manager
```

## Commands
```bash
smf run skill-manager                      # Interactive management UI
smf run skill-manager --list             # List all skills
smf run skill-manager --remove [skill]    # Remove a skill
smf run skill-manager --backup [skill]    # Backup a skill
```

## Common Examples
```bash
# Open interactive management UI
smf run skill-manager

# List all installed skills
smf run skill-manager --list

# Remove a skill (with dry-run first)
smf run skill-manager --remove some-skill --dry-run
smf run skill-manager --remove some-skill

# Backup a specific skill
smf run skill-manager --backup some-skill
```

## Help
```bash
smf run skill-manager --help
```
