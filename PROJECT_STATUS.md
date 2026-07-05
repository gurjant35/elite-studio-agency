# Project Status

## Current Goal

We are rebuilding the Elite Studio automation system safely.

The goal is to create a cleaner setup that helps find leads, verify them, prepare outreach, and track everything without accidentally sending emails or making calls.

## What We Found In The Audit

Hermes is installed and has multiple agent profiles.

The main active profiles found were:

- Alex: lead scanning
- Mike: marketing ideas
- Sara: email and calling automation
- Lucky: coordination
- Professor: demand scanning
- Eleven: data/devops support

These are old audited profiles. They are not the final v2 operating team.

Six Hermes gateway services exist and are enabled on the server:

- Alex
- Mike
- Sara
- Lucky
- Professor
- Eleven

The final v2 operating team will use fresh profiles instead of reusing these old profiles.

Sara was the important safety concern because she had two active scheduled jobs:

- `sara-daily-emails`
- `sara-calling-window`

Those jobs were designed to run automatically and could send emails or make calls.

## Safety Lock Applied

Before making any safety change, Sara's Hermes cron jobs file was backed up.

Backup file:

`/root/.hermes/profiles/sara/cron/jobs.json.bak.20260705_172043`

Then only these two Sara jobs were paused:

- `sara-daily-emails`
- `sara-calling-window`

No Hermes profiles were deleted. No gateways or services were stopped. No Cloudflare, SSH, VAPI, email, or Telegram services were stopped.

## Current Safe State

Sara's automatic email job is paused.

Sara's automatic calling job is paused.

That means the system should not automatically send outreach emails or make outreach calls while we rebuild.

Hermes itself still exists, and the server services were not shut down.

## Confirmed Google Sheet

The new pipeline sheet has been created.

Sheet name:

`Elite Studio Lead Pipeline`

Sheet ID:

`1XIq1WJevgfcgSc7PVFt45woIS3DTkhXzlRapZyuuWjk`

Confirmed tabs:

- Leads
- Outreach Log
- Daily Reports
- Settings

## What We Will Build Next

The new Elite Studio system will be rebuilt around a fresh v2 agent team with new Hermes profiles, new memory/sessions, and clean `SOUL.md` files.

- Atlas: CEO Telegram bot and main control/reporting interface for Boss.
- Scout: finds possible leads.
- Mark: verifier and quality checker who confirms leads are real, relevant, and safe to contact.
- Sara: v2 outreach agent who prepares outreach, but does not send without approval.
- Google Sheets dashboard: tracks leads, status, approvals, and results.

Old profiles from the audit should not be reused as the v2 operating team.

## Rules For The New System

- No outreach without approval.
- Google Sheets is the source of truth.
- Every important action must be verified.
- No Notion for the new system.
- The system should be easy for a non-technical owner to understand and control.
