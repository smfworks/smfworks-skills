# Database Backup — How-To Guide

**Prerequisites:** SMF Works Pro subscription active. Database client tools installed (if using MySQL/PostgreSQL). Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Back Up a SQLite Database](#1-how-to-back-up-a-sqlite-database)
2. [How to Back Up a MySQL Database](#2-how-to-back-up-a-mysql-database)
3. [How to Back Up a PostgreSQL Database](#3-how-to-back-up-a-postgresql-database)
4. [How to Restore a SQLite Backup](#4-how-to-restore-a-sqlite-backup)
5. [How to List and Clean Up Backups](#5-how-to-list-and-clean-up-backups)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Back Up a SQLite Database

**When to use it:** Your app uses a local SQLite database file that needs regular backup.

### Steps

**Step 1 — Navigate to the skill.**

```bash
cd ~/smfworks-skills/skills/database-backup
```

**Step 2 — Run the backup wizard.**

```bash
python3 main.py backup
```

```
Database type (sqlite/mysql/postgres): sqlite
Database file path: /home/user/myapp/data/app.db

💾 Creating backup...
✅ Backup created: app-2024-03-15-090001.db.gz
   Size: 2.4 MB
   Location: ~/.smf/db-backups/app-2024-03-15-090001.db.gz
```

**Result:** Your SQLite database is safely backed up and compressed.

---

## 2. How to Back Up a MySQL Database

**When to use it:** Your WordPress, app, or web service uses MySQL or MariaDB.

### Steps

**Step 1 — Run the backup wizard.**

```bash
python3 main.py backup
```

```
Database type: mysql
Host [localhost]: localhost
Port [3306]: 3306
Username: myuser
Password: [type password, hidden]
Database name: myapp_production

💾 Running mysqldump...
✅ Backup created: myapp_production-2024-03-15-020001.sql.gz
   Size: 48.7 MB
```

**Result:** A compressed SQL dump of your entire MySQL database.

---

## 3. How to Back Up a PostgreSQL Database

**When to use it:** Your application uses PostgreSQL.

### Steps

**Step 1 — Run the backup wizard.**

```bash
python3 main.py backup
```

```
Database type: postgres
Host [localhost]: localhost
Port [5432]: 5432
Username: postgres
Database name: myapp

💾 Running pg_dump...
✅ Backup created: myapp-2024-03-15-020001.sql.gz
   Size: 34.2 MB
```

---

## 4. How to Restore a SQLite Backup

**When to use it:** After data loss, corruption, or accidental deletion.

### Steps

**Step 1 — List available backups.**

```bash
python3 main.py list
```

```
📋 Database Backups (4 total):

1. app-2024-03-15-090001.db.gz — 2.4 MB — 2024-03-15 09:00
2. app-2024-03-14-090001.db.gz — 2.4 MB — 2024-03-14 09:00
```

**Step 2 — Restore the desired backup.**

```bash
python3 main.py restore ~/.smf/db-backups/app-2024-03-14-090001.db.gz
```

Output:
```
🔄 Restoring backup: app-2024-03-14-090001.db.gz
✅ Restore complete!
```

**For MySQL/PostgreSQL restore** (manual process):

```bash
# MySQL:
gunzip -c backup.sql.gz | mysql -u myuser -p myapp_production

# PostgreSQL:
gunzip -c backup.sql.gz | psql -U postgres myapp
```

---

## 5. How to List and Clean Up Backups

**List all backups:**

```bash
python3 main.py list
```

**View statistics:**

```bash
python3 main.py stats
```

**Remove backups older than 30 days:**

```bash
python3 main.py cleanup 30
```

**Remove backups older than 7 days:**

```bash
python3 main.py cleanup 7
```

---

## 6. Automating with Cron

### Open crontab

```bash
crontab -e
```

### Example: Daily MySQL backup at 2 AM using environment variables

First, create a secure env file:
```bash
cat > ~/.smf/db-backup.env << 'EOF'
export MYSQL_HOST=localhost
export MYSQL_USER=myuser
export MYSQL_PASS=mypassword
export MYSQL_DB=myapp_production
EOF
chmod 600 ~/.smf/db-backup.env
```

Then in crontab:
```bash
0 2 * * * source /home/yourname/.smf/db-backup.env && python3 /home/yourname/smfworks-skills/skills/database-backup/main.py backup >> /home/yourname/logs/db-backup.log 2>&1
```

### Example: Weekly cleanup of old backups

```bash
0 3 * * 0 python3 /home/yourname/smfworks-skills/skills/database-backup/main.py cleanup 30 >> /home/yourname/logs/db-backup.log 2>&1
```

---

## 7. Combining with Other Skills

**Database Backup + Claw System Backup:** Combined protection strategy:

```bash
# Back up database AND system
python3 ~/smfworks-skills/skills/database-backup/main.py backup
python3 ~/smfworks-skills/skills/claw-system-backup/main.py
```

**Database Backup + System Monitor:** Check disk before backing up large databases:

```bash
python3 ~/smfworks-skills/skills/system-monitor/main.py disk
python3 ~/smfworks-skills/skills/database-backup/main.py backup
```

---

## 8. Troubleshooting Common Issues

### `mysqldump: command not found`

**Fix:** Install MySQL client tools:
```bash
sudo apt install mysql-client   # Ubuntu/Debian
brew install mysql-client       # macOS
```

### `Access denied for user 'xxx'@'localhost'`

Wrong credentials or insufficient privileges.  
**Fix:** Verify credentials. Grant necessary privileges: `GRANT SELECT, LOCK TABLES ON mydb.* TO 'myuser'@'localhost';`

### Backup file is 0 bytes or empty

The dump command failed.  
**Fix:** Test your credentials manually: `mysqldump -u myuser -p myapp_production --no-data 2>&1` — this shows any errors.

### `pg_dump: error: FATAL: password authentication failed`

Wrong PostgreSQL password.  
**Fix:** Check your password. PostgreSQL also accepts a `.pgpass` file for automation: `echo "localhost:5432:mydb:myuser:mypassword" > ~/.pgpass && chmod 600 ~/.pgpass`

---

## 9. Tips & Best Practices

**Back up before any schema changes or data migrations.** Always create a fresh backup immediately before running any `ALTER TABLE`, data import, or migration script. This is your rollback point.

**Store database credentials securely.** Never put plaintext passwords in cron jobs. Use environment variables or a `.pgpass`/`.my.cnf` file with restricted permissions (600).

**Test restores periodically.** A backup you've never restored from is an untested backup. Restore a copy to a test location quarterly to confirm the backup is actually usable.

**Set cleanup intervals based on your change rate.** A database that changes hourly needs more recent backups. A database that changes weekly can use 30-day retention. Set cleanup days accordingly.

**Compress before storing.** The skill compresses with gzip automatically. SQL dumps compress 5–10× typically, so a 500 MB dump becomes ~50 MB.
