# Database Backup

Automated database backups for SQLite, PostgreSQL, and MySQL. Compress, encrypt, and manage backups with ease.

## Features

- ✅ **SQLite** — Native .dump with gzip compression
- ✅ **PostgreSQL** — pg_dump integration
- ✅ **MySQL** — mysqldump integration
- ✅ **Compression** — Automatic gzip compression
- ✅ **List & Manage** — View all backups, sizes, dates
- ✅ **Restore** — Restore from backup (SQLite)
- ✅ **Cleanup** — Auto-remove old backups
- ✅ **Local Storage** — Backups stay on your machine

## Installation

```bash
# Install SMF CLI (if not already)
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash

# Login (Pro skill requires subscription)
smf login

# Install the skill
smf install database-backup
```

## Usage

### Interactive Backup

```bash
smf run database-backup backup
```

This launches an interactive wizard:
1. Select database type (SQLite/PostgreSQL/MySQL)
2. Enter connection details
3. Choose backup destination
4. Done!

### SQLite Backup

```bash
# Interactive
smf run database-backup backup

# Example flow:
# Select database type: 1 (SQLite)
# SQLite database file path: ~/myapp.db
# Backup destination: ~/backups/
```

### PostgreSQL Backup

```bash
# Interactive
smf run database-backup backup

# Example flow:
# Select database type: 2 (PostgreSQL)
# Host: localhost
# Port: 5432
# Database name: myapp
# Username: postgres
# Password: *****
# Backup destination: ~/backups/
```

### MySQL Backup

```bash
# Interactive
smf run database-backup backup

# Example flow:
# Select database type: 3 (MySQL)
# Host: localhost
# Port: 3306
# Database name: myapp
# Username: root
# Password: *****
# Backup destination: ~/backups/
```

### List Backups

```bash
smf run database-backup list
```

Output:
```
💾 5 Backup(s)
--------------------------------------------------------------------------------
Name                                               Size       Date
--------------------------------------------------------------------------------
myapp-20260320-143052.sqlite.sql.gz              2.3 MB     2026-03-20 14:30:52
myapp-20260319-120000.sqlite.sql.gz              2.1 MB     2026-03-19 12:00:00
postgres-prod-20260318-080000.postgres.sql.gz    45.7 MB    2026-03-18 08:00:00
```

### Show Statistics

```bash
smf run database-backup stats
```

Output:
```
📊 Backup Statistics
========================================
Total backups: 15
Total size: 128.5 MB
Backup location: /home/user/.smf/backups

Backups by database:
  myapp: 10 backup(s)
  postgres-prod: 5 backup(s)
```

### Restore Backup (SQLite)

```bash
smf run database-backup restore ~/backups/myapp-20260320-143052.sqlite.sql.gz

# Enter target file when prompted
# Target database file: ~/myapp-restored.db
# Confirm: yes
```

### Cleanup Old Backups

```bash
# Remove backups older than 30 days (default)
smf run database-backup cleanup

# Remove backups older than 7 days
smf run database-backup cleanup 7
```

## Backup Location

By default, backups are stored in:
```
~/.smf/backups/
```

Each backup is named:
```
{database-name}-{timestamp}.{db-type}.sql.gz

Examples:
  myapp-20260320-143052.sqlite.sql.gz
  production-20260320-120000.postgres.sql.gz
  wordpress-20260319-080000.mysql.sql.gz
```

## Compression

All backups are automatically gzip compressed:
- Typical compression: 70-90% for text-heavy databases
- Compression ratio shown after backup
- Transparent decompression on restore

## Automated Backups

### Using Cron (Linux/macOS)

```bash
# Edit crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * smf run database-backup backup < ~/backups/answers.txt

# Or with specific config
0 2 * * * cd ~/ && smf run database-backup backup
```

### Using Systemd Timer (Linux)

Create `~/.config/systemd/user/smf-backup.service`:
```ini
[Unit]
Description=SMF Database Backup

[Service]
Type=oneshot
ExecStart=/home/user/.local/bin/smf run database-backup backup
```

Create `~/.config/systemd/user/smf-backup.timer`:
```ini
[Unit]
Description=Daily Database Backup

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

Enable:
```bash
systemctl --user enable smf-backup.timer
systemctl --user start smf-backup.timer
```

## Requirements

### SQLite
- `sqlite3` command line tool
- Usually pre-installed on most systems

### PostgreSQL
- `pg_dump` command line tool
- Install: `sudo apt install postgresql-client` (Ubuntu/Debian)
- Install: `brew install libpq` (macOS)

### MySQL
- `mysqldump` command line tool
- Install: `sudo apt install mysql-client` (Ubuntu/Debian)
- Install: `brew install mysql` (macOS)

## Backup Security

- **Local only:** Backups never leave your machine
- **Permissions:** Backup files created with 0600 (user-only)
- **Compression:** Reduces exposure of raw SQL
- **No cloud:** No automatic cloud upload (you control this)

## Offsite Backup (Optional)

To sync backups to cloud storage:

```bash
# Sync to S3 (requires awscli)
aws s3 sync ~/.smf/backups/ s3://my-backup-bucket/

# Sync to Google Drive (requires rclone)
rclone sync ~/.smf/backups/ gdrive:backups/

# Sync to Dropbox (requires dropbox-uploader)
~/dropbox_uploader.sh upload ~/.smf/backups/* /
```

## Troubleshooting

### "pg_dump: command not found"
Install PostgreSQL client tools:
```bash
# Ubuntu/Debian
sudo apt install postgresql-client

# macOS
brew install libpq
brew link --force libpq

# Add to PATH
echo 'export PATH="/usr/local/opt/libpq/bin:$PATH"' >> ~/.zshrc
```

### "mysqldump: command not found"
Install MySQL client:
```bash
# Ubuntu/Debian
sudo apt install mysql-client

# macOS
brew install mysql
```

### "Permission denied" on backup
Check directory permissions:
```bash
chmod 700 ~/.smf
chmod 700 ~/.smf/backups
```

### Large database backups fail
For very large databases, consider:
- Splitting into smaller chunks
- Using `pg_dump` with custom format: `pg_dump -Fc`
- Streaming to remote storage instead of local disk

## Pricing

**Database Backup is a premium SMF Works skill.**

This is a paid skill that is part of the SMF Works subscription service. One monthly fee for unlimited access to the growing library of premium SMF Skills and applications.

- **Price:** $19.99/month (locked forever at signup rate)
- **Includes:** All premium skills, updates, priority support
- **Free alternative:** Use native database tools or free skills

Subscribe at https://smf.works/subscribe

## See Also

- [SETUP.md](./SETUP.md) — Complete setup and configuration guide
- `smf help` — CLI documentation
- `smf status` — Check subscription status

## License

SMF Works Pro Skill — See SMF Works Terms of Service
