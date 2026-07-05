# Hermes Fresh Profiles Plan

## Purpose

Elite Studio v2 should use fresh Hermes profiles.

The new agents should have clean folders, clean instructions, new memory, and new sessions. Old profiles should stay untouched as legacy.

This plan is only a planning document. It does not create profiles yet.

## Old Profiles Stay Untouched

These old profiles stay as legacy and should not be disturbed:

- `lucky`
- `alex`
- `sara`
- `professor`
- `mike`
- `eleven`
- `jarvis`
- `nova`
- `jordan`
- `taylor`
- `morgan`
- `sky`

They should not be reused as the v2 operating team.

## New v2 Profiles

Fresh v2 profiles to create later:

- `atlas`
- `scout`
- `mark`
- `sara-v2`

If Hermes profile names cannot use a hyphen, use:

- `sara2`

## Creation Order

### 1. Atlas First

Atlas is created first.

First purpose:

- Reporting only
- Telegram-facing CEO bot
- Answers Boss status questions
- Reads Google Sheets through `scripts/sheets_helper.py`

Atlas should not delegate work or trigger outreach in the first version.

### 2. Scout Second

Scout is created after Atlas is tested.

First purpose:

- No live scraping
- No real lead creation
- Test-only lead-finding logic
- Reads rules and docs

Scout should not write real leads until helper commands and fake-data tests are ready.

### 3. Mark Third

Mark is created after Scout.

First purpose:

- Fake/test verification only
- No live lead approvals
- No outreach approval
- No guessing

Mark should prove the verification rules with test data before touching real leads.

### 4. Sara v2 Last

Sara v2 is created last.

First purpose:

- No real outreach
- No scheduled outreach
- No emails
- No calls
- Reads rules and prepares for future safe outreach

Sara v2 should not contact businesses until owner approval and all safety gates are working.

## Files For Each New Profile

Each new profile should get:

- Fresh profile folder
- Clean `SOUL.md`
- Clean `config.yaml`
- `.env` only with needed secrets or references

Each new profile should not get:

- Old sessions copied
- Old memory copied
- Old broken cron jobs copied
- Old Notion pipeline copied

Each profile should point to:

- `/root/elite-studio-v2/ELITE_STUDIO_V2_ARCHITECTURE.md`
- `/root/elite-studio-v2/PROJECT_STATUS.md`
- `/root/elite-studio-v2/GOOGLE_SHEETS_PIPELINE_DESIGN.md`
- `/root/elite-studio-v2/SHEETS_HELPER_USAGE.md`
- `/root/elite-studio-v2/scripts/sheets_helper.py`

## Safety Rules

- No cron until manual testing passes.
- No outreach until `outreach_paused=false`.
- No outreach without owner approval.
- No old Notion pipeline.
- Google Sheets is the source of truth.
- Agents must use approved helper scripts.
- Agents must not rely on old profile memory.
- Agents must not reuse old sessions.
- Agents must not contact businesses during setup.

## First Live Target

The first live target is Atlas.

Atlas should answer Boss status questions using:

```bash
python3 /root/elite-studio-v2/scripts/sheets_helper.py status
```

Atlas first version should be able to answer:

- Is outreach paused?
- How many leads are in the sheet?
- What are the lead status counts?
- What are the verification status counts?
- Are there outreach log entries?
- Is there a latest daily report?

Atlas first version should not:

- Delegate to Scout
- Trigger Mark
- Trigger Sara
- Send outreach
- Call businesses
- Email businesses
- Create real leads

Atlas starts as a safe reporting bot only.
