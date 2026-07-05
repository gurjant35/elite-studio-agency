# Atlas Readiness Check

Date: 2026-07-05

## Read-Only Commands Identified

Safest status/config commands that do not start a Telegram bot or background process:

- `python3 /root/elite-studio-v2/scripts/sheets_helper.py status`
- `python3 /root/elite-studio-v2/scripts/sheets_helper.py settings`
- `python3 /root/elite-studio-v2/scripts/sheets_helper.py tabs`
- `hermes profile show atlas`
- `hermes profile list`
- `hermes gateway status --system`

For this check, only read-only commands were used.

## Atlas Profile Check

Atlas profile files exist at:

- `/root/.hermes/profiles/atlas/SOUL.md`
- `/root/.hermes/profiles/atlas/config.yaml`
- `/root/.hermes/profiles/atlas/.env`

Required profile folders exist:

- `logs`
- `sessions`
- `cron`
- `skills`
- `memories`
- `plans`
- `workspace`
- `home`

No copied sessions were found.

No cron jobs were found in the Atlas profile folder.

No gateway PID, gateway state, or state database exists for Atlas.

## Environment Check

The following required env variable names are present in Atlas `.env`:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_ALLOWED_USERS`
- `TELEGRAM_HOME_CHANNEL`
- `OPENROUTER_API_KEY`
- `GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE`
- `GOOGLE_SHEET_ID`

All of those variables are non-empty.

Secret values are not shown here.

## Google Sheets Check

Google Sheets references are present in Atlas `.env`.

The shared Google Sheets helper still works:

- `python3 scripts/sheets_helper.py status`

Observed status:

- `outreach_paused=true`
- `total_leads=0`
- `total_outreach_log_entries=0`
- latest daily report: `none`

## Risks / Missing Requirements

- Atlas is still not ready to run because the Telegram bot allowlist/channel values in `.env` are still placeholder values.
- Atlas has not been started yet, which is correct for this dry check.
- Cron is not enabled for Atlas, which is also correct for now.
- Do not reuse old profile memory, sessions, or cron jobs when moving from planning into execution.

## Bottom Line

Atlas profile structure is in place and the Google Sheets status path is working.

The remaining blocker is replacing the placeholder Telegram allowlist/channel values with the real Boss identifiers before any live Telegram test.
