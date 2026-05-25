#!/bin/bash
# Recordatorio para Mr. Jair: buscar alcohol isopropilico
# Se ejecuta via cron a las 9:00 AM Colombia time

BOT_TOKEN="$(cat /tmp/tg_token.txt)"
CHAT_ID="7310779816"
MESSAGE="⏰ *Recordatorio JARVIS* ⏰%0A%0ABuscar alcohol isopropílico para limpiar la moto 🏍️"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  -d "text=${MESSAGE}" \
  -d "parse_mode=Markdown" > /dev/null 2>&1

# Also log it
echo "[$(date)] Recordatorio enviado: alcohol isopropilico" >> /root/.openclaw/workspace/memory/recordatorios.log