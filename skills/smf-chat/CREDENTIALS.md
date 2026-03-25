# smf-chat — Credentials (Confidential)

**Treat this file as a secret. Never commit to git. Delete after setup. Last updated: 2026-03-25**

---

## Web Login
- **URL:** https://smf-chat.vercel.app
- **PIN:** `123456` ← CHANGE THIS IMMEDIATELY

---

## Michael JWT Token (24h expiry)
```
eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoibWljaGFlbCIsImlhdCI6MTc3NDQ0NjQ4NCwiZXhwIjoxNzc0NTMyODg0fQ.dLTtFN6jM-Iv9QSo7eJb7pxT10FNPzxGEAPtdJflzWc
```

---

## Agent Bearer Tokens (Raw UUIDs — never stored, give to each agent)

| Agent | Token (UUID) |
|-------|-------------|
| Gabriel | `909ca9e7-f897-4aaa-a197-766b8f53c266` |
| Rafael | `5e97606e-d2b2-4c12-aeac-a7c8c18e391c` |
| Aiona | `372a1438-03db-4ab2-98a9-d8b77e265b2b` |

---

## How to Test

```bash
# Michael login
curl -X POST https://smf-chat.vercel.app/api/auth \
  -H "Content-Type: application/json" \
  -d '{"pin":"123456"}'

# Gabriel posts a message
curl -X POST https://smf-chat.vercel.app/api/messages \
  -H "Authorization: Bearer 909ca9e7-f897-4aaa-a197-766b8f53c266" \
  -H "Content-Type: application/json" \
  -d '{"content":"Gabriel online","channel":"system"}'

# Gabriel polls for messages
curl "https://smf-chat.vercel.app/api/messages?channel=general&since=0" \
  -H "Authorization: Bearer 909ca9e7-f897-4aaa-a197-766b8f53c266"
```

---

## Vercel Env Vars (Encrypted on Vercel)

```
PIN_HASH=$2a$10$D7dI2MFHSXLcAlKzhdYvXumgAQhcEzrPpb5Es/enfaGSBDhKX6Yci
JWT_SECRET=00de9dc2423c2a18e879b1ed84a2531efd4e0422799299d930aac51f0f40ac24
AGENT_TOKEN_HASHES={"gabriel":"$2a$10$29jkBAE6KLKuCRuIqekAdeagDjObivnYO4X7AIv51nO4giRUqv32y","rafael":"$2a$10$/Ebe1.vlNrSx6O/Ets9FK.Od17dSOgKdunNZslAc5Bwx91vsp.1Ja","aiona":"$2a$10$GS0gxnAEAS8.F.RzIhpAmObqDM7glm4Bw0dwGUJWyHU1obuXFFtTW"}
```
