# Google Sheets Pipeline Design

## Purpose

Google Sheets will replace Notion for the new Elite Studio lead pipeline.

The sheet will be the main place where agents read work, write updates, and report progress. This keeps the system easier to inspect, easier to approve, and easier to pause.

Confirmed sheet name:

`Elite Studio Lead Pipeline`

Confirmed sheet ID:

`1XIq1WJevgfcgSc7PVFt45woIS3DTkhXzlRapZyuuWjk`

## Sheet Tabs

The Google Sheet has four confirmed tabs:

1. Leads
2. Outreach Log
3. Daily Reports
4. Settings

## Tab 1: Leads

This is the main pipeline.

Columns:

- Lead ID
- Date Added
- Source
- Business Name
- Trade
- City
- Website
- Google Business Profile
- Email
- Phone
- Contact Name
- Lead Notes
- Scout Status
- Verification Status
- Lead Status
- Rejection Reason
- Outreach Approved By
- Outreach Approved At
- Assigned Agent
- Last Action Date
- Next Action
- Owner Notes

Lead status values:

- New
- Needs Verification
- Verified
- Rejected
- Approved for Outreach
- Email Drafted
- Email Sent
- Call Scheduled
- Call Completed
- Follow Up Needed
- Won
- Lost
- Do Not Contact

Who can write:

- Scout can write: Source, Business Name, Trade, City, Website, Google Business Profile, Email, Phone, Contact Name, Lead Notes, Scout Status.
- Verifier can write: Verification Status, Lead Status, Rejection Reason, Last Action Date, Next Action.
- Lucky CEO can write: Outreach Approved By, Outreach Approved At, Assigned Agent, Owner Notes, Lead Status.
- Sara Outreach can write: Email Drafted, Email Sent, Call Scheduled, Call Completed status updates, Last Action Date, Next Action.

## Tab 2: Outreach Log

This records every email and call.

Columns:

- Log ID
- Date
- Lead ID
- Business Name
- Outreach Type
- Agent
- Status Before Outreach
- Approval Checked
- Email Subject
- Email Proof
- VAPI Call ID
- Call Outcome
- Response Received
- Follow Up Needed
- Notes

Allowed outreach types:

- Email
- VAPI Call
- Follow Up

Who can write:

- Sara Outreach can write outreach records after approval is confirmed.
- Verifier can add notes if a record needs review.
- Lucky CEO can add owner notes and final outcome notes.

## Tab 3: Daily Reports

This is where Lucky reports progress from the sheet.

Columns:

- Report Date
- Reported By
- New Leads Found
- Leads Verified
- Leads Rejected
- Emails Drafted
- Emails Sent
- Calls Made
- Replies Received
- Follow Ups Needed
- Wins
- Problems Found
- Next Recommended Action

Who can write:

- Lucky CEO writes daily summaries.
- Scout, Verifier, and Sara do not write final daily reports unless asked.

## Tab 4: Settings

This controls rules and owner preferences.

Columns:

- Setting Name
- Setting Value
- Notes
- Last Updated By
- Last Updated At

Suggested settings:

- Allowed Cities
- Allowed Trades
- Daily Email Limit
- Daily Call Limit
- Outreach Approval Required
- Owner Approval Name
- Calling Hours Start
- Calling Hours End
- Do Not Contact Keywords
- Approved Email Tone

Who can write:

- Lucky CEO can update settings.
- The business owner can update settings.
- Other agents should read settings but not change them.

## Safety Rules

- No outreach unless the lead status is `Verified` or `Approved for Outreach`.
- If a lead is rejected, it must have a rejection reason.
- Every email must create a row in `Outreach Log`.
- Every email must include proof, such as the email subject, timestamp, and lead ID.
- Every VAPI call must create a row in `Outreach Log`.
- Every VAPI call must log the VAPI call ID.
- Sara must check the lead status before sending an email or starting a call.
- Lucky reports from the Google Sheet, not from memory.
- The sheet is the source of truth. If it is not in the sheet, it should not be treated as done.
- No Notion is used for the new system.

## Simple Workflow

1. Scout adds possible leads to the `Leads` tab.
2. Verifier checks each lead.
3. Bad leads are marked `Rejected` with a reason.
4. Good leads are marked `Verified`.
5. Lucky reviews verified leads and approves outreach.
6. Sara prepares or sends outreach only when approval is present.
7. Every email or call is logged in `Outreach Log`.
8. Lucky creates a daily report from the sheet.
