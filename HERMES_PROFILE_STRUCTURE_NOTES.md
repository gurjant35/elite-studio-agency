# Hermes Profile Structure Notes

## Scope

This is a read-only inspection summary for planning fresh Elite Studio v2 Hermes profiles.

No live Hermes files were changed. No profiles were created. No secrets are included here.

## Existing Profile Pattern Observed

Hermes named profiles live under:

`/root/.hermes/profiles/<profile-name>/`

Local Hermes code says each profile is intended to be an independent `HERMES_HOME` with its own:

- `config.yaml`
- `.env`
- memories
- sessions
- skills
- gateway files
- cron files
- logs

Fresh profile names can use lowercase letters, numbers, underscores, and hyphens. That means `sara-v2` should be valid. If a command rejects it later for any reason, use `sara2`.

## Minimum Files Needed For A New Profile

For a clean v2 profile, the practical minimum is:

- Profile folder: `/root/.hermes/profiles/<name>/`
- `SOUL.md`
- `config.yaml`
- `.env`

Hermes fresh profile creation also bootstraps folders such as:

- `memories/`
- `sessions/`
- `skills/`
- `logs/`
- `plans/`
- `workspace/`
- `cron/`
- `home/`

For Elite Studio v2, do not copy old `memories/`, `sessions/`, `cron/`, `state.db`, logs, or old gateway state.

## Profile Creation Notes From Local Hermes Help

Local help shows:

```bash
hermes profile create <profile-name>
```

Important options:

- `--clone`: copies `config.yaml`, `.env`, `SOUL.md`, and skills from an existing profile.
- `--clone-all`: copies much more state.
- `--clone-from`: chooses a source profile.
- `--no-skills`: creates an empty profile with no bundled skills.
- `--description`: records what the profile is for.

For v2, avoid `--clone`, `--clone-all`, and `--clone-from` because we want fresh memory, fresh sessions, and clean instructions.

## Telegram Gateway Config Fields

From existing profiles and local Hermes code, Telegram needs secrets in `.env` and small behavior settings in `config.yaml`.

Secrets or IDs should be referenced, not pasted:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_ALLOWED_USERS`
- `TELEGRAM_HOME_CHANNEL`
- Optional: `TELEGRAM_HOME_CHANNEL_NAME`
- Optional: `TELEGRAM_PROXY`

Useful config fields:

```yaml
telegram:
  allowed_chats: ""

messaging:
  telegram:
    poll_timeout: 30

timezone: America/Toronto
```

For Atlas, `allowed_chats` should be restricted to Boss only.

## Model And Provider Config Fields

Existing profiles show two config styles.

Simple style:

```yaml
model: google/gemini-2.5-flash
```

Provider style:

```yaml
model:
  default: some/model-name
  provider: openrouter
```

For v2, model selection should happen later through OpenRouter. Do not reuse old profile model choices automatically.

Expected model/provider secrets should be stored in `.env`, not pasted into docs:

- `OPENROUTER_API_KEY`
- Any other selected provider key, if OpenRouter is not used later

## Env And Secrets To Reference But Not Paste

Do not paste secret values into docs or SOUL files.

Profile `.env` files may eventually need:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_ALLOWED_USERS`
- `TELEGRAM_HOME_CHANNEL`
- `OPENROUTER_API_KEY`
- `GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE=/root/elite-studio-v2/google-sheets-service-account.json`
- `GOOGLE_SHEET_ID=1XIq1WJevgfcgSc7PVFt45woIS3DTkhXzlRapZyuuWjk`

Sara v2 may later need:

- VAPI API key reference
- VAPI assistant ID reference
- Email sending account reference

Those should not be added until Sara v2 is ready for safe testing.

## SOUL.md Structure Observed

Lucky old SOUL structure is short:

- Title
- Identity
- How You Work
- Hard Rules
- Personality

Sara old SOUL structure is long and outreach-heavy:

- Identity
- What Elite Studio sells
- Job
- Email rules
- Email structures
- Email settings
- Hard rules
- Reporting to Lucky
- Notion instructions
- Email sending instructions
- Reply checking
- Inbound lead checking
- VAPI outbound calling
- Calling rules
- Deduplication rule

For v2, use the simple structure style, not the old content.

## Risks From Old Profiles That Must Not Be Copied

Do not copy these old-profile patterns into v2:

- Old Notion pipeline instructions.
- Old Sara email sending instructions.
- Old VAPI calling instructions.
- Old cron jobs.
- Old memories.
- Old sessions.
- Old logs.
- Old `state.db` files.
- Old gateway state files.
- Old `.env` files wholesale.
- Old model choices without review.
- `approvals: mode: auto` from old configs, because logs showed Hermes treated `auto` as unknown and fell back to manual.
- Large broad configs copied from old profiles without understanding each field.

The old Sara profile is especially risky because it contains outreach, Notion, email, and calling instructions from the broken pipeline.

## Recommended Clean Atlas Profile Template

This is a planning template only. It contains no secrets.

### Suggested Profile Name

`atlas`

### Suggested Folder

`/root/.hermes/profiles/atlas/`

### Suggested config.yaml

```yaml
model:
  default: TO_BE_CHOSEN_LATER
  provider: openrouter

toolsets:
  - hermes-cli

timezone: America/Toronto

messaging:
  telegram:
    poll_timeout: 30

telegram:
  allowed_chats: BOSS_CHAT_ID_ONLY

approvals:
  mode: manual
  cron_mode: manual

web:
  backend: ""
  search_backend: ""
  extract_backend: ""

agent:
  max_turns: 20
  gateway_timeout: 300
```

### Suggested .env Shape

```bash
# Per-profile secrets for Atlas.
# Do not paste secrets into docs.

TELEGRAM_BOT_TOKEN=REDACTED
TELEGRAM_ALLOWED_USERS=REDACTED
TELEGRAM_HOME_CHANNEL=REDACTED

OPENROUTER_API_KEY=REDACTED

GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE=/root/elite-studio-v2/google-sheets-service-account.json
GOOGLE_SHEET_ID=1XIq1WJevgfcgSc7PVFt45woIS3DTkhXzlRapZyuuWjk
```

### Suggested SOUL.md Shape

```markdown
# ATLAS — CEO | Elite Studio v2

## Identity

Atlas is the CEO Telegram bot and main control/reporting interface for Boss.

## Source Of Truth

Atlas must treat Google Sheets as the source of truth, not chat memory.

## Allowed Work

Atlas may read project docs and use `scripts/sheets_helper.py` read-only status commands.

## First Version

Status reports only. No delegation. No outreach. No real lead creation.

## Hard Rules

No emails. No calls. No scraping. No direct Google Sheets edits. No changing `outreach_paused`.
```

## Recommended First Manual Test For Atlas

After profile creation later, the first safe behavior should be:

```bash
python3 /root/elite-studio-v2/scripts/sheets_helper.py status
```

Atlas should summarize that output for Boss and do nothing else.

No cron should be enabled until manual testing passes.
