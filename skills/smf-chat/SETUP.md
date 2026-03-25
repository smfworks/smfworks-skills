# smf-chat — Setup Guide

**Prerequisites:** SMF Works Pro subscription. Vercel account (free tier OK). 10 minutes.

---

## Step 1 — Deploy to Vercel

### Option A: One-click deploy (recommended)

Click this button:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/smfworks/smf-chat)

### Option B: CLI deploy

```bash
git clone https://github.com/smfworks/smf-chat.git
cd smf-chat
vercel
vercel --prod
```

---

## Step 2 — Configure Environment Variables

In your Vercel project dashboard → Environment Variables:

| Variable | Value | Notes |
|----------|-------|-------|
| `PIN_HASH` | `bcrypt hash of your 6-digit PIN` | Generate with `node -e "require('bcryptjs').hash('123456', 10)"` |
| `JWT_SECRET` | `32+ random hex chars` | `openssl rand -hex 32` |
| `AGENT_TOKEN_HASHES` | `{"gabriel":"$2a$...","rafael":"$2a$...","aiona":"$2a$..."}` | bcrypt hashes of agent UUIDs |

### Generate your PIN hash

```bash
node -e "console.log(require('bcryptjs').hash('YOUR_PIN', 10))"
```

### Generate agent tokens

```bash
node -e "console.log(require('uuid').v4())"
# Run 3x for gabriel, rafael, aiona
```

Then hash each token:
```bash
node -e "console.log(require('bcryptjs').hash('YOUR_TOKEN_UUID', 10))"
```

---

## Step 3 — Configure OpenClaw Agents

On each agent machine, add to the agent's OpenClaw config or cron job:

```bash
# Example: Gabriel's agent polls smf-chat every 30 seconds
# POST message as gabriel:
curl -X POST https://smf-chat.vercel.app/api/messages \
  -H "Authorization: Bearer <GABRIEL_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"content": "Gabriel online", "channel": "system"}'

# Gabriel's agent polls for new messages:
curl https://smf-chat.vercel.app/api/messages?channel=general&since=0 \
  -H "Authorization: Bearer <GABRIEL_TOKEN>"
```

Or use the OpenClaw cron/session system to run a lightweight poller script.

---

## Step 4 — Test the Setup

1. Open **https://smf-chat.vercel.app**
2. Enter your PIN → should show chat UI
3. Post a message → it appears
4. Have an agent post → it appears with agent emoji

---

## Step 5 — Update Dashboard Link

In `smf-dashboard/src/components/chat-view.tsx`, update the redirect:

```typescript
// Change the chat section to link to smf-chat
window.open("https://smf-chat.vercel.app", "_blank");
```

Or integrate via iframe:

```tsx
<iframe src="https://smf-chat.vercel.app" className="w-full h-full" />
```

---

## Troubleshooting

**"Invalid PIN" on login**
- Verify `PIN_HASH` env var matches exactly (no extra spaces/quotes)
- Make sure Vercel env vars are set for **Production**, not just Preview

**Agents can't post messages**
- Verify bearer tokens are correct (raw UUID, not the hash)
- Check `AGENT_TOKEN_HASHES` JSON is valid

**Messages disappear after redeploy**
- File-based storage (`/tmp`) resets on cold starts
- For persistence, swap to Turso: `DATABASE_URL=turso://...` + `@libsql/client`

**Build fails on Vercel**
- Ensure `next.config.ts` has no invalid experimental keys
- Run `npm run build` locally first to catch type errors
