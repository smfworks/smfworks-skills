# OpenClaw Optimizer

> Audit your OpenClaw workspace for performance issues — bloated context, too many skills, oversized memory files — and get specific optimization recommendations.

**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo at [smfworks.com/subscribe](https://smfworks.com/subscribe))  
**Version:** 1.0  
**Category:** System / Performance

---

## What It Does

OpenClaw Optimizer is an OpenClaw Pro skill that analyzes your OpenClaw workspace and skills setup for performance issues. It checks workspace size and file breakdown, identifies large files that inflate your agent's context, counts loaded skills and flags bloat, reviews your memory files for optimization opportunities, and generates a full optimization report with specific, actionable recommendations.

**What it does NOT do:** It does not automatically fix issues (it only reports and recommends), delete files, modify your workspace, or analyze the agent's actual prompt token usage directly.

---

## Prerequisites

- [ ] **SMF Works Pro subscription** — [smfworks.com/subscribe](https://smfworks.com/subscribe)
- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed and authenticated**

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/openclaw-optimizer
python3 main.py help
```

---

## Quick Start

Run a full audit:

```bash
python3 main.py audit
```

Output:
```
🔍 OpenClaw Workspace Audit
══════════════════════════════════════════════

Workspace: /home/user/.openclaw/workspace
Total size: 847 KB
Files: 34

📊 Context Analysis
   MEMORY.md: 24 KB ⚠️ Large — consider pruning old entries
   SOUL.md: 8 KB ✅
   AGENTS.md: 12 KB ✅
   memory/: 156 KB (18 daily files)
   Other: 647 KB

🔧 Skills Analysis
   Installed skills: 23
   ⚠️ High skill count — each skill adds loading overhead

💡 Recommendations
   1. Prune MEMORY.md — remove entries older than 90 days
   2. Archive old daily memory files (keep last 30 days)
   3. Consider using fewer skills for leaner context
   4. Large files in workspace: config-backup.tar.gz (512 KB)

Report saved to: ~/.smf/optimizer-reports/report-2024-03-15.txt
```

---

## Command Reference

### `audit`

Full workspace audit. Checks all dimensions: workspace size, context bloat, skill count, memory files, and large files.

```bash
python3 main.py audit
```

---

### `analyze --context`

Analyzes context bloat specifically — which files are large and contributing to slow agent responses.

```bash
python3 main.py analyze --context
```

Output:
```
📊 Context Analysis

Files loaded into agent context:
  MEMORY.md: 24 KB ⚠️ Large
  SOUL.md: 8 KB ✅
  AGENTS.md: 12 KB ✅
  USER.md: 2 KB ✅
  IDENTITY.md: 1 KB ✅
  TOOLS.md: 3 KB ✅

Total context size: 50 KB
Recommendation: MEMORY.md is the largest file. Review and prune old entries.
```

---

### `analyze --skills`

Analyzes your installed skills — count, sizes, and which ones may be unused.

```bash
python3 main.py analyze --skills
```

Output:
```
🔧 Skills Analysis

Installed skills: 23
Total skills size: 4.2 MB

Large skills:
  booking-engine: 48 KB
  email-campaign: 52 KB
  report-generator: 44 KB

⚠️ High skill count — consider removing skills you don't use regularly
```

---

### `recommend`

Gets optimization recommendations based on current workspace state.

```bash
python3 main.py recommend
```

Output:
```
💡 Optimization Recommendations

Priority: HIGH
1. Prune MEMORY.md (24 KB → target <10 KB)
   Action: Remove entries older than 90 days; keep only most relevant memories

Priority: MEDIUM  
2. Archive old daily memory files
   Action: Keep last 30 days in memory/, archive or delete older ones

3. Remove unused skills
   Action: Run 'skill-manager --list' to see installed skills, remove ones you don't use

Priority: LOW
4. Remove large non-text files from workspace
   Action: config-backup.tar.gz (512 KB) doesn't belong in the workspace
```

---

### `optimize --skills`

Analyzes skills for removal candidates.

```bash
python3 main.py optimize --skills
```

---

### `report`

Generates a full optimization report and saves it to `~/.smf/optimizer-reports/`.

```bash
python3 main.py report
```

Output:
```
📄 Report generated: ~/.smf/optimizer-reports/report-2024-03-15.txt
```

---

## What It Checks

| Check | What it analyzes | What triggers a warning |
|-------|-----------------|------------------------|
| Workspace size | Total size of workspace directory | > 5 MB |
| MEMORY.md size | Size of your long-term memory file | > 15 KB |
| Daily memory files | Number of daily note files | > 60 files |
| Skill count | Number of installed skills | > 20 skills |
| Large files | Non-text files in workspace | > 100 KB |
| Old memory files | Age of oldest daily note | > 90 days |

---

## Use Cases

### 1. Monthly workspace health check

```bash
python3 main.py audit
```

Run monthly to catch creeping workspace bloat before it impacts performance.

### 2. Diagnose slow agent responses

If your agent seems slower than usual:

```bash
python3 main.py analyze --context
```

Large context files are the most common cause of slower responses.

### 3. Before adding new skills

```bash
python3 main.py analyze --skills
```

See how many skills you already have. Consider removing unused ones before adding new ones.

### 4. Get a prioritized to-do list for workspace cleanup

```bash
python3 main.py recommend
```

Specific, prioritized recommendations for what to clean up.

---

## Applying Recommendations

The optimizer recommends but does not act. Here's how to apply common recommendations:

**Prune MEMORY.md:**
```bash
nano ~/.openclaw/workspace/MEMORY.md
# Remove old, stale, or irrelevant entries
```

**Archive old daily memory files:**
```bash
mkdir -p ~/.openclaw/workspace/memory/archive
mv ~/.openclaw/workspace/memory/2023-*.md ~/.openclaw/workspace/memory/archive/
```

**Remove unused skills:**
```bash
python3 ~/smfworks-skills/skills/skill-manager/main.py --list
python3 ~/smfworks-skills/skills/skill-manager/main.py --remove skill-name
```

**Remove large files from workspace:**
```bash
ls -lh ~/.openclaw/workspace/
# Identify and move/delete large files that don't belong there
```

---

## Configuration

Reports are saved to: `~/.smf/optimizer-reports/`  
No configuration file needed.

---

## Troubleshooting

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

### `Workspace not found`
**Fix:** OpenClaw workspace not found at default location. Verify `~/.openclaw/workspace/` exists.

### Audit shows nothing to optimize
Congratulations! Your workspace is in good shape.

---

## FAQ

**Q: Will running the optimizer change anything?**  
A: No. The optimizer only reads and analyzes. It never modifies files.

**Q: How often should I run an audit?**  
A: Monthly is sufficient for most users. Run it after major changes to your workspace (adding many new memory entries, installing many skills, etc.).

**Q: What's a good target size for MEMORY.md?**  
A: Under 10 KB. A curated MEMORY.md with the most important long-term context keeps your agent fast and focused. Bigger isn't better — quality over quantity.

**Q: Does skill count really affect performance?**  
A: Yes. Each installed skill adds to the loading context. 5–10 skills is lean; 20+ is high. Remove skills you don't use regularly.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| SMF Works Pro | Required ($19.99/mo) |
| External APIs | None |
| Internet | For subscription check only |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/openclaw-optimizer)
- 🔑 [Subscribe](https://smfworks.com/subscribe)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
