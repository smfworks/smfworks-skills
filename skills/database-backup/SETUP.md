# Database Backup — Setup Guide

**Estimated setup time:** 10–15 minutes  
**Difficulty:** Easy to Moderate  
**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo)

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| SMF Works Pro subscription | [smfworks.com/subscribe](https://smfworks.com/subscribe) | $19.99/mo |
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| OpenClaw | Installed and authenticated | Free |
| smfworks-skills repository | Cloned via git | Included |
| **For MySQL:** mysqldump | MySQL client tools | Free |
| **For PostgreSQL:** pg_dump | PostgreSQL client tools | Free |
| **For SQLite:** nothing extra | Already in Python | Free |

---

## Step 1 — Subscribe and Authenticate

Visit [smfworks.com/subscribe](https://smfworks.com/subscribe).

```bash
openclaw auth status
```

---

## Step 2 — Install Database Client Tools (if needed)

**For MySQL/MariaDB backups:**
```bash
# Ubuntu/Debian:
sudo apt install mysql-client

# macOS:
brew install mysql-client
```

**For PostgreSQL backups:**
```bash
# Ubuntu/Debian:
sudo apt install postgresql-client

# macOS:
brew install postgresql
```

**For SQLite:** No additional tools needed.

---

## Step 3 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 4 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/database-backup
```

---

## Step 5 — Verify

```bash
python3 main.py
```

Expected:
```
Usage: python main.py <command> [options]

Commands:
  backup              - Interactive backup wizard
  list                - List all backups
  stats               - Show backup statistics
  restore <file>      - Restore from backup (SQLite only)
  cleanup [days]      - Remove old backups (default: 30 days)
```

---

## Verify Your Setup

Run a test backup of a SQLite database. If you have one:

```bash
python3 main.py backup
# Choose: sqlite
# Path: /path/to/your/database.db
```

Or create a test SQLite database:
```bash
python3 -c "import sqlite3; conn=sqlite3.connect('/tmp/test.db'); conn.execute('CREATE TABLE t(id int)'); conn.close()"
python3 main.py backup
# sqlite, /tmp/test.db
```

Expected: Success message with backup file path and size.

---

## Configuration for Automation

For cron automation, set database credentials as environment variables instead of entering them interactively:

**MySQL:**
```bash
export MYSQL_HOST=localhost
export MYSQL_USER=myuser
export MYSQL_PASS=mypassword
export MYSQL_DB=mydatabase
```

**PostgreSQL:**
```bash
export PGHOST=localhost
export PGUSER=postgres
export PGPASSWORD=mypassword
export PGDATABASE=mydatabase
```

Add these to `~/.bashrc` or use a secure env file in your cron setup.

---

## Troubleshooting

**`Error: SMF Works Pro subscription required`** — Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

**`mysqldump: command not found`** — Install MySQL client: `sudo apt install mysql-client` or `brew install mysql-client`.

**`pg_dump: command not found`** — Install PostgreSQL client: `sudo apt install postgresql-client` or `brew install postgresql`.

---

## Next Steps

Setup complete. See **HOWTO.md** for backup walkthroughs, restore procedures, and cron automation.
