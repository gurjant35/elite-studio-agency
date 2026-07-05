# Next Chat Handoff

## Current Project Goal

Rebuild Elite Studio automation safely as Elite Studio v2.

The new system should use Google Sheets as the source of truth, fresh Hermes profiles, clean agent instructions, and owner approval before any outreach.

## Current Safe State

The old automatic Sara outreach jobs are paused.

The Google Sheet is connected and working.

The helper script can safely read pipeline status.

No fresh v2 Hermes profiles have been created yet.

No live Hermes `SOUL.md` files have been edited.

No real outreach is enabled.

## Fresh v2 Team Names

- Atlas = CEO Telegram bot and main control/reporting interface
- Scout = lead finder
- Mark = verifier / quality checker
- Sara = fresh v2 outreach agent

## Important Files To Read First

Read these before making changes:

- `PROJECT_STATUS.md`
- `ELITE_STUDIO_V2_ARCHITECTURE.md`
- `HERMES_FRESH_PROFILES_PLAN.md`
- `HERMES_PROFILE_STRUCTURE_NOTES.md`
- `SHEETS_HELPER_USAGE.md`

## Completed Milestones

- Old Sara cron jobs paused.
- Hermes configs backed up.
- Google Sheet created and connected.
- Google Sheet headers set up.
- `scripts/sheets_helper.py` created and working.
- Helper status commands are working.
- Agent designs created.
- Fresh v2 team names documented.
- Hermes profile structure inspected read-only.

## Current Safety Rules

- No outreach.
- `outreach_paused=true`.
- Google Sheets is the source of truth.
- Old profiles are legacy.
- Do not clone old profiles.
- Do not copy old memory.
- Do not copy old sessions.
- Do not copy old cron jobs.
- Do not edit live `SOUL.md` files unless the owner explicitly approves that step.
- Do not contact anyone.

## Next Recommended Step

Create the fresh Atlas profile only.

Atlas first version should be reporting-only:

- No cron yet.
- No delegation yet.
- No Scout trigger.
- No Mark trigger.
- No Sara trigger.
- No outreach.
- No real lead creation.

Atlas should answer Boss status questions using:

```bash
python3 /root/elite-studio-v2/scripts/sheets_helper.py status
```

## Prompt For New Codex Chat

Paste this into a new Codex chat:

```text
Continue Elite Studio v2 from /root/elite-studio-v2 on the VPS. First read NEXT_CHAT_HANDOFF.md, PROJECT_STATUS.md, and ELITE_STUDIO_V2_ARCHITECTURE.md. Continue step by step, explain why before each step, and do not change live Hermes until the plan is confirmed.
```
