# OpenClaw Optimizer — How-To Guide

**Prerequisites:** SMF Works Pro subscription active. Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Run a Full Workspace Audit](#1-how-to-run-a-full-workspace-audit)
2. [How to Analyze Context Bloat](#2-how-to-analyze-context-bloat)
3. [How to Analyze Your Skills](#3-how-to-analyze-your-skills)
4. [How to Apply Optimization Recommendations](#4-how-to-apply-optimization-recommendations)
5. [How to Generate and Save a Report](#5-how-to-generate-and-save-a-report)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Run a Full Workspace Audit

**What this does:** Checks all dimensions of your OpenClaw workspace — size, context files, skills, memory — and produces a summary with recommendations.

**When to use it:** Monthly, or when you notice your agent responding more slowly than usual.

### Steps

**Step 1 — Navigate to the skill.**

```bash
cd ~/smfworks-skills/skills/openclaw-optimizer
```

**Step 2 — Run the full audit.**

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

🔧 Skills Analysis
   Installed skills: 23 ⚠️ High count

🔴 Issues Found: 3

💡 Recommendations
   1. [HIGH] Prune MEMORY.md — 24 KB → target <10 KB
   2. [MEDIUM] Archive old daily memory files
   3. [LOW] Remove config-backup.tar.gz from workspace

Report saved to: ~/.smf/optimizer-reports/report-2024-03-15.txt
```

**Step 3 — Prioritize the HIGH recommendations first.**

**Result:** A clear, prioritized list of what to fix.

---

## 2. How to Analyze Context Bloat

**What this does:** Focuses specifically on files that get loaded into your agent's context window, making it slower or less focused.

**When to use it:** When your agent seems slower than usual or gives generic responses.

### Steps

**Step 1 — Run context analysis.**

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

Total context: 50 KB

Recommendation:
  MEMORY.md is the largest file (24 KB).
  Target: < 10 KB
  Action: Remove entries older than 90 days, keep only the most relevant memories
```

**Step 2 — Prune MEMORY.md if recommended.**

```bash
nano ~/.openclaw/workspace/MEMORY.md
```

Remove:
- Entries about completed projects you no longer need
- Outdated preferences or context
- Duplicate information
- Very old dated entries

**Result:** Smaller context → faster, more focused agent responses.

---

## 3. How to Analyze Your Skills

**What this does:** Shows how many skills are installed and which ones are largest.

```bash
python3 main.py analyze --skills
```

Output:
```
🔧 Skills Analysis

Installed skills: 23
Total skills size: 4.2 MB

Largest skills:
  email-campaign: 52 KB
  booking-engine: 48 KB
  report-generator: 44 KB
  form-builder: 41 KB

⚠️ High skill count (23) — Consider removing skills you don't use regularly.
   Each installed skill adds context loading overhead.
```

---

## 4. How to Apply Optimization Recommendations

**What this does:** Shows your current recommendations in priority order.

```bash
python3 main.py recommend
```

**Applying each type of recommendation:**

### Prune MEMORY.md

```bash
nano ~/.openclaw/workspace/MEMORY.md
# Review entries, delete stale ones, save
```

Target: Keep only facts that are:
- Still accurate and relevant
- Not duplicated elsewhere
- Timeless rather than dated

### Archive old daily memory files

```bash
mkdir -p ~/.openclaw/workspace/memory/archive
# Move files older than 30 days:
cd ~/.openclaw/workspace/memory
for f in $(ls *.md | head -n -30); do mv "$f" archive/; done
```

### Remove unused skills

```bash
python3 ~/smfworks-skills/skills/skill-manager/main.py --list
python3 ~/smfworks-skills/skills/skill-manager/main.py --remove skill-name
```

### Remove large non-text files from workspace

```bash
ls -lh ~/.openclaw/workspace/
# Identify files > 100KB that shouldn't be there
# Move them: mv large-file.tar.gz ~/Backups/
```

---

## 5. How to Generate and Save a Report

**When to use it:** To track your workspace health over time, or share the audit with someone helping you configure OpenClaw.

```bash
python3 main.py report
```

Output:
```
📄 Report generated: ~/.smf/optimizer-reports/report-2024-03-15.txt
```

View the report:
```bash
cat ~/.smf/optimizer-reports/report-2024-03-15.txt
```

Compare to previous report:
```bash
diff ~/.smf/optimizer-reports/report-2024-02-01.txt ~/.smf/optimizer-reports/report-2024-03-15.txt
```

---

## 6. Automating with Cron

### Example: Monthly report on the 1st

```bash
0 9 1 * * python3 /home/yourname/smfworks-skills/skills/openclaw-optimizer/main.py report >> /home/yourname/logs/optimizer.log 2>&1
```

### Example: Weekly context check on Mondays

```bash
0 8 * * 1 python3 /home/yourname/smfworks-skills/skills/openclaw-optimizer/main.py analyze --context >> /home/yourname/logs/context-check.log 2>&1
```

---

## 7. Combining with Other Skills

**OpenClaw Optimizer + OpenClaw Backup:** Back up before making changes based on optimizer recommendations:

```bash
python3 ~/smfworks-skills/skills/openclaw-backup/main.py
python3 ~/smfworks-skills/skills/openclaw-optimizer/main.py recommend
# Apply recommendations
```

**OpenClaw Optimizer + Skill Manager:** Remove unused skills found by the analyzer:

```bash
python3 ~/smfworks-skills/skills/openclaw-optimizer/main.py analyze --skills
python3 ~/smfworks-skills/skills/skill-manager/main.py --list
python3 ~/smfworks-skills/skills/skill-manager/main.py --remove unused-skill
```

---

## 8. Troubleshooting Common Issues

### `Error: SMF Works Pro subscription required`

**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe) and re-authenticate.

### Audit shows high skill count but I use all of them

**Fix:** The threshold is a guideline. If you actively use all your skills, the warning is informational. Focus on other recommendations.

### MEMORY.md keeps growing back quickly

**Fix:** Your agent is writing a lot to memory. Review AGENTS.md to adjust what gets captured in daily notes vs. MEMORY.md. Quality over quantity — not everything needs to be in MEMORY.md.

### Large files appear in workspace that I don't recognize

**Fix:** Your agent or a skill may have created them. Check timestamps: `ls -lat ~/.openclaw/workspace/ | head -10`. If it's a backup or log file, move it out of the workspace.

---

## 9. Tips & Best Practices

**Run monthly, not obsessively.** Your workspace isn't going to bloat overnight. Monthly audits catch issues before they become real problems without adding maintenance overhead.

**Back up before applying recommendations.** Always run OpenClaw Backup before making significant changes to MEMORY.md or removing skills.

**MEMORY.md quality beats quantity.** A 5 KB MEMORY.md with the 20 most important facts about you is far more useful to your agent than a 25 KB file with 200 semi-relevant notes. Prune ruthlessly.

**Treat the skill count warning as a signal, not a rule.** If you have 25 skills but only use 5 regularly, consider removing the other 20. If you actively use all 25, the overhead is the cost of that capability.

**Save reports for trend tracking.** Keeping monthly reports lets you see if your workspace is growing faster than expected and identify what's driving the growth.
