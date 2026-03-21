# Database Backup - Setup & Configuration Guide

Complete setup instructions for installing, configuring, and using the Database Backup skill.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Authentication Setup](#authentication-setup)
4. [Database-Specific Setup](#database-specific-setup)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Automation](#automation)
8. [Troubleshooting](#troubleshooting)
9. [Security Best Practices](#security-best-practices)

---

## Prerequisites

### System Requirements
- **OS:** Linux, macOS, or Windows with Python
- **Python:** 3.8 or higher
- **Storage:** Space for backups (typically 2-5x database size)
- **Network:** Connection to database server (for PostgreSQL/MySQL)

### Required Tools

Depending on your database type, you need:

| Database | Required Tool | Install Command |
|----------|---------------|-----------------|
| SQLite | `sqlite3` | Usually pre-installed |
| PostgreSQL | `pg_dump` | `apt install postgresql-client` or `brew install libpq` |
| MySQL | `mysqldump` | `apt install mysql-client` or `brew install mysql` |

### SMF Works Subscription
- **Required:** SMF Works Pro subscription ($19.99/mo)
- **Sign up:** https://smf.works/subscribe

---

## Installation

### Step 1: Install SMF CLI

If you haven't already:

```bash
# One-liner install
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash

# Reload PATH
source ~/.bashrc  # or ~/.zshrc
```

### Step 2: Authenticate

```bash
# Login with your subscription
smf login

# Verify
smf status
```

Expected output:
```
🔐 SMF Works Status
----------------------------------------
✅ Subscription active
   Tier: pro
   Expires: 2027-03-20
```

### Step 3: Install Database Backup Skill

```bash
smf install database-backup
```

### Step 4: Verify Installation

```bash
smf run database-backup --help
```

Expected output:
```
Usage: smf run database-backup <command> [options]

Commands:
  backup              - Interactive backup wizard
  list                - List all backups
  stats               - Show backup statistics
  restore <file>      - Restore from backup
  cleanup [days]      - Remove old backups
```

---

## Authentication Setup

### Subscribe to SMF Works Pro

1. Visit https://smf.works/subscribe
2. Choose "Pro" plan ($19.99/mo)
3. Complete checkout via Stripe
4. Get your API token from the dashboard

### Authenticate CLI

```bash
smf login

# Paste your token when prompted
# Token saved to ~/.smf/token
```

### Verify Authentication

```bash
smf status
```

If you see "Subscription active", you're ready!

---

## Database-Specific Setup

### SQLite Setup

**No additional setup required!** SQLite is file-based.

Just know your database file path:
```bash
# Common locations
~/myapp.db
~/projects/myapp/database.sqlite3
/var/lib/app/data.db
```

### PostgreSQL Setup

#### Install pg_dump

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql-client
```

**macOS:**
```bash
brew install libpq
brew link --force libpq

# Add to PATH
echo 'export PATH="/usr/local/opt/libpq/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Verify:**
```bash
pg_dump --version
```

#### Database Connection Info

Gather these details:
- **Host:** Usually `localhost` or IP address
- **Port:** Usually `5432`
- **Database name:** The database to backup
- **Username:** PostgreSQL username
- **Password:** PostgreSQL password

**Example:**
```
Host: localhost
Port: 5432
Database: myapp_production
Username: postgres
Password: ********
```

### MySQL Setup

#### Install mysqldump

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-client
```

**macOS:**
```bash
brew install mysql
```

**Verify:**
```bash
mysqldump --version
```

#### Database Connection Info

Gather these details:
- **Host:** Usually `localhost` or IP address
- **Port:** Usually `3306`
- **Database name:** The database to backup
- **Username:** MySQL username (often `root`)
- **Password:** MySQL password

**Example:**
```
Host: localhost
Port: 3306
Database: wordpress_db
Username: root
Password: ********
```

---

## Configuration

### Backup Directory

Default backup location:
```
~/.smf/backups/
```

To change, you can specify during backup or symlink:
```bash
# Create symlink to external drive
ln -s /mnt/external/backups ~/.smf/backups
```

### Permission Setup

Ensure proper permissions:
```bash
# Create directories with secure permissions
mkdir -p ~/.smf/backups
chmod 700 ~/.smf
chmod 700 ~/.smf/backups

# Verify
drwx------  user user  .smf
drwx------  user user  backups
```

### Database Credentials

For security, credentials are entered interactively and not stored.

For automation, you can use environment variables:

```bash
# PostgreSQL
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=myapp
export PGUSER=postgres
export PGPASSWORD=secret

# MySQL
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_DATABASE=myapp
export MYSQL_USER=root
export MYSQL_PASSWORD=secret
```

---

## Usage

### Creating Your First Backup

**Interactive Mode (Recommended):**
```bash
smf run database-backup backup
```

Follow the prompts:
1. Select database type (1=SQLite, 2=PostgreSQL, 3=MySQL)
2. Enter connection details
3. Choose backup destination (or press Enter for default)
4. Done!

**Example - SQLite:**
```
💾 Database Backup
========================================

Select database type:
  1. SQLite
  2. PostgreSQL
  3. MySQL

Choice (1-3): 1

SQLite database file path: ~/myapp.db
Backup destination directory [~/smf/backups]:

✅ Backup complete!
   File: /home/user/.smf/backups/myapp-20260320-143052.sqlite.sql.gz
   Size: 2.3 MB
   Compression: 78.5%
```

### Listing Backups

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
production-20260318-080000.postgres.sql.gz       45.7 MB    2026-03-18 08:00:00
```

### Viewing Statistics

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
  production: 5 backup(s)
```

### Restoring a Backup

**SQLite Only:**
```bash
smf run database-backup restore ~/backups/myapp-20260320-143052.sqlite.sql.gz

# Enter when prompted:
# Target database file: ~/myapp-restored.db
# Are you sure? (yes/no): yes

# Output:
✅ Restored to /home/user/myapp-restored.db
```

### Cleaning Up Old Backups

```bash
# Remove backups older than 30 days (default)
smf run database-backup cleanup

# Remove backups older than 7 days
smf run database-backup cleanup 7

# Output:
✅ Removed 12 backup(s)
   Freed 245.6 MB
```

---

## Automation

### Automated Daily Backups

**Using Cron (Linux/macOS):**

Create backup script `~/backup-script.sh`:
```bash
#!/bin/bash
# Daily database backup
export PATH="$HOME/.local/bin:$PATH"

cd ~
echo "1" > /tmp/db-type.txt      # 1=SQLite
echo "$HOME/myapp.db" >> /tmp/db-type.txt
echo "" >> /tmp/db-type.txt        # Default destination

smf run database-backup backup < /tmp/db-type.txt
```

Make executable:
```bash
chmod +x ~/backup-script.sh
```

Add to crontab:
```bash
crontab -e
```

Add line for daily 2 AM backup:
```
0 2 * * * /home/user/backup-script.sh >> /home/user/.smf/backup.log 2>&1
```

**Verify cron is working:**
```bash
# Check crontab
crontab -l

# View backup log
tail -f ~/.smf/backup.log
```

### Systemd Timer (Linux)

**Create service file** `~/.config/systemd/user/smf-backup.service`:
```ini
[Unit]
Description=SMF Database Backup

[Service]
Type=oneshot
ExecStart=/home/user/.local/bin/smf run database-backup backup
StandardOutput=append:/home/user/.smf/backup.log
StandardError=append:/home/user/.smf/backup.log
```

**Create timer file** `~/.config/systemd/user/smf-backup.timer`:
```ini
[Unit]
Description=Daily Database Backup at 2 AM

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

**Enable and start:**
```bash
# Reload systemd
systemctl --user daemon-reload

# Enable timer
systemctl --user enable smf-backup.timer

# Start timer
systemctl --user start smf-backup.timer

# Check status
systemctl --user status smf-backup.timer

# View next run
systemctl --user list-timers
```

### Offsite Backup Sync

**Sync to S3:**
```bash
# Install awscli
pip install awscli

# Configure
aws configure

# Create sync script
cat > ~/sync-to-s3.sh << 'EOF'
#!/bin/bash
aws s3 sync ~/.smf/backups/ s3://my-backup-bucket/databases/
EOF

chmod +x ~/sync-to-s3.sh

# Add to cron (runs after backup)
0 3 * * * /home/user/sync-to-s3.sh
```

**Sync to Google Drive:**
```bash
# Install rclone
# https://rclone.org/install/

# Configure
cat > ~/.config/rclone/rclone.conf << 'EOF'
[gdrive]
type = drive
client_id = 
client_secret =
token =
EOF

# Sync
rclone sync ~/.smf/backups/ gdrive:Backups/Databases/
```

---

## Troubleshooting

### "Command not found: smf"

**Problem:** SMF CLI not in PATH

**Solution:**
```bash
# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Make permanent
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### "pg_dump: command not found"

**Problem:** PostgreSQL client tools not installed

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install postgresql-client

# macOS
brew install libpq
brew link --force libpq
```

### "mysqldump: command not found"

**Problem:** MySQL client tools not installed

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install mysql-client

# macOS
brew install mysql
```

### "Permission denied" on backup

**Problem:** Insufficient permissions on backup directory

**Solution:**
```bash
# Fix permissions
chmod 700 ~/.smf
chmod 700 ~/.smf/backups

# Verify
ls -la ~/.smf/
```

### "No subscription token found"

**Problem:** Not authenticated

**Solution:**
```bash
smf login
```

### Large database backup fails

**Problem:** Database too large for available disk space

**Solutions:**
1. Check available space: `df -h ~/.smf/backups`
2. Backup to external drive: `smf run database-backup backup` and specify external path
3. Use streaming backup to remote storage

### Backup is very slow

**Problem:** Large database or slow connection

**Solutions:**
1. For PostgreSQL: Use connection pooling
2. Backup during low-traffic hours
3. Consider incremental backups (future feature)
4. Compress after backup: Already done automatically

### "pg_dump: [archiver] connection to server failed"

**Problem:** Cannot connect to PostgreSQL server

**Solutions:**
1. Verify server is running: `sudo service postgresql status`
2. Check firewall rules
3. Verify connection details (host, port, credentials)
4. Test connection: `psql -h localhost -U postgres -d mydb`

---

## Security Best Practices

### 1. Secure Backup Storage

```bash
# Set restrictive permissions
chmod 700 ~/.smf
chmod 700 ~/.smf/backups

# Verify
ls -la ~/.smf/
# Should show: drwx------
```

### 2. Encrypt Sensitive Backups

For extra security, encrypt backups:
```bash
# Install gpg if needed
# Encrypt backup
gpg --symmetric --cipher-algo AES256 ~/.smf/backups/myapp-*.sql.gz

# Decrypt
gpg --decrypt myapp-*.sql.gz.gpg > backup.sql.gz
```

### 3. Use Environment Variables for Credentials

Never hardcode credentials:
```bash
# Good
export PGPASSWORD="secret"
smf run database-backup backup

# Bad
echo "password: secret" >> script.sh
```

### 4. Backup to Encrypted Storage

```bash
# Encrypt home directory (Ubuntu)
sudo apt install ecryptfs-utils
ecryptfs-setup-private

# Or use encrypted external drive
sudo cryptsetup luksFormat /dev/sdb1
sudo cryptsetup open /dev/sdb1 backup-drive
```

### 5. Regular Security Audit

```bash
# Check backup permissions
find ~/.smf/backups -type f -ls

# Should show: -rw------- (owner only)

# Check for old backups
find ~/.smf/backups -mtime +30 -ls

# Secure delete if needed
shred -u ~/.smf/backups/old-backup.sql.gz
```

### 6. Test Restores Regularly

```bash
# Monthly restore test
smf run database-backup restore ~/backups/latest.sql.gz
```

---

## Next Steps

1. **Verify setup:** Run your first backup
2. **Test restore:** Ensure you can recover data
3. **Automate:** Set up daily backups
4. **Monitor:** Check backup logs regularly
5. **Secure:** Implement encryption if needed

---

## Support

- **Documentation:** https://github.com/smfworks/smfworks-skills
- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **Email:** support@smf.works

---

*Last updated: March 20, 2026*
