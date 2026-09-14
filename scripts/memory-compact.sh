#!/bin/bash
# memory-compact.sh — P2 two-zone: cap mecánico ## Live a 40 líneas
# Cero LLM, puro texto. Corre diario 04:35 por cron comando.
# Si ## Live > 40 líneas, mueve las más viejas a ## Archived del mismo archivo.
# NO toca MEMORY.md (eso es decisión semántica, la hace H.E.L.E.N. en turno main).

MEMORY_DIR="/root/.openclaw/workspace/memory"
MAX_LIVE=40

compact_file() {
    local f="$1"
    # Solo archivos con sección ## Live
    if ! grep -q "^## Live" "$f" 2>/dev/null; then
        return 0
    fi

    # Extraer líneas bajo ## Live (hasta próximo ## o fin)
    local live_lines
    live_lines=$(awk '/^## Live/{flag=1;next}/^## /{flag=0}flag' "$f" | grep -c "^- " 2>/dev/null)
    live_lines=${live_lines:-0}

    if [ "$live_lines" -le "$MAX_LIVE" ]; then
        return 0
    fi

    local excess=$((live_lines - MAX_LIVE))

    # Líneas a mover (las más viejas = primeras)
    local to_move
    to_move=$(awk '/^## Live/{flag=1;next}/^## /{flag=0}flag' "$f" | grep "^- " | head -n "$excess")

    # Remover esas líneas de ## Live
    local tmp=$(mktemp)
    local moved=0
    while IFS= read -r line; do
        if echo "$to_move" | grep -qxF "$line" && [ "$moved" -lt "$excess" ]; then
            moved=$((moved + 1))
            continue
        fi
        echo "$line"
    done < "$f" > "$tmp"

    # Agregar sección ## Archived si no existe, append bullets
    if ! grep -q "^## Archived" "$tmp"; then
        echo "" >> "$tmp"
        echo "## Archived" >> "$tmp"
    fi
    # Insertar bullets movidos bajo ## Archived
    local tmp2=$(mktemp)
    local inserted=0
    while IFS= read -r line; do
        echo "$line" >> "$tmp2"
        if [ "$inserted" -eq 0 ] && echo "$line" | grep -q "^## Archived"; then
            echo "$to_move" >> "$tmp2"
            inserted=1
        fi
    done < "$tmp"
    mv "$tmp2" "$f"
    rm -f "$tmp"

    echo "COMPACTED $(basename "$f"): $live_lines → $MAX_LIVE live ($excess → Archived)"
}

for f in "$MEMORY_DIR"/2026-*.md; do
    [ -f "$f" ] && compact_file "$f"
done

echo "=== MEMORY COMPACT DONE ==="
