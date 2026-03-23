# Form Builder — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo)

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| SMF Works Pro subscription | [smfworks.com/subscribe](https://smfworks.com/subscribe) | $19.99/mo |
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| OpenClaw | Installed and authenticated | Free |
| smfworks-skills repository | Cloned via git | Included |
| A web browser | For viewing and submitting forms | Free |

---

## Step 1 — Subscribe and Authenticate

```bash
openclaw auth status
```

If not subscribed: [smfworks.com/subscribe](https://smfworks.com/subscribe)

---

## Step 2 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 3 — Navigate and Verify

```bash
cd ~/smfworks-skills/skills/form-builder
python3 main.py help
```

---

## Verify Your Setup

Create and serve a test form:

**Step 1 — Create a form:**

```bash
python3 main.py create --name "Test Form" --fields name,email
```

Note the FORM-ID in the output.

**Step 2 — Serve it:**

```bash
python3 main.py serve FORM-XXXXX --port 8080
```

**Step 3 — Open in browser:**

Go to `http://localhost:8080/FORM-XXXXX` in your browser. You should see the form with name and email fields.

**Step 4 — Submit a test response:**

Fill in the form and click submit.

**Step 5 — Stop the server (Ctrl+C) and view responses:**

```bash
python3 main.py responses FORM-XXXXX
```

You should see your test submission. Setup is complete.

---

## Port Selection

The default port is `8080`. If it's already in use, pick another:

```bash
python3 main.py serve FORM-ID --port 9090
```

Check what's using a port: `lsof -i :8080`

---

## Firewall Notes

The server binds to `localhost` by default. If you want to serve on your LAN:

```bash
# Find your local IP
ip addr show | grep "inet 192"
# Then share: http://192.168.x.x:8080/FORM-ID
```

Note: Opening ports on a LAN exposes the form to all devices on that network.

---

## Troubleshooting

**`Error: SMF Works Pro subscription required`** — Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

**`Address already in use: port 8080`** — Use a different port: `--port 8081`

**Form not loading in browser** — Ensure the server is still running (it must stay running while you use the form).

---

## Next Steps

Setup complete. See **HOWTO.md** for walkthroughs on creating forms, adding fields, serving, collecting responses, and exporting data.
