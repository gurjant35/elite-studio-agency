# Sheets Helper Test Report

Date: 2026-07-05

Helper script:

`/root/elite-studio-v2/scripts/sheets_helper.py`

Sheet ID:

`1XIq1WJevgfcgSc7PVFt45woIS3DTkhXzlRapZyuuWjk`

Service account file:

`/root/elite-studio-v2/google-sheets-service-account.json`

## Commands Tested

### tabs

Result:

- Leads
- Outreach Log
- Daily Reports
- Settings

### settings

Result:

- `timezone=America/Toronto`
- `calling_window_start=09:00`
- `calling_window_end=19:00`
- `outreach_paused=true`
- `real_outreach_requires_owner_approval=true`

### lead-count before test

Result:

`0`

### add-test-lead

Result:

One fake test lead was added with Business Name `TEST DO NOT CONTACT`.

No real lead data was added.

### lead-count after add-test-lead

Result:

`1`

### clear-test-leads

Result:

Removed `1` fake test lead row.

Only rows where Business Name exactly matched `TEST DO NOT CONTACT` were targeted.

### lead-count after clear-test-leads

Result:

`0`

## Final Result

Success.

The helper can read tabs, read settings, count leads, add one fake test lead, and remove fake test leads.

No Hermes configs or services were changed. No one was contacted. `outreach_paused` stayed `true`.
