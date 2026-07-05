#!/usr/bin/env python3
import base64
import json
import time
from pathlib import Path

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


SERVICE_ACCOUNT_FILE = Path("/root/elite-studio-v2/google-sheets-service-account.json")
SHEET_ID = "1XIq1WJevgfcgSc7PVFt45woIS3DTkhXzlRapZyuuWjk"
REPORT_FILE = Path("/root/elite-studio-v2/GOOGLE_SHEETS_HEADERS_SETUP.md")
SCOPE = "https://www.googleapis.com/auth/spreadsheets"

HEADERS = {
    "Leads": [
        "Lead ID", "Business Name", "Industry", "City", "Province", "Country",
        "Phone", "Email", "Website", "Source URL", "Source Type", "Lead Status",
        "Verification Status", "Fit Score", "Rejection Reason", "Last Action",
        "Next Action", "Assigned Agent", "Created At", "Updated At", "Notes",
    ],
    "Outreach Log": [
        "Log ID", "Lead ID", "Timestamp", "Agent", "Action Type", "Channel",
        "Result", "Proof ID", "Proof Link", "Message Summary", "Next Step", "Notes",
    ],
    "Daily Reports": [
        "Report Date", "Agent", "New Leads Found", "Leads Verified",
        "Leads Rejected", "Emails Sent", "Calls Placed", "Replies",
        "Follow Ups Needed", "Problems", "Summary",
    ],
    "Settings": ["Setting", "Value", "Notes"],
}

SETTINGS_VALUES = [
    ["timezone", "America/Toronto", ""],
    ["calling_window_start", "09:00", ""],
    ["calling_window_end", "19:00", ""],
    ["outreach_paused", "true", ""],
    ["real_outreach_requires_owner_approval", "true", ""],
]


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def access_token(service_account: dict) -> str:
    now = int(time.time())
    header = {"alg": "RS256", "typ": "JWT"}
    claim = {
        "iss": service_account["client_email"],
        "scope": SCOPE,
        "aud": "https://oauth2.googleapis.com/token",
        "iat": now,
        "exp": now + 3600,
    }
    unsigned = (
        b64url(json.dumps(header, separators=(",", ":")).encode())
        + "."
        + b64url(json.dumps(claim, separators=(",", ":")).encode())
    )
    key = serialization.load_pem_private_key(
        service_account["private_key"].encode(),
        password=None,
    )
    sig = key.sign(unsigned.encode("ascii"), padding.PKCS1v15(), hashes.SHA256())
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": unsigned + "." + b64url(sig),
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def main() -> int:
    service_account = json.loads(SERVICE_ACCOUNT_FILE.read_text())
    token = access_token(service_account)
    headers = {"Authorization": f"Bearer {token}"}
    base = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}"

    metadata = requests.get(base, headers=headers, timeout=30)
    metadata.raise_for_status()
    title = metadata.json().get("properties", {}).get("title", "")
    tabs = [s["properties"]["title"] for s in metadata.json().get("sheets", [])]

    updates = []
    for tab, row in HEADERS.items():
        updates.append({"range": f"'{tab}'!A1", "values": [row]})
    updates.append({"range": "'Settings'!A2:C6", "values": SETTINGS_VALUES})

    write = requests.post(
        f"{base}/values:batchUpdate",
        headers={**headers, "Content-Type": "application/json"},
        params={"valueInputOption": "RAW"},
        json={"data": updates},
        timeout=30,
    )
    write.raise_for_status()

    verified = {}
    for tab in HEADERS:
        read = requests.get(
            f"{base}/values/'{tab}'!1:1",
            headers=headers,
            timeout=30,
        )
        read.raise_for_status()
        verified[tab] = read.json().get("values", [[]])[0]

    ok = all(verified.get(tab) == row for tab, row in HEADERS.items())
    report = [
        "# Google Sheets Headers Setup",
        "",
        f"Sheet ID: `{SHEET_ID}`",
        f"Spreadsheet title: `{title}`",
        f"Service account: `{service_account.get('client_email', '')}`",
        "",
        "## Tabs Seen",
        "",
        *[f"- {tab}" for tab in tabs],
        "",
        "## Header Verification",
        "",
    ]
    for tab, row in verified.items():
        report.extend([
            f"### {tab}",
            "",
            "Read back first row:",
            "",
            ", ".join(row),
            "",
        ])
    report.extend([
        "## Settings Values Written",
        "",
        "- `timezone = America/Toronto`",
        "- `calling_window_start = 09:00`",
        "- `calling_window_end = 19:00`",
        "- `outreach_paused = true`",
        "- `real_outreach_requires_owner_approval = true`",
        "",
        f"Result: `{'success' if ok else 'failure'}`",
        "",
        "No Hermes configs or services were changed. No real leads were added. No one was contacted.",
        "",
    ])
    REPORT_FILE.write_text("\n".join(report))
    print("SUCCESS" if ok else "FAILURE")
    for tab, row in verified.items():
        print(f"{tab}: {', '.join(row)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
