# Elite Studio v2 Architecture

## Goal

Elite Studio v2 is a safer rebuild of the automation system.

The goal is to help find leads, verify them, prepare outreach, and report progress without accidentally emailing or calling businesses.

The system should be simple enough for the owner to understand and control.

## What Stays From The Old Setup

These parts of the old setup can stay, but they must be used carefully:

- VPS server
- Cloudflare SSH access
- Hermes installation
- VAPI assistants
- Email setup, if verified later
- Telegram bots, if verified later

Nothing old should be trusted blindly. Anything reused must be checked before it is connected to the new pipeline.

The v2 operating team should be fresh: new Hermes profiles, new memory/sessions, and clean `SOUL.md` files.

Old Hermes profiles should not be reused as the v2 operating team.

## What Changes

Google Sheets replaces Notion for the new lead pipeline.

The new Google Sheet is:

`Elite Studio Lead Pipeline`

Sheet ID:

`1XIq1WJevgfcgSc7PVFt45woIS3DTkhXzlRapZyuuWjk`

Confirmed tabs:

- Leads
- Outreach Log
- Daily Reports
- Settings

Old automatic Sara cron jobs remain paused:

- `sara-daily-emails`
- `sara-calling-window`

Agents must use helper scripts and project docs instead of making raw, uncontrolled changes.

No agent can contact businesses until the owner approves it.

No Notion is used for the new system.

## System Flow

The intended flow is:

Boss -> Atlas CEO -> Scout -> Mark -> Sara -> Google Sheets reports

What that means:

- Boss gives direction and approvals.
- Atlas CEO talks to Boss and reports status.
- Atlas is the CEO Telegram bot and main control/reporting interface.
- Boss can ask Atlas questions about the pipeline.
- Boss can tell Atlas what to do.
- Atlas reports everything important to Boss.
- Scout finds possible Canadian local business leads.
- Mark checks if the leads are real, Canadian, local, not duplicates, and a good fit.
- Sara handles outreach only after Mark verifies the lead and the owner approves outreach.
- Google Sheets stores the truth and reports.

## Agent Roles

### Atlas CEO

Atlas is the Telegram-facing CEO/manager for Elite Studio.

Atlas talks to Boss, reads the project docs, reads Google Sheets through `scripts/sheets_helper.py`, and reports safe summaries.

Atlas is the main control and reporting interface for the owner.

Boss should be able to ask Atlas questions like:

- What is the current pipeline status?
- Is outreach paused?
- How many leads are in the sheet?
- What needs approval?
- What happened today?

Boss should also be able to tell Atlas what to do, such as asking for a status report, asking to prepare a plan, or asking to request approval before another agent runs.

Atlas must report everything important back to Boss.

First version behavior:

- Status reports only
- No autonomous pipeline
- No outreach
- No real lead creation

Atlas must treat Google Sheets as the source of truth, not chat memory.

### Scout

Scout finds possible Canadian small or local businesses that may need an AI receptionist or automation.

Scout targets businesses like dentists, clinics, salons, barbers, restaurants, plumbers, HVAC, electricians, landscapers, contractors, cleaners, auto shops, and other solo or small service businesses.

First version behavior:

- Design only
- No live scraping
- No scheduled jobs
- No real lead creation

### Mark

Mark is the verifier and quality checker.

Mark checks candidate leads before outreach. Mark rejects fake, wrong-country, duplicate, franchise, big corporation, unclear, or bad-fit leads.

First version behavior:

- Design only
- No live verification
- No scheduled jobs
- No sheet edits

### Sara Outreach

Sara is the outreach agent.

Sara eventually sends emails and places VAPI calls, but only when the lead is verified, owner-approved, and outreach is unpaused.

Sara v2 outreach should use professional, business-owner-friendly language.

Sara should sell AI receptionist and missed-call automation, not website design.

Future outreach messaging should adapt to timing:

- Weekend angle: missed weekend calls, after-hours inquiries, and capturing leads when staff are busy or unavailable.
- Holiday or long weekend angle: missed holiday calls, closed-office periods, and making sure customer inquiries are still answered.
- Weekday angle: busy work hours, missed calls, booking friction, and owner time savings.

Sara must not use these outreach messages live until `outreach_paused=false` and owner approval is recorded.

Exact email templates and VAPI call scripts will be designed later before live outreach.

First version behavior:

- Design only
- No live outreach
- No scheduled jobs
- No emails
- No calls

If proof is missing, Sara must report `not verified` instead of claiming success.

## Model Selection Later

Agent models will be chosen later through OpenRouter.

Atlas likely needs the strongest reasoning and planning model.

Scout can use a cost-efficient model if lead finding quality is still good.

Mark needs a careful verification model that avoids guessing.

Sara needs a stable communication and tool-use model.

We do not need the same model for every agent.

Model choice will be based on:

- Quality
- Cost
- Speed
- Tool reliability
- Context length

Do not reuse old profile model choices automatically.

## Safety Model

The safety model is the most important part of Elite Studio v2.

Rules:

- `outreach_paused=true` by default.
- Google Sheets is the source of truth.
- Every important action requires proof.
- No outreach without a verified lead and owner approval.
- No agent should contact a business unless the sheet and owner approval allow it.
- No direct raw JSON reading by agents.
- Agents should use approved helper commands instead of raw Google API calls.
- Rejected leads must have a reason.
- Every email must log proof.
- Every VAPI call must log a VAPI call ID.
- Atlas reports from the sheet, not memory.

## Scheduled Jobs Plan

Cron or scheduled jobs should exist in the final safe system.

The final system should include Atlas scheduled reporting, so Boss gets regular status updates without having to ask every time.

Scout scheduled jobs may exist later, but only after safe tests prove Scout can add clean candidate leads without contacting anyone.

Mark scheduled jobs may exist later, but only after safe tests prove Mark can review candidates without guessing or approving uncertain leads.

Sara scheduled outreach may exist later, but only after owner approval and safety gates are fully working.

Sara must never run scheduled outreach while `outreach_paused=true`.

The old Sara cron jobs from the broken pipeline are paused for now. They are not the final cron design.

## Google Sheets Helper

The current helper script is:

`scripts/sheets_helper.py`

Current safe commands:

- `tabs`
- `settings`
- `lead-count`
- `add-test-lead`
- `clear-test-leads`

The current write commands are only for fake testing.

`add-test-lead` adds only a fake row with Business Name:

`TEST DO NOT CONTACT`

`clear-test-leads` removes only rows where Business Name exactly matches:

`TEST DO NOT CONTACT`

## Current Completed Milestones

Completed so far:

- Hermes setup was audited.
- Sara's two automatic cron jobs were paused.
- A safety lock report was created.
- Important Hermes configuration was backed up.
- Project status was documented.
- Google Sheets pipeline design was documented.
- Credentials needed were documented.
- Google Sheet was created and confirmed.
- Google Sheets service account access was tested.
- Sheet headers were set up.
- Settings values were added:
  - `timezone=America/Toronto`
  - `calling_window_start=09:00`
  - `calling_window_end=19:00`
  - `outreach_paused=true`
  - `real_outreach_requires_owner_approval=true`
- `scripts/sheets_helper.py` was created.
- The helper was tested with fake data only.
- Atlas CEO role was designed.
- Scout role was designed.
- Mark verifier role was designed.
- Sara v2 outreach role was designed.

## Next Planned Milestones

Next steps:

- Expand `scripts/sheets_helper.py` with real lead commands.
- Build fake-data tests for future commands.
- Create fresh Atlas Hermes profile safely.
- Test Atlas status report only.
- Later build Scout integration.
- Later build Mark integration.
- Later build Sara v2 outreach integration.

Future helper commands may include:

- `add-lead`
- `list-ready-leads`
- `update-lead-status`
- `log-outreach`
- `daily-report`

These commands should be built and tested with fake data before any real business data or outreach is allowed.

## Owner Control Rule

The owner stays in control.

No business should be emailed or called unless:

- The lead is verified.
- The lead is approved for outreach.
- `outreach_paused=false`.
- The action is logged.
- Proof is recorded.

Until those rules are fully implemented and tested, Elite Studio v2 remains in safe rebuild mode.
