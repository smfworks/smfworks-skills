# Database Backup

> Automated backups for SQLite, PostgreSQL, and MySQL databases with compression and restore

---

## What It Does

Database Backup handles automated backups for all your databases — SQLite, PostgreSQL, and MySQL. It compresses backups to save space, keeps a history of backups, and lets you restore with a single command when things go wrong.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Pro tier:**
```bash
smfw install database-backup
smf login
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Start an interactive backup session:

```bash
python main.py backup
```

---

## Commands

### `backup`

**What it does:** Launch interactive wizard to back up any supported database.

**Usage:**
```bash
python main.py backup
```

**Example:**
```bash
python main.py backup

# Example session:
# Select database type: 1 (SQLite)
# SQLite database file path: ~/myapp.db
# Backup destination: ~/backups/

# Or PostgreSQL:
# Select database type: 2 (PostgreSQL)
# Host: localhost
# Port: 5432
# Database name: myapp
# Username: postgres
# Password: env:DB_PASSWORD
```

**Output:**
```
✅ Backup complete!
   File: ~/.smf/backups/myapp-20260320-143052.sqlite.sql.gz
   Size: 2.3 MB
   Compression: 75%
```

---

### `list`

**What it does:** Display all existing backups with size and date.

**Usage:**
```bash
python main.py list
```

**Example:**
```bash
python main.py list
```

**Output:**
```
💾 5 Backup(s)
--------------------------------------------------------------------------------
Name                                               Size       Date
--------------------------------------------------------------------------------
myapp-20260320-143052.sqlite.sql.gz              2.3 MB     2026-03-20 14:30:52
myapp-20260319-120000.sqlite.sql.gz              2.1 MB     2026-03-19 12:00:00
postgres-prod-20260318-080000.postgres.sql.gz    45.7 MB    2026-03-18 08:00:00
```

---

### `stats`

**What it does:** Show backup statistics and storage usage.

**Usage:**
```bash
python main.py stats
```

**Example:**
```bash
python main.py stats
```

**Output:**
```
📊 Backup Statistics
========================================
Total backups: 15
Total size: 128.5 MB
Backup location: ~/.smf/backups

Backups by database:
  myapp: 10 backup(s)
  postgres-prod: 5 backup(s)
```

---

### `restore`

**What it does:** Restore a database from a compressed backup file.

**Usage:**
```bash
python main.py restore [backup-file]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `backup-file` | ✅ Yes | Path to backup file | `~/backups/myapp-20260320.sqlite.sql.gz` |

**Example:**
```bash
python main.py restore ~/.smf/backups/myapp-20260320-143052.sqlite.sql.gz
```

**Output:**
```
⚠️  This will overwrite: ~/myapp.db
Are you sure? (yes/no): yes
✅ Restored successfully!
```

---

### `cleanup`

**What it does:** Remove backups older than specified days.

**Usage:**
```bash
python main.py cleanup [days]
```

**Arguments:**

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `days` | ❌ No | Remove backups older than N days | `30` |

**Example:**
```bash
python main.py cleanup
python main.py cleanup 7
```

---

## Use Cases

- **Daily backups:** Schedule automatic daily backups via cron
- **Before updates:** Create a backup before updating your application
- **Migration:** Back up a database before moving to a new server
- **Disaster recovery:** Restore from backup when things go wrong
- **Audit trail:** Keep point-in-time backups for compliance

---

## Tips & Tricks

- Use `env:VARNAME` for passwords to avoid storing them in plain text
- Backups are automatically compressed (70-90% size reduction typical)
- Set up cron for hands-free daily backups: `0 2 * * * smf run database-backup backup`
- Store backups on a different drive than your database for true disaster recovery
- Use `stats` to monitor your backup storage usage

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "pg_dump not found" | Install PostgreSQL client: `sudo apt install postgresql-client` |
| "mysqldump not found" | Install MySQL client: `sudo apt install mysql-client` |
| "Authentication failed" | Check password or use `env:VARNAME` syntax |
| Permission denied | Ensure backup directory is writable: `chmod 700 ~/.smf/backups` |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- (Optional) `sqlite3` command for SQLite verification
- (Optional) `pg_dump` for PostgreSQL backups
- (Optional) `mysqldump` for MySQL backups

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/database-backup)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
