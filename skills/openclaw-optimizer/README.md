# OpenClaw Optimizer

Audit and optimize OpenClaw workspace for cost, performance, and context efficiency.

## Features

- ✅ **Workspace Audit** — Analyze size, structure, and bloat
- ✅ **Context Analysis** — Identify bloat sources
- ✅ **Skill Surface Audit** — Review always-loaded skills
- ✅ **Model Routing** — Get recommendations for task-based routing
- ✅ **Safety First** — Advisory only, no auto-changes

## Installation

```bash
smf install openclaw-optimizer
```

## Usage

### Full Audit

```bash
smf run openclaw-optimizer audit
```

### Analyze Context Bloat

```bash
smf run openclaw-optimizer analyze --context
```

### Get Model Routing Plan

```bash
smf run openclaw-optimizer recommend --model-routing
```

## Safety

- This skill is **advisory only**
- No changes are made automatically
- All recommendations require explicit approval
- Rollback plans provided for every change

## Pricing

OpenClaw Optimizer is a premium SMF Works skill.

- **Price:** $19.99/month
- Subscribe at https://smf.works/subscribe
