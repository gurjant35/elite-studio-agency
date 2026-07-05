# Credentials Needed

This checklist is for the new Google Sheets-based Elite Studio pipeline.

Do not paste secrets into public docs or chat unless absolutely necessary. Store secrets in server `.env` files with restricted permissions.

## 1. Google Sheets Service Account JSON

What it is used for:

- Lets the automation read and write the Google Sheet.
- Used by Scout, Verifier, Sara, and Lucky when they update the pipeline.

Where it should be stored:

- Suggested path: `/root/elite-studio-v2/secrets/google-service-account.json`
- File permissions should be restricted so only the server owner can read it.

Do we likely already have it from the old setup?

- Probably not. The old system used Notion, so this may be new.

User action needed?

- Yes. Create or provide a Google service account JSON file.
- Share the Google Sheet with the service account email address.

## 2. Google Sheet ID

What it is used for:

- Tells the automation which Google Sheet is the source of truth.

Where it should be stored:

- Suggested path: `/root/elite-studio-v2/.env`
- Example variable name: `GOOGLE_SHEET_ID`

Do we likely already have it from the old setup?

- No. This is for the new Google Sheets system.

User action needed?

- Yes. Create the Google Sheet and provide the Sheet ID.

## 3. Google Places API Key Or Chosen Lead Source API Key

What it is used for:

- Lets Scout find business leads from Google Places or another selected lead source.

Where it should be stored:

- Suggested path: `/root/elite-studio-v2/.env`
- Example variable names: `GOOGLE_PLACES_API_KEY` or `LEAD_SOURCE_API_KEY`

Do we likely already have it from the old setup?

- Unknown. The old setup used web search and Notion. There may not be a dedicated lead source API key.

User action needed?

- Yes, unless we choose a no-key lead source.

## 4. VAPI API Key And Assistant IDs

What it is used for:

- Lets Sara place approved outbound calls through VAPI.
- Assistant IDs tell VAPI which calling assistant/script to use.

Where it should be stored:

- Suggested path: `/root/elite-studio-v2/.env`
- Example variable names:
  - `VAPI_API_KEY`
  - `VAPI_ASSISTANT_ID_SARA`

Do we likely already have it from the old setup?

- Likely yes, because the old Sara setup referenced VAPI calling.

User action needed?

- Maybe. We need to confirm the existing VAPI key and assistant IDs are still valid.

## 5. Email Sending Credentials Or Existing Himalaya Account Check

What it is used for:

- Lets Sara send approved emails.
- Himalaya may already be configured for the current Hermes email tool.

Where it should be stored:

- Existing Hermes email credentials may already live under Sara's Hermes profile.
- For the new system, use a restricted server `.env` file or the existing secure Himalaya account config.

Do we likely already have it from the old setup?

- Likely yes. Sara had email automation in the old setup.

User action needed?

- Maybe. We should check whether the existing account is still working before using it.

## 6. Telegram Bot Tokens And Profile Mapping For Lucky And Sara

What it is used for:

- Lets Lucky and Sara send status messages or approval requests through Telegram.
- Profile mapping tells the system which Telegram bot/profile belongs to which agent.

Where it should be stored:

- Suggested path: `/root/elite-studio-v2/.env`
- Example variable names:
  - `LUCKY_TELEGRAM_BOT_TOKEN`
  - `SARA_TELEGRAM_BOT_TOKEN`
  - `OWNER_TELEGRAM_CHAT_ID`

Do we likely already have it from the old setup?

- Likely yes. The old Hermes profiles used Telegram.

User action needed?

- Maybe. We need to confirm which tokens and chat IDs should be used for the rebuilt system.

## 7. OpenRouter Or Model Provider Key Used By Hermes

What it is used for:

- Lets Hermes agents use the selected AI models.
- Used by Scout, Verifier, Sara, and Lucky for reasoning and writing.

Where it should be stored:

- Existing Hermes credentials may already be stored in Hermes auth or profile `.env` files.
- For the new project, use a restricted `.env` file if we build outside Hermes.
- Example variable name: `OPENROUTER_API_KEY`

Do we likely already have it from the old setup?

- Likely yes. The audit showed Hermes profiles configured with OpenRouter/model providers.

User action needed?

- Maybe. We need to confirm the provider key is valid and approved for the new pipeline.

## Safe Storage Rules

- Do not paste API keys, passwords, tokens, or service account JSON into public docs.
- Do not paste secrets into chat unless there is no safer option.
- Store secrets in server `.env` files or JSON secret files.
- Keep permissions restricted.
- Keep a simple list of which secret exists, but not the secret value itself.
