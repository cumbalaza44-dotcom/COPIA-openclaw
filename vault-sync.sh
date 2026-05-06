#!/bin/bash
# vault-sync.sh — Auto-sync vault + refresh index
# Uso: ./vault-sync.sh
# Se ejecuta automáticamente desde J.A.R.V.I.S. antes de cada interacción con el vault

OBSIDIAN_DIR="/root/.openclaw/workspace/obsidian-vault"
WORKSPACE_DIR="/root/.openclaw/workspace"

cd "$OBSIDIAN_DIR" || exit 1

# 1. Pull remoto
git pull --rebase origin main 2>&1

# 2. Reconstruir índice JSON (para JARVIS)
find . -not -path './.git/*' -not -path './.obsidian/*' -name '*.md' -printf '%P\n' | sort | while IFS= read -r f; do
  lines=$(wc -l < "$f")
  echo "{\"path\":\"$f\",\"lines\":$lines}"
done | jq -s '{updated: now | strftime("%Y-%m-%dT%H:%M:%S%z"), totalNotes: length, notes: .}' > "$WORKSPACE_DIR/vault-index.json"

echo "=== VAULT SYNC COMPLETE ==="
echo "Total notas: $(jq '.totalNotes' "$WORKSPACE_DIR/vault-index.json")"
