#!/usr/bin/env python3
"""
create-all-reminders.py — Script unificado de recordatorios.

Lee obsidian-vault/tasks.md, extrae todas las tareas de la sección HOY
que tengan ⏰ HH:MM, y crea todos los cron jobs de una sola vez.
Emite un JSON array con todos los jobs creados.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

WORKDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_TASKS = os.path.join(WORKDIR, "obsidian-vault", "tasks.md")
PARSE_SCRIPT = os.path.join(WORKDIR, "skills", "arya-reminders", "parse_time.py")
SCHEDULE_SCRIPT = os.path.join(WORKDIR, "skills", "arya-reminders", "schedule_cron.py")
LOG_FILE = os.path.join(WORKDIR, "memory", "reminders.md")
TZ = "America/Bogota"
CHAT_ID = os.environ.get("ARYA_TELEGRAM_CHAT_ID", "7310779816")


def get_today_section():
    """Lee tasks.md y extrae la sección 🔥 HOY — [fecha]"""
    if not os.path.exists(VAULT_TASKS):
        print(f"ERROR: {VAULT_TASKS} not found", file=sys.stderr)
        sys.exit(1)

    with open(VAULT_TASKS, "r") as f:
        content = f.read()

    # Buscar sección HOY
    match = re.search(r'## 🔥 HOY.*?\n(.*?)(?:\n\n---|\n---|\Z)', content, re.DOTALL)
    if not match:
        # Fallback: buscar cualquier sección con HOY
        match = re.search(r'##.*?HOY.*?\n(.*?)(?:\n---|\Z)', content, re.DOTALL)
    if not match:
        print("WARNING: No HOY section found in tasks.md", file=sys.stderr)
        return []

    section = match.group(1)
    return section.split("\n")


def extract_reminders(lines):
    """De las líneas de la sección HOY, extrae (nombre_tarea, hora_str)"""
    reminders = []

    for line in lines:
        line = line.strip()

        # Formato tabla: | N | Tarea | ⏰ HH:MM | Estado | Prioridad |
        table_match = re.match(
            r'\|\s*\d+\s*\|\s*(.*?)\s*\|\s*⏰\s*(\d{1,2}:\d{2}(?:\s*AM|\s*PM)?)\s*\|\s*[✅⏳🔄]?\s*\|\s*[🔴🟡🟢]?\s*\|',
            line
        )
        if table_match:
            task_name = table_match.group(1).strip()
            # Limpiar formato bold **...**
            task_name = re.sub(r'\*\*(.*?)\*\*', r'\1', task_name)
            hora = table_match.group(2).strip()
            reminders.append((task_name, hora))
            continue

        # Formato: 🔴🟡🟢 Tarea · ⏰ HH:MM · ✅⏳🔄
        inline_match = re.match(
            r'[🔴🟡🟢]\s*(.*?)\s*·\s*⏰\s*(\d{1,2}:\d{2}(?:\s*AM|\s*PM)?)\s*·',
            line
        )
        if inline_match:
            task_name = inline_match.group(1).strip()
            hora = inline_match.group(2).strip()
            reminders.append((task_name, hora))
            continue

    return reminders


def parse_hora(hora_str):
    """Usa parse_time.py para convertir '7:00' a timestamp ISO"""
    try:
        result = subprocess.run(
            ["python3", PARSE_SCRIPT, "--tz", TZ, "--when", hora_str],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"  WARNING: parse_time failed for '{hora_str}': {result.stderr}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"  ERROR: parse_time exception for '{hora_str}': {e}", file=sys.stderr)
        return None


def schedule_reminder(name, iso_ts, chat_id):
    """Usa schedule_cron.py para generar JSON del job"""
    try:
        result = subprocess.run(
            ["python3", SCHEDULE_SCRIPT, "--name", name, "--at", iso_ts, "--chat-id", chat_id, "--message", name],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return json.loads(result.stdout.strip())
        else:
            print(f"  WARNING: schedule_cron failed: {result.stderr}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"  ERROR: schedule_cron exception: {e}", file=sys.stderr)
        return None


def log_reminder(name, iso_ts):
    """Escribe en el log de recordatorios"""
    tz = ZoneInfo(TZ)
    dt = datetime.fromisoformat(iso_ts)
    display = dt.astimezone(tz).strftime("%Y-%m-%d %H:%M %Z")

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"- {timestamp} | {display} | {name}\n")


def main():
    ap = argparse.ArgumentParser(description="Create all reminders from tasks.md HOY section")
    ap.add_argument("--dry-run", action="store_true", help="Parse and show what would be created without creating")
    ap.add_argument("--chat-id", default=CHAT_ID, help=f"Telegram chat ID (default: {CHAT_ID})")
    ap.add_argument("--json", action="store_true", help="Output results as JSON (for agent consumption)")
    args = ap.parse_args()

    lines = get_today_section()
    reminders = extract_reminders(lines)

    if not reminders:
        if args.json:
            print(json.dumps({"status": "none", "message": "No tasks with ⏰ found in HOY section", "reminders": []}))
        else:
            print("📭 No se encontraron tareas con ⏰ en la sección HOY.")
        return

    created = []
    failed = []
    skipped = []

    for task_name, hora in reminders:
        print(f"  → {task_name} @ {hora}", file=sys.stderr)

        iso_ts = parse_hora(hora)
        if not iso_ts:
            failed.append({"name": task_name, "reason": "parse_time failed"})
            continue

        # Verificar que el timestamp sea futuro
        tz = ZoneInfo(TZ)
        now = datetime.now(tz)
        dt = datetime.fromisoformat(iso_ts)
        if dt.tzinfo:
            dt_naive = dt.astimezone(tz).replace(tzinfo=None)
        else:
            dt_naive = dt
        now_naive = now.replace(tzinfo=None)

        if dt_naive <= now_naive:
            # Si ya pasó, empujar a mañana (ensure_future inline)
            dt_naive += timedelta(days=1)
            iso_ts = dt_naive.isoformat()
            skipped.append({"name": task_name, "reason": f"pushed to tomorrow ({dt_naive.strftime('%Y-%m-%d %H:%M')})"})
            print(f"    ⏭️  Hora pasada → empujado a mañana", file=sys.stderr)

        if args.dry_run:
            created.append({"name": task_name, "at": iso_ts, "dry_run": True})
            continue

        job = schedule_reminder(task_name, iso_ts, args.chat_id)
        if job:
            # Formatear nombre para el cron (limpiar)
            clean_name = f"Reminder: {task_name}"
            job["name"] = clean_name[:120]  # límite de nombre
            created.append(job)
            log_reminder(task_name, iso_ts)
            print(f"    ✅ Creado: {dt_naive.strftime('%Y-%m-%d %H:%M')}", file=sys.stderr)
        else:
            failed.append({"name": task_name, "reason": "schedule_cron failed"})
            print(f"    ❌ Falló", file=sys.stderr)

    # Output
    if args.json:
        output = {
            "status": "ok",
            "total": len(reminders),
            "created": len(created),
            "failed": len(failed),
            "skipped": len(skipped),
            "reminders": created,
            "errors": failed,
            "notes": skipped
        }
        print(json.dumps(output, ensure_ascii=False))
    else:
        print(f"\n📊 Resumen: {len(created)} creados, {len(failed)} fallos, {len(skipped)} saltados (empujados a mañana)", file=sys.stderr)


if __name__ == "__main__":
    main()
