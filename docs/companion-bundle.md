# Companion bundle

This page is a pointer. The canonical OpenClaw companion map — ownership, the three SMF pieces, and suggested install order — lives in the vision repo:

**[smf-openclaw-vision/docs/companion-bundle.md](https://github.com/smfworks/smf-openclaw-vision/blob/main/docs/companion-bundle.md)**

Do not treat this file as a second copy of that map.

## Short version

- **OpenClaw** is required and is not an SMF Works product. Install from [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw). Site: [openclaw.ai](https://openclaw.ai). Docs: [docs.openclaw.ai](https://docs.openclaw.ai). [smfworks/openclaw](https://github.com/smfworks/openclaw) is a fork/mirror only, not the canonical source.
- **Skills** — this repo. Free skills install with `install.sh` and `smfw` (see the [README](../README.md#openclaw-companion)).
- **Memory** — [mnemosyne-openclaw](https://github.com/smfworks/mnemosyne-openclaw): offline SQLite memory for the OpenClaw gateway. Optional.
- **Vision** — [smf-openclaw-vision](https://github.com/smfworks/smf-openclaw-vision): iPhone vision over Tailscale. Optional.

**Suggested order:** upstream OpenClaw → skills (this repo) → optional memory → optional vision.
