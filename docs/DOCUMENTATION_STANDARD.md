# SMF Works Skill — End-User Documentation Standard

**Version:** 1.0  
**Created:** 2026-03-23  
**Status:** Active — required for all skills

> This standard defines what complete end-user documentation looks like for every SMF Works OpenClaw skill.
> **All new and remediated skills must meet this standard before being considered done.**

The full standard (with rationale, tone guide, and subagent task spec instructions) lives in the Obsidian vault:
`/home/mikesai1/Documents/Obsidian/MikesAI/SMF Works/Skill End-User Documentation Standard.md`

What follows is the working reference for anyone building or improving skill documentation.

---

## Required Files Per Skill

```
skills/[skill-name]/
├── README.md       # Full reference docs — 250+ lines
├── SETUP.md        # Install & config walkthrough — 100–300+ lines
└── HOWTO.md        # Goal-based usage walkthroughs — 200+ lines
```

All three are mandatory. A skill without all three is incomplete.

---

## README.md — Required Sections

1. **Header** — name, one-sentence value prop, tier, version
2. **What It Does** — plain language, 3–5 sentences, includes what it does NOT do
3. **Prerequisites** — checkbox list with Python version, OpenClaw version, subscription tier, API keys
4. **Installation** — step-by-step with expected output shown
5. **Quick Start** — fastest path to a result, with realistic output example
6. **Command Reference** — every command with: usage, arguments table, options table, example, output block
7. **Use Cases** — 3–5 real-world scenarios with commands and results
8. **Configuration** — env vars / config file options (even if "none required")
9. **Troubleshooting** — 5+ real error messages with specific fixes
10. **FAQ** — 5+ real user questions with complete answers
11. **Requirements table** — Python, OpenClaw, OS, tier, external APIs
12. **Support footer** — links to docs, GitHub issues, Discord, contact

---

## SETUP.md — Required Sections

1. **Header** — estimated time, difficulty, tier
2. **What You'll Need** — table with every dependency, link, and cost
3. **Step-by-step setup** — numbered, every step shows what success looks like
   - Simple skills: verify OpenClaw → install → first run
   - API-dependent skills: account creation → API key → config → install → verify
4. **Verify Your Setup** — single test command with exact expected output
5. **Configuration Options** — settings table (if applicable)
6. **Troubleshooting** — setup-specific errors and fixes
7. **Next Steps** — pointer to HOWTO.md

---

## HOWTO.md — Required Sections

1. **Header** — prerequisites: setup complete
2. **Table of Contents** — links to all walkthroughs
3. **5+ goal-based walkthroughs** — each one:
   - States what it does and when to use it
   - Numbered steps with "why" explanation per step
   - Expected output after each command
   - Final "Result:" summary
4. **Automating with Cron** — how to schedule the skill; includes cron expression table
5. **Combining with Other Skills** (if applicable) — multi-skill workflow example
6. **Troubleshooting Common Issues** — runtime errors (not setup errors)
7. **Tips & Best Practices** — skill-specific, non-obvious advice

---

## Quality Bar Checklist

### README.md
- [ ] 250+ lines
- [ ] Prerequisites with checkboxes
- [ ] Installation with expected output
- [ ] Quick Start with realistic output example
- [ ] Every command: arguments table + output example
- [ ] 3+ use case scenarios
- [ ] 5+ real error messages in troubleshooting
- [ ] 5+ real Q&A in FAQ
- [ ] Requirements table complete

### SETUP.md
- [ ] 100+ lines (simple) / 300+ lines (API-dependent)
- [ ] "What you'll need" table with links and costs
- [ ] Every step numbered with success indicator
- [ ] API key walkthrough (if applicable)
- [ ] Verification command with expected output
- [ ] Ends pointing to HOWTO.md

### HOWTO.md
- [ ] 200+ lines
- [ ] Table of contents
- [ ] 5+ complete goal-based walkthroughs
- [ ] Each walkthrough: context + numbered steps + output + result
- [ ] Cron/automation section
- [ ] Runtime troubleshooting section
- [ ] Tips & Best Practices section

---

## Key Rules

1. **Write for a smart non-technical user** — knows terminal, doesn't know every flag
2. **Show real output, not placeholders** — "[your output here]" is not acceptable
3. **Explain the why** — every step gets one sentence on why the user is doing it
4. **Be specific** — "You should see: `✅ Done`" not "You should see a success message"
5. **Troubleshooting uses real error messages** — copy from actual skill output

---

## Subagent Task Spec Template

Use this when spawning a subagent to write skill documentation:

```
Task: Write complete end-user documentation for the [skill-name] skill.

Files to create/update:
- skills/[skill-name]/HOWTO.md (rewrite from scratch)
- skills/[skill-name]/SETUP.md (create if missing, rewrite if exists)
- skills/[skill-name]/README.md (expand to meet standard)

Standard to follow:
  /home/mikesai1/projects/smfworks-skills/docs/DOCUMENTATION_STANDARD.md

Skill tier: [Free / Pro]
main.py: skills/[skill-name]/main.py — read this first; all commands and args 
         must be accurate to the actual implementation

Audience: Non-technical user who has never used this skill before.

Definition of done: Every item in the quality bar checklist above is checked off.
Do not consider the task complete until all three files meet the line minimums 
and every checklist item passes.
```

---

*v1.0 — 2026-03-23 — Aiona Edge*  
*Full standard: /home/mikesai1/Documents/Obsidian/MikesAI/SMF Works/Skill End-User Documentation Standard.md*
