# 2026-05-23 — Arya Reminders: Reparación y puesta a punto

## Contexto
Se identificó que `cron` tool estaba en la deny list del agente `main` (configurado 2026-05-19 para ahorrar tokens). Esto impedía crear recordatorios automáticos.

## Cambios realizados

### openclaw.json
- Eliminado `"cron"` de `agents.list[0].tools.deny` → hot reload automático

### skills/arya-reminders/
- **create-reminder.sh**: chat_id default corregido `5028608085` → `7310779816`
- **schedule_cron.py**: reescrito completamente:
  - `atMs` → `at` ISO string en UTC
  - `deliver/channel/to` embebidos → `delivery: {mode: "announce"}`
  - Agregado `deleteAfterRun: true`
  - Conversión tz-aware a UTC (antes ignoraba offset horario)
- **create-reminder.agent.md**: instrucciones actualizadas

## Estado final
Pipeline completo funcional:
1. parse_time.py → calcula fecha/hora Bogotá
2. schedule_cron.py → genera JSON con timestamp UTC
3. cron.add() → Gateway programa el job (isolated agentTurn → announce → Telegram)
4. Log a memory/reminders.md

## Tests
- Test #1: `fbb4cade` — ejecutado y autodestruido (10:47 Bogotá)
- Test #2: `12c3bc68` — ejecutado y autodestruido (10:55 Bogotá)
