# Agent usage note (Arya)

When the user asks for a reminder:

1) Derive MESSAGE and WHEN from the user's natural language.

2) Run:

```bash
bash skills/arya-reminders/create-reminder.sh "<MESSAGE>" "<WHEN>"
```

This prints a JSON job request and the display time on stderr.

3) Call the `cron` tool with `action=add` and `job=<that JSON object>`.
   Capture the returned `id` from the Gateway response.

4) Log to `memory/reminders.md`:

```bash
echo "- **HH:MM** Bogotá — Mensaje ([job_id])" >> memory/reminders.md
```

Notes:
- Timezone parsing defaults to America/Bogota.
- Delivery: Telegram -> Mr. Jair (chat 7310779816).
- The JSON output from create-reminder.sh already has `announce: true` and `deleteAfterRun: true`.
