#!/bin/bash

# Simple and robust backup script

cd /root/.openclaw/workspace || exit 1

# Load SSH key if exists
if [ -f ~/.ssh/id_ed25519 ]; then
    ssh-add ~/.ssh/id_ed25519 2>/dev/null || true
fi

# Add files from known directories
git add prompts/*.md 2>/dev/null || true
git add skills/*.sh 2>/dev/null || true
git add tools/*.json 2>/dev/null || true
git add workflows/*.yaml 2>/dev/null || true
git add memory/*.md 2>/dev/null || true
git add *.md 2>/dev/null || true
git add *.json 2>/dev/null || true
git add *.sh 2>/dev/null || true
git add *.yaml 2>/dev/null || true

# Check if there are changes
if git diff --cached --quiet; then
    echo "$(date): No changes to backup" >> /var/log/openclaw-backup.log
    exit 0
fi

# Commit
git commit -m "Backup $(date +'%Y-%m-%d %H:%M')" 2>/dev/null || exit 1

# Push
git fetch origin 2>&1 >> /var/log/openclaw-backup.log
git push --force-with-lease origin HEAD:main 2>&1 >> /var/log/openclaw-backup.log || exit 1

echo "$(date): Backup completed successfully" >> /var/log/openclaw-backup.log
exit 0