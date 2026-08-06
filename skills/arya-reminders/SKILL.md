---
name: arya-reminders
description: Recordatorios en lenguaje natural (Bogotá). Crea cron jobs seguros y registra en markdown (y opcionalmente Sheets).
metadata:
  openclaw:
    emoji: "⏰"
    requires:
      bins: ["bash", "python3"]
---

# Arya Reminders

Recordatorios en lenguaje natural para OpenClaw, diseñados para Jaider.

## Qué hace

- Interpreta fechas/horas relativas y absolutas en español (y formatos comunes).
- Usa **America/Bogota** por defecto.
- Crea recordatorios **one-shot** (una sola vez) como cron jobs.
- Registra cada recordatorio en `memory/reminders.md`.
- (Opcional futuro) registrar en Google Sheets cuando esté habilitado.

## Uso (conversacional)

Ejemplos:
- "Recuérdame pagar la luz mañana a las 3pm"
- "Recuérdame en 45 minutos revisar el horno"
- "Recuérdame hoy a las 5:30pm llamar a mamá"
- "Recuérdame el viernes a las 9am entregar el taller"

## Comandos (manual)

### Crear recordatorio (una vez)

```bash
bash skills/arya-reminders/create-reminder.sh "Mensaje" "Cuándo"
```

### Revisar log

```bash
cat memory/reminders.md
```

## Notas

- No requiere APIs externas.
- Usa el tool `cron` del Gateway (no hardcodea rutas ni IDs ajenos).
- **sessionTarget:** `isolated` para one-shot (evita ensuciar la sesión principal).

---

## ✅ Checklist obligatorio (2 pasos)

> **Siempre ambos. Sin excepciones.**

### PASO 1 — Crear cron job

```
cron → action: add → job: {
  name: "Recordatorio: <descripción>",
  schedule: {
    kind: "at",
    at: "<ISO-8601 con offset -05:00>"
  },
  payload: {
    kind: "agentTurn",
    message: "Recordatorio: <mensaje>. Enviar por Telegram."
  },
  sessionTarget: "isolated",
  delivery: {
    mode: "announce",
    channel: "telegram",
    to: "7310779816"
  },
  enabled: true
}
```

**Campos obligatorios:** `name`, `schedule.kind`, `schedule.at`, `payload.kind`, `payload.message`, `sessionTarget`, `delivery.mode`, `delivery.channel`, `delivery.to`

**Errores comunes:**
- ❌ Olvidar `delivery.channel` y `delivery.to` → el sistema resuelve a un target incorrecto
- ❌ Usar `sessionTarget: "main"` en one-shot → ensucia la sesión principal
- ❌ Usar `kind: "cron"` en vez de `kind: "at"` → se repite forever
- ❌ Olvidar el offset `-05:00` → hora en UTC, no en Bogotá

### PASO 2 — Registrar en memory/reminders.md

```bash
# Al final de la sección del día, agregar línea:
| <timestamp actual> | <cuándo dispara> | <mensaje> | <cron job ID corto (8 chars)> |
```

**Ejemplo:**
```
## 2026-06-27
| 2026-06-27 11:43 | 2026-06-27 21:00 | Investigar ciclo menstrual | 3f8d8419 |
```

---

## 📐 Formato de schedule.at

| Tipo | Formato | Ejemplo |
|------|---------|--------|
| Hoy a las 9pm | `AAAA-MM-DDTHH:00:00-05:00` | `2026-06-27T21:00:00-05:00` |
| Mañana 7am | `AAAA-MM-DDTHH:00:00-05:00` | `2026-06-28T07:00:00-05:00` |
| Próx. martes 4pm | Calcular fecha manual | `2026-06-30T16:00:00-05:00` |

**Siempre `-05:00` (Bogotá). Nunca UTC.**
