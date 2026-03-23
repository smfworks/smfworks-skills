# OpenClaw Optimizer — Quick Reference

## Install
```bash
smfw install openclaw-optimizer
```

## Commands
```bash
smf run openclaw-optimizer audit                    # Full workspace audit
smf run openclaw-optimizer analyze --context      # Analyze context bloat
smf run openclaw-optimizer analyze --skills       # Analyze skills
smf run openclaw-optimizer recommend              # Get recommendations
smf run openclaw-optimizer report                 # Generate report
```

## Common Examples
```bash
# Run full audit
smf run openclaw-optimizer audit

# Analyze context bloat
smf run openclaw-optimizer analyze --context

# Get recommendations
smf run openclaw-optimizer recommend --model-routing

# Generate and save report
smf run openclaw-optimizer report
```

## Help
```bash
smf run openclaw-optimizer help
```
