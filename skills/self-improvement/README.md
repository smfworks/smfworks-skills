# Self-Improvement

> Log errors, learnings, and insights for continuous improvement — coding agents process these into fixes

---

## What It Does

Self-Improvement builds a knowledge base of your errors, learnings, and insights over time. Log what goes wrong, what you learn, and what insights you gain. Coding agents can process these logs to identify patterns and promote important items to your project memory.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Pro tier:**
```bash
smfw install self-improvement
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

Log an error you just encountered:

```bash
smf run self-improvement log-error "File not found" --context "Reading config.json"
```

---

## Commands

### `log-error`

**What it does:** Log an error with context, severity, and resolution.

**Usage:**
```bash
smf run self-improvement log-error [description] [options]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `description` | ✅ Yes | Error description | `File not found` |

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--context` | ❌ No | What were you doing | `--context "Reading config"` |
| `--severity` | ❌ No | low/medium/high/critical | `--severity high` |
| `--tags` | ❌ No | Comma-separated tags | `--tags "file-io,config"` |
| `--resolution` | ❌ No | How you fixed it | `--resolution "Added check"` |
| `--prevention` | ❌ No | How to prevent | `--prevention "Validate path"` |

**Example:**
```bash
smf run self-improvement log-error "JSON parse error" --context "API response" --severity medium --tags "json,api"
```

---

### `log-learning`

**What it does:** Log an insight or best practice you discovered.

**Usage:**
```bash
smf run self-improvement log-learning [insight] [options]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `insight` | ✅ Yes | What you learned | `Validate JSON first` |

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--category` | ❌ No | Category type | `--category best-practice` |
| `--context` | ❌ No | When does this apply | `--context "API calls"` |
| `--tags` | ❌ No | Comma-separated tags | `--tags "python,json"` |

**Categories:** `best-practice`, `pattern`, `anti-pattern`, `optimization`, `architecture`, `other`

**Example:**
```bash
smf run self-improvement log-learning "Use pathlib instead of os.path" --category best-practice
```

---

### `list`

**What it does:** List all logged items with optional filters.

**Usage:**
```bash
smf run self-improvement list [options]
```

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--type` | ❌ No | Filter by type | `--type error` |
| `--status` | ❌ No | Filter by status | `--status open` |
| `--category` | ❌ No | Filter by category | `--category best-practice` |

**Example:**
```bash
smf run self-improvement list
smf run self-improvement list --type error
smf run self-improvement list --category best-practice
```

---

### `search`

**What it does:** Search all logged items by keyword.

**Usage:**
```bash
smf run self-improvement search [keyword]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `keyword` | ✅ Yes | Search term | `json` |

**Example:**
```bash
smf run self-improvement search "config"
```

---

### `show`

**What it does:** Display full details of a specific item.

**Usage:**
```bash
smf run self-improvement show [item-id]
```

**Example:**
```bash
smf run self-improvement show ERR-20260320-ABC123
```

---

### `promote`

**What it does:** Promote an important item to your project memory.

**Usage:**
```bash
smf run self-improvement promote [item-id]
```

**Example:**
```bash
smf run self-improvement promote LRN-20260320-DEF456
```

---

### `stats`

**What it does:** Display improvement statistics.

**Usage:**
```bash
smf run self-improvement stats
```

---

## Use Cases

- **Error tracking:** Log bugs and their solutions for future reference
- **Learning journal:** Record insights and best practices
- **Knowledge base:** Build a searchable database of solutions
- **Agent training:** Help coding agents avoid past mistakes
- **Retrospectives:** Provide data for team retrospectives

---

## Tips & Tricks

- Log errors immediately while context is fresh
- Use tags consistently for better search results
- Promote important learnings to project memory
- Review weekly to identify patterns
- Use categories to organize learnings

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Subscription required" | Run `smf login` to activate Pro access |
| "Item not found" | Check the item ID from `list` output |
| Empty search results | Try different keywords or check spelling |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- Pro subscription

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/self-improvement)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
