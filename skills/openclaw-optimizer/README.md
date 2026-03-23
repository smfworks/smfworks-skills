# OpenClaw Optimizer

> Audit and optimize your OpenClaw workspace for cost, performance, and context efficiency

---

## What It Does

OpenClaw Optimizer analyzes your OpenClaw workspace and provides recommendations for optimizing cost, performance, and context usage. It identifies large files, bloated skills, context bloat, and suggests model routing strategies — all advisory, nothing changes automatically.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Pro tier:**
```bash
smfw install openclaw-optimizer
smf login
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Run a full workspace audit:

```bash
smf run openclaw-optimizer audit
```

---

## Commands

### `audit`

**What it does:** Run a complete workspace audit with size analysis, skills analysis, and recommendations.

**Usage:**
```bash
smf run openclaw-optimizer audit
```

**Example:**
```bash
smf run openclaw-optimizer audit
```

**Output:**
```
======================================================================
  OpenClaw Workspace Audit Report
======================================================================
  Generated: 2026-03-20 14:30:52

📊 Size Analysis
----------------------------------------------------------------------
  Total Size: 125.3 MB

  By Category:
    • bootstrap      12.5 KB (0.01%)
    • memory        45.2 MB (36.08%)
    • config         8.1 KB (0.01%)
    • skills        80.0 MB (63.86%)

  Large Files (>1MB):
    • memory/2026-02-archive.md  15.2 MB
    • memory/old-notes.md          8.5 MB

======================================================================
🛠️  Skills Analysis
----------------------------------------------------------------------
  Total Skills: 12
  Total Skill Size: 80.0 MB

  Top 5 Skills by Size:
    • skill-manager              12.3 MB
    • openclaw-backup             8.1 MB
    • email-campaign              7.5 MB
    • database-backup             6.2 MB
    • report-generator             5.8 MB

======================================================================
📝 Context Analysis
----------------------------------------------------------------------
  Memory Files: 45
  Total Memory Size: 45.2 MB

======================================================================
💡 Recommendations
----------------------------------------------------------------------

  🟠 [HIGH] Memory directory is 45.2 MB. This impacts context window.
      → Archive old memory files
      → Remove unused entries
      → Consider compacting MEMORY.md

  🟡 [MEDIUM] 2 skills are >5MB. Review for bloat.
      → skill-manager (12.3 MB)
      → openclaw-backup (8.1 MB)

  🟡 [MEDIUM] Consider unloading 2 unused skills.

======================================================================
```

---

### `analyze`

**What it does:** Analyze specific aspects of your workspace.

**Usage:**
```bash
smf run openclaw-optimizer analyze [options]
```

**Options:**

| Option | Required | Description |
|--------|----------|-------------|
| `--context` | ❌ No | Analyze memory/context bloat |
| `--skills` | ❌ No | Analyze loaded skills |

**Example:**
```bash
smf run openclaw-optimizer analyze --context
smf run openclaw-optimizer analyze --skills
```

---

### `recommend`

**What it does:** Get optimization recommendations and model routing suggestions.

**Usage:**
```bash
smf run openclaw-optimizer recommend [options]
```

**Options:**

| Option | Required | Description |
|--------|----------|-------------|
| `--model-routing` | ❌ No | Include model routing plan |

**Example:**
```bash
smf run openclaw-optimizer recommend
smf run openclaw-optimizer recommend --model-routing
```

---

### `report`

**What it does:** Generate and save a full optimization report.

**Usage:**
```bash
smf run openclaw-optimizer report
```

**Example:**
```bash
smf run openclaw-optimizer report
```

---

## Use Cases

- **Cost optimization:** Identify skills/features that increase costs
- **Performance tuning:** Find what's slowing down your workspace
- **Context management:** Reduce context window bloat
- **Model routing:** Route tasks to the most cost-effective model
- **Cleanup:** Get actionable steps to reduce workspace size

---

## Tips & Tricks

- Run `audit` monthly to catch issues early
- Use `recommend --model-routing` to optimize model selection
- Reports are saved to `~/.smf/optimizer-reports/` for review
- All recommendations are advisory — you decide what to act on

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Subscription required" | Run `smf login` to activate Pro access |
| Audit shows no issues | Your workspace is well-optimized! |
| Recommendations seem wrong | Consider your specific use case — recommendations are generic |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- Pro subscription

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/openclaw-optimizer)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
