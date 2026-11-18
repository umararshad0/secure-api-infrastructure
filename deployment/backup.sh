
#!/bin/bash
set -euo pipefail

umask 077

PROJECT_DIR="$HOME/secure-api-infrastructure"
BACKUP_DIR="$HOME/backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="$BACKUP_DIR/secure-api-backup-$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"
chmod 700 "$BACKUP_DIR"

echo "Starting backup..."

tar -czf "$BACKUP_FILE" \
    --exclude='.venv' \
    --exclude='.git' \
    --exclude='.pytest_cache' \
    --exclude='__pycache__' \
    -C "$PROJECT_DIR" .

tar -tzf "$BACKUP_FILE" > /dev/null
chmod 600 "$BACKUP_FILE"

echo "Backup verified: $BACKUP_FILE"

# Keep the 7 most recent backups
ls -1t "$BACKUP_DIR"/secure-api-backup-*.tar.gz 2>/dev/null \
    | tail -n +8 \
    | while IFS= read -r old_backup; do
        rm -f -- "$old_backup"
      done

echo "Backup completed successfully."
