#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone

# This script prints JSON describing the cron job creation request.
# The agent will call the cron tool with this payload (safer than shelling openclaw CLI).


def to_utc_iso(ts_str: str) -> str:
    """Convert any ISO8601 timestamp to UTC YYYY-MM-DDTHH:MM:SS.000Z"""
    dt = datetime.fromisoformat(ts_str)
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--at", required=True, help="ISO8601 timestamp with tz offset")
    ap.add_argument("--chat-id", required=True, help="Telegram numeric chat ID")
    ap.add_argument("--message", required=True)
    args = ap.parse_args()

    job = {
        "name": args.name,
        "schedule": {"kind": "at", "at": to_utc_iso(args.at)},
        "payload": {
            "kind": "agentTurn",
            "message": f"⏰ Recordatorio: {args.message}",
        },
        "delivery": {
            "mode": "announce",
            "channel": "telegram",
            "to": args.chat_id,
        },
        "sessionTarget": "isolated",
        "deleteAfterRun": True,
        "enabled": True,
    }

    print(json.dumps(job, ensure_ascii=False))


if __name__ == "__main__":
    main()