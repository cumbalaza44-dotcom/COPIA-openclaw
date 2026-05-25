#!/bin/bash
# Recordatorio: Balancear ingresos — 7 PM
# Creado por JARVIS el 2026-05-22

# Enviar mensaje por Telegram
openclaw message send \
  --channel telegram \
  --target "7310779816" \
  --message "🦾 Recordatorio automático: Balancear ingresos 💰" \
  --silent

echo "[$(date)] Recordatorio enviado: Balancear ingresos" >> /root/.openclaw/workspace/scripts/log-recordatorios.log