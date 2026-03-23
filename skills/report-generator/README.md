# Report Generator

> Create professional HTML and text reports from CSV or JSON data with automatic statistics

---

## What It Does

Report Generator transforms your data (CSV or JSON) into beautiful, professional reports. Automatically calculates statistics (sum, mean, median, min, max), generates clean HTML output, and saves reports to your local machine.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Pro tier:**
```bash
smfw install report-generator
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

Create a report with built-in sample data:

```bash
smf run report-generator create --sample sales
```

---

## Commands

### `create`

**What it does:** Create a new report from data file or sample data.

**Usage:**
```bash
smf run report-generator create [options]
```

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--sample` | ❌ No | Use sample data (sales/customers/inventory) | `--sample sales` |
| `--data` | ❌ No | Path to CSV or JSON file | `--data sales.csv` |
| `--title` | ❌ No | Report title | `--title "Q1 Report"` |
| `--format` | ❌ No | Output format: html or text | `--format html` |
| `--value-column` | ❌ No | Column to calculate statistics on | `--value-column total` |

**Example:**
```bash
smf run report-generator create --sample sales
smf run report-generator create --data sales.csv --title "Q1 Sales"
smf run report-generator create --data data.json --format text
```

---

### `templates`

**What it does:** List available sample data templates.

**Usage:**
```bash
smf run report-generator templates
```

**Example:**
```bash
smf run report-generator templates
```

**Output:**
```
📊 Available Sample Templates:
------------------------------------------------------------
1. sales       — Sales transactions with products
2. customers   — Customer list with order history
3. inventory   — Product inventory with stock levels
```

---

## Use Cases

- **Sales reports:** Weekly or monthly sales summaries
- **Financial reports:** Revenue, expenses, profit analysis
- **Inventory reports:** Stock levels and reorder alerts
- **Customer analysis:** Order history and segmentation

---

## Tips & Tricks

- Use `--value-column` to automatically calculate statistics
- Sample data templates let you test without real data
- Reports are saved to `~/.smf/reports/`
- Use `--format text` for plain text output (great for email)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Subscription required" | Run `smf login` to activate Pro access |
| "File not found" | Check the path to your CSV or JSON file |
| Empty report | Ensure your data file has content |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- Pro subscription

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/report-generator)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
