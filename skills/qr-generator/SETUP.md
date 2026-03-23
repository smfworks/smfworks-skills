# QR Generator — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Free — no subscription, no API keys required

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| pip | Python package manager | Free |
| qrcode[pil] | Python QR code library + image support | Free |
| smfworks-skills repository | Cloned via git | Free |

---

## Step 1 — Verify Python and pip

```bash
python3 --version
pip --version
```

Expected:
```
Python 3.11.4
pip 23.1.2 from /usr/local/lib/python3.11/...
```

---

## Step 2 — Install the qrcode Package

```bash
pip install "qrcode[pil]"
```

Expected output:
```
Collecting qrcode[pil]
  Downloading qrcode-7.4.2-py3-none-any.whl (46 kB)
Collecting Pillow>=9.1.0
  Downloading Pillow-10.1.0-cp311-cp311-manylinux...
Installing collected packages: Pillow, qrcode
Successfully installed Pillow-10.1.0 qrcode-7.4.2
```

The `[pil]` part tells pip to also install Pillow (image library) needed for PNG output.

---

## Step 3 — Get the Skills Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 4 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/qr-generator
ls
```

Expected:
```
HOWTO.md   README.md   SETUP.md   main.py
```

---

## Step 5 — Verify the Skill

```bash
python3 main.py
```

Expected:
```
Usage: python main.py <command> [options]

Commands:
  url <url> [output.png]              - Generate URL QR code
  wifi <ssid> <password> [output.png]  - Generate WiFi QR code
  email <email> [output.png]          - Generate email QR code
  phone <number> [output.png]        - Generate phone QR code
  vcard <name> <phone> [email] [output.png] - Generate vCard
  sms <number> [message] [output.png] - Generate SMS QR
```

---

## Verify Your Setup

Generate a test QR code:

```bash
python3 main.py url https://smfworks.com test-qr.png
```

Expected:
```
✅ QR code generated: test-qr.png
   Data: https://smfworks.com
   Size: 25x25
```

Open `test-qr.png` and scan it with your phone. It should open `https://smfworks.com`.

Clean up:
```bash
rm test-qr.png
```

---

## Configuration Options

No configuration file or environment variables needed. All options are passed as arguments.

---

## Troubleshooting

**`qrcode not installed. Run: pip install qrcode[pil]`**  
Run `pip install "qrcode[pil]"` (use quotes around the package name in some shells).

**`ModuleNotFoundError: No module named 'PIL'`**  
Pillow wasn't installed. Run `pip install Pillow`.

**`pip: command not found`**  
Try `pip3` or `python3 -m pip install "qrcode[pil]"`.

---

## Next Steps

Setup complete. See **HOWTO.md** for walkthroughs on generating WiFi QR codes, vCards, URL codes, and scheduling with cron.
