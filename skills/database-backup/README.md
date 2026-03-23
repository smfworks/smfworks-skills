# Database Backup

> Back up SQLite, MySQL, and PostgreSQL databases from the terminal — with a step-by-step interactive wizard, rolling retention, and restore support.

**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo at [smfworks.com/subscribe](https://smfworks.com/subscribe))  
**Version:** 1.0  
**Category:** Data / Backup

---

## What It Does

Database Backup is an OpenClaw Pro skill for creating, listing, and restoring database backups. It supports SQLite (file-based), MySQL/MariaDB, and PostgreSQL. An interactive wizard guides you through the backup process — just answer the prompts and your database is backed up safely.

Backups use the appropriate native tool for each database type: direct file copy for SQLite, `mysqldump` for MySQL, and `pg_dump` for PostgreSQL.

**What it does NOT do:** It does not back up to cloud storage, perform incremental backups (full dump each time), monitor database health, or support other database types (MongoDB, Redis, etc.).

---

## Prerequisites

- [ ] **SMF Works Pro subscription** — [smfworks.com/subscribe](https://smfworks.com/subscribe)
- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed and authenticated**
- [ ] **Database-specific tools:**
  - SQLite: No additional tools needed
  - MySQL: `mysqldump` installed
  - PostgreSQL: `pg_dump` installed

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/database-backup
python3 main.py
```

---

## Quick Start

Run an interactive backup:

```bash
python3 main.py backup
```

The wizard prompts:
```
Database type (sqlite/mysql/postgres): sqlite
Database file path: ~/data/myapp.db

✅ Backup created: myapp-2024-03-15-090001.db.gz
   Size: 2.4 MB
```

---

## Command Reference

### `backup`

Interactive backup wizard. Prompts for database type, connection details, and backup location.

```bash
python3 main.py backup
```

For SQLite:
```
Database type: sqlite
Database file: ~/data/myapp.db
→ Creates: ~/.smf/db-backups/myapp-2024-03-15.db.gz
```

For MySQL:
```
Database type: mysql
Host: localhost
Port: 3306
Username: myuser
Password: [prompted securely]
Database name: myapp_production
→ Creates: ~/.smf/db-backups/myapp_production-2024-03-15.sql.gz
```

For PostgreSQL:
```
Database type: postgres
Host: localhost
Port: 5432
Username: postgres
Database name: myapp
→ Creates: ~/.smf/db-backups/myapp-2024-03-15.sql.gz
```

---

### `list`

Lists all database backups with size, date, and database name.

```bash
python3 main.py list
```

Output:
```
📋 Database Backups (4 total):

1. myapp-2024-03-15-090001.db.gz — 2.4 MB — 2024-03-15 09:00
2. myapp-2024-03-14-090001.db.gz — 2.4 MB — 2024-03-14 09:00
3. production-2024-03-15-020001.sql.gz — 48.7 MB — 2024-03-15 02:00
4. production-2024-03-14-020001.sql.gz — 47.9 MB — 2024-03-14 02:00

Total: 4 backups, 101.4 MB
```

---

### `stats`

Shows backup statistics: total count, total size, last backup time, oldest backup.

```bash
python3 main.py stats
```

Output:
```
📊 Backup Statistics
─────────────────────
Total backups: 4
Total size: 101.4 MB
Last backup: 2024-03-15 09:00
Oldest backup: 2024-03-14 02:00
```

---

### `restore <file>`

Restores a database from a backup file. SQLite restore only (MySQL and PostgreSQL require manual import).

```bash
python3 main.py restore ~/.smf/db-backups/myapp-2024-03-14-090001.db.gz
```

Output:
```
🔄 Restoring backup: myapp-2024-03-14-090001.db.gz
   Target: ~/data/myapp.db
   Decompressing and restoring...

✅ Restore complete!
```

---

### `cleanup [days]`

Removes backups older than N days (default: 30 days).

```bash
python3 main.py cleanup 30
```

Output:
```
🧹 Removing backups older than 30 days...
✅ Removed 3 old backups (saved 148.2 MB)
```

---

## Use Cases

### 1. Daily database backup

Schedule via cron (see HOWTO.md for setup details).

### 2. Pre-migration backup

Always back up before schema changes or data migrations:

```bash
python3 main.py backup
# Then run your migration
```

### 3. Restore after accidental data deletion

```bash
python3 main.py list
python3 main.py restore /path/to/backup.db.gz
```

### 4. Audit backup history

```bash
python3 main.py stats
```

---

## Configuration

Backup storage: `~/.smf/db-backups/`  
No config file required — connection details are entered interactively during each backup run.

---

## Troubleshooting

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

### `mysqldump: command not found`
MySQL client tools not installed.  
**Fix:** `sudo apt install mysql-client` (Ubuntu) or `brew install mysql-client` (macOS).

### `pg_dump: command not found`
PostgreSQL client tools not installed.  
**Fix:** `sudo apt install postgresql-client` (Ubuntu) or `brew install postgresql` (macOS).

### `Access denied for user 'xxx'` (MySQL)
Wrong username or password.  
**Fix:** Verify credentials. Ensure the user has SELECT and LOCK TABLES privileges.

### Backup file is 0 bytes
The dump command failed silently.  
**Fix:** Run the backup again and check the output carefully. Verify database credentials and accessibility.

### `Error: File not found` for SQLite
Wrong file path for the SQLite database.  
**Fix:** Use the full absolute path: `/home/user/data/myapp.db`

---

## FAQ

**Q: Does it store my database credentials?**  
A: Credentials are entered interactively and not saved between runs. For automation, use environment variables (see HOWTO.md).

**Q: Can I restore MySQL/PostgreSQL backups?**  
A: CLI restore is only supported for SQLite. For MySQL: `gunzip -c backup.sql.gz | mysql -u user -p database`. For PostgreSQL: `gunzip -c backup.sql.gz | psql -U user database`

**Q: What's the compression ratio?**  
A: SQL dumps typically compress 5–10× with gzip. A 500 MB MySQL dump often produces a 50–100 MB `.sql.gz` file.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| SMF Works Pro | Required ($19.99/mo) |
| mysqldump | Required for MySQL backups |
| pg_dump | Required for PostgreSQL backups |
| External APIs | None |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/database-backup)
- 🔑 [Subscribe](https://smfworks.com/subscribe)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
