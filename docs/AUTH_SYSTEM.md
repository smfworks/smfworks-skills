# SMF Works Auth System

Authentication and subscription system for SMF Works Pro skills.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   SMF Skills    │     │   SMF Works      │     │   Stripe        │
│   (Local)       │────▶│   API (Vercel)   │◀────│   (Billing)     │
│                 │◀────│                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │
        │                 ┌──────┴──────┐
        │                 │  Database   │
        │                 │ (Revocations│
        │                 │  + Tokens)   │
        │                 └─────────────┘
        │
   ~/.smf/token
```

## Components

### 1. Shared Auth Library (`shared/smf_auth.py`)

Embedded in every Pro skill. Handles:
- JWT token loading from `~/.smf/token`
- Local token validation (offline support)
- Revocation list checking
- Subscription tier verification

**Usage in skills:**
```python
from smf_auth import require_subscription, show_subscription_error

sub = require_subscription("lead-capture", min_tier="pro")
if not sub["valid"]:
    show_subscription_error(sub)
    sys.exit(1)

# Skill runs...
```

### 2. Vercel API Routes (`smfworks-site/app/api/`)

| Route | Method | Purpose |
|-------|--------|---------|
| `/api/token/issue` | POST | Issue new JWT token |
| `/api/token/issue` | GET | Get public key for verification |
| `/api/token/validate` | POST | Validate token server-side |
| `/api/webhook/stripe` | POST | Handle Stripe events |
| `/api/revocation-list` | GET | Get revoked subscriber IDs |

### 3. CLI Tool (`cli/smf_login.py`)

```bash
# Authenticate
python cli/smf_login.py login

# Check status
python cli/smf_login.py status

# Logout
python cli/smf_login.py logout
```

### 4. Pro Skill Template (`templates/pro_skill_template.py`)

Template for building subscription-restricted skills.

## Token Format (JWT)

```json
{
  "sub": "cus_abc123",
  "tier": "pro",
  "skills": ["*"],
  "iat": 1710000000,
  "exp": 1741632000
}
```

- `sub`: Stripe customer ID
- `tier`: "pro" or "enterprise"
- `skills`: Array of allowed skill names or `"*"` for all
- `iat`: Issued at timestamp
- `exp`: Expiration timestamp

## Subscription Flow

1. **User signs up** on smf.works
2. **Stripe webhook** triggers on `customer.subscription.created`
3. **Vercel API** issues JWT token via `/api/token/issue`
4. **User runs** `smf login` and pastes token
5. **Token saved** to `~/.smf/token`
6. **Pro skills** validate token locally before running

## Cancellation Flow

1. **User cancels** subscription
2. **Stripe webhook** triggers on `customer.subscription.deleted`
3. **Vercel API** adds customer to revocation list
4. **Skills check** revocation list on startup (cached locally)
5. **Token invalidated** — skill shows subscription error

## Security

- **JWT signed** with RS256 (asymmetric)
- **Public key** embedded in skills for offline verification
- **Private key** stored only on Vercel server
- **Token stored** in `~/.smf/token` with 0600 permissions
- **Revocation list** checked periodically (cached for offline grace period)

## Environment Variables (Vercel)

```bash
SMF_JWT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----..."
SMF_JWT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----..."
STRIPE_SECRET_KEY="sk_live_..."
STRIPE_WEBHOOK_SECRET="whsec_..."
```

## Development Mode

All Pro skills support `--test-mode` flag:

```bash
python main.py --test-mode
```

This skips subscription check for development/testing.

## Free vs Pro Skills

| Feature | Free Skills | Pro Skills |
|---------|-------------|------------|
| Auth required | ❌ No | ✅ Yes |
| Subscription | N/A | $19.99/mo |
| Install | `pip install` | `pip install` + `smf login` |
| Offline | Always works | Grace period ~24hrs |

## Next Steps

1. **Generate RSA keypair** for JWT signing
2. **Deploy API routes** to Vercel
3. **Set up Stripe** products and webhooks
4. **Test** with a sample Pro skill
5. **Build** real Pro skills (Lead Capture, CRM, etc.)

---

*SMF Works Auth System v1.0*
