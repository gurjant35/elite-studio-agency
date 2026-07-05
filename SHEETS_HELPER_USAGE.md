# Sheets Helper Usage

## What It Does

`scripts/sheets_helper.py` is a small command-line helper for the Elite Studio Google Sheets pipeline.

It connects to the Google Sheet using the service account file on the server:

`/root/elite-studio-v2/google-sheets-service-account.json`

It uses this Google Sheet:

`Elite Studio Lead Pipeline`

The helper gives agents a simple and safer way to read basic sheet information and run limited test actions.

## Why Agents Should Use This Helper

Agents should use `scripts/sheets_helper.py` instead of raw Google API calls because it keeps actions controlled.

Raw API calls are easier to misuse. They can accidentally write to the wrong tab, update the wrong range, or delete the wrong rows.

This helper limits what agents can do. Each command has a clear purpose, and the current write commands are only for fake test data.

## Available Commands

### Show Sheet Tabs

```bash
python3 scripts/sheets_helper.py tabs
```

Prints the names of the tabs in the Google Sheet.

Expected tabs:

- Leads
- Outreach Log
- Daily Reports
- Settings

### Show Settings

```bash
python3 scripts/sheets_helper.py settings
```

Prints the Settings tab as simple `key=value` lines.

Example:

```text
timezone=America/Toronto
outreach_paused=true
```

### Count Lead Rows

```bash
python3 scripts/sheets_helper.py lead-count
```

Prints the number of non-empty rows in the Leads tab, not counting the header row.

### Show Pipeline Status

```bash
python3 scripts/sheets_helper.py status
```

Prints a simple pipeline overview.

This is the main command Lucky should use for pipeline status and reporting.

It shows:

- `outreach_paused` value
- Total leads
- Count by Lead Status
- Count by Verification Status
- Total Outreach Log entries
- Latest Daily Reports row, if one exists

This command is read-only. It does not contact anyone and does not change Google Sheets.

### Show Recent Leads

```bash
python3 scripts/sheets_helper.py recent-leads
```

Prints up to 10 recent lead rows in a clean format.

It shows:

- Lead ID
- Business Name
- City
- Province
- Lead Status
- Verification Status
- Last Action

Lucky can use this for safe reporting when Boss asks what is currently in the pipeline.

This command is read-only. It does not contact anyone and does not change Google Sheets.

### Show Outreach Summary

```bash
python3 scripts/sheets_helper.py outreach-summary
```

Prints a simple summary of the Outreach Log.

It shows:

- Total Outreach Log entries
- Count by Action Type
- Count by Result

Lucky can use this to report whether outreach activity has been logged.

This command is read-only. It does not contact anyone and does not change Google Sheets.

### Add A Fake Test Lead

```bash
python3 scripts/sheets_helper.py add-test-lead
```

Adds one fake test row only.

The fake business name is:

`TEST DO NOT CONTACT`

This command is only for testing that the sheet connection works.

### Clear Fake Test Leads

```bash
python3 scripts/sheets_helper.py clear-test-leads
```

Removes rows where the Business Name is exactly:

`TEST DO NOT CONTACT`

It should not be used for real lead cleanup.

## Safety Notes

- `status`, `recent-leads`, and `outreach-summary` are read-only.
- Lucky should use the read-only commands for status and reporting.
- The read-only commands do not contact anyone.
- The read-only commands do not change Google Sheets.
- `add-test-lead` is only for fake testing.
- `clear-test-leads` only removes rows where Business Name exactly matches `TEST DO NOT CONTACT`.
- Do not use the helper to add real leads yet.
- Real outreach is blocked while `outreach_paused=true`.
- Agents must check Settings before doing any future outreach-related action.
- No real emails or calls should happen without owner approval.

## Future Commands We May Add Later

These commands are not part of the helper yet, but they may be added after the safety rules are fully built:

- `add-lead`
- `list-ready-leads`
- `update-lead-status`
- `log-outreach`
- `daily-report`

These future commands should still follow the same rule: Google Sheets is the source of truth, and no outreach happens without approval.
