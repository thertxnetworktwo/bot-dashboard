#!/bin/bash

# Database Backup Script
# This script creates automated backups of the PostgreSQL database

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$PROJECT_DIR/backups"
LOG_FILE="$PROJECT_DIR/backend/logs/backup.log"

# Load environment variables
if [ -f "$PROJECT_DIR/backend/.env" ]; then
    export $(cat "$PROJECT_DIR/backend/.env" | grep -v '^#' | xargs)
fi

DB_NAME="${DB_NAME:-dashboard_db}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Log start
echo "[$(date)] Starting backup..." >> "$LOG_FILE"

# Create backup
sudo -u postgres pg_dump $DB_NAME > "$BACKUP_FILE"

# Compress backup
gzip "$BACKUP_FILE"

# Log completion
echo "[$(date)] Backup completed: ${BACKUP_FILE}.gz" >> "$LOG_FILE"

# Remove backups older than 7 days
find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +7 -delete

echo "[$(date)] Old backups cleaned up" >> "$LOG_FILE"
echo "Backup completed successfully: ${BACKUP_FILE}.gz"
