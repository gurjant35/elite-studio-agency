#!/usr/bin/env python3
import argparse
import base64
from collections import Counter
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


SERVICE_ACCOUNT_FILE = Path("/root/elite-studio-v2/google-sheets-service-account.json")
SHEET_ID = "1XIq1WJevgfcgSc7PVFt45woIS3DTkhXzlRapZyuuWjk"
SCOPE = "https://www.googleapis.com/auth/spreadsheets"
TEST_BUSINESS_NAME = "TEST DO NOT CONTACT"

LEADS_HEADERS = [
    "Lead ID",
    "Business Name",
    "Industry",
    "City",
    "Province",
    "Country",
    "Phone",
    "Email",
    "Website",
    "Source URL",
    "Source Type",
    "Lead Status",
    "Verification Status",
    "Fit Score",
    "Rejection Reason",
    "Last Action",
    "Next Action",
    "Assigned Agent",
    "Created At",
    "Updated At",
    "Notes",
]


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def get_access_token(service_account: dict) -> str:
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
        b64url(json.dumps(header, separators=(",", ":")).encode("utf-8"))
        + "."
        + b64url(json.dumps(claim, separators=(",", ":")).encode("utf-8"))
    )
    private_key = serialization.load_pem_private_key(
        service_account["private_key"].encode("utf-8"),
        password=None,
    )
    signature = private_key.sign(
        unsigned.encode("ascii"),
        padding.PKCS1v15(),
        hashes.SHA256(),
    )
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": unsigned + "." + b64url(signature),
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]


class SheetsClient:
    def __init__(self) -> None:
        service_account = json.loads(SERVICE_ACCOUNT_FILE.read_text())
        token = get_access_token(service_account)
        self.headers = {"Authorization": f"Bearer {token}"}
        self.base = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}"

    def metadata(self) -> dict:
        response = requests.get(self.base, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def values(self, range_name: str) -> list[list[str]]:
        response = requests.get(
            f"{self.base}/values/{range_name}",
            headers=self.headers,
            timeout=30,
        )
        response.raise_for_status()
        return response.json().get("values", [])

    def append_values(self, range_name: str, rows: list[list[str]]) -> None:
        response = requests.post(
            f"{self.base}/values/{range_name}:append",
            headers={**self.headers, "Content-Type": "application/json"},
            params={"valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS"},
            json={"values": rows},
            timeout=30,
        )
        response.raise_for_status()

    def batch_update(self, requests_body: list[dict]) -> None:
        response = requests.post(
            f"{self.base}:batchUpdate",
            headers={**self.headers, "Content-Type": "application/json"},
            json={"requests": requests_body},
            timeout=30,
        )
        response.raise_for_status()


def cmd_tabs(client: SheetsClient) -> int:
    for sheet in client.metadata().get("sheets", []):
        print(sheet["properties"]["title"])
    return 0


def cmd_settings(client: SheetsClient) -> int:
    for key, value in settings_dict(client).items():
        print(f"{key}={value}")
    return 0


def settings_dict(client: SheetsClient) -> dict[str, str]:
    rows = client.values("'Settings'!A:C")
    settings = {}
    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        key = row[0].strip()
        value = row[1].strip() if len(row) > 1 else ""
        settings[key] = value
    return settings


def rows_as_dicts(rows: list[list[str]]) -> list[dict[str, str]]:
    if not rows:
        return []
    headers = [cell.strip() for cell in rows[0]]
    result = []
    for row in rows[1:]:
        if not any(cell.strip() for cell in row):
            continue
        item = {}
        for index, header in enumerate(headers):
            item[header] = row[index].strip() if index < len(row) else ""
        result.append(item)
    return result


def non_empty_lead_rows(client: SheetsClient) -> list[list[str]]:
    rows = client.values("'Leads'!A:U")
    return [row for row in rows[1:] if any(cell.strip() for cell in row)]


def lead_dicts(client: SheetsClient) -> list[dict[str, str]]:
    return rows_as_dicts(client.values("'Leads'!A:U"))


def outreach_log_dicts(client: SheetsClient) -> list[dict[str, str]]:
    return rows_as_dicts(client.values("'Outreach Log'!A:L"))


def daily_report_dicts(client: SheetsClient) -> list[dict[str, str]]:
    return rows_as_dicts(client.values("'Daily Reports'!A:K"))


def cmd_lead_count(client: SheetsClient) -> int:
    print(len(non_empty_lead_rows(client)))
    return 0


def print_counter(title: str, counter: Counter[str]) -> None:
    print(f"{title}:")
    if not counter:
        print("- none: 0")
        return
    for key in sorted(counter):
        label = key if key else "(blank)"
        print(f"- {label}: {counter[key]}")


def cmd_status(client: SheetsClient) -> int:
    settings = settings_dict(client)
    leads = lead_dicts(client)
    outreach_logs = outreach_log_dicts(client)
    daily_reports = daily_report_dicts(client)

    print("Pipeline Status")
    print(f"outreach_paused={settings.get('outreach_paused', '')}")
    print(f"total_leads={len(leads)}")
    print_counter("Lead Status counts", Counter(row.get("Lead Status", "") for row in leads))
    print_counter(
        "Verification Status counts",
        Counter(row.get("Verification Status", "") for row in leads),
    )
    print(f"total_outreach_log_entries={len(outreach_logs)}")
    print("latest_daily_report:")
    if daily_reports:
        latest = daily_reports[-1]
        for key in [
            "Report Date",
            "Agent",
            "New Leads Found",
            "Leads Verified",
            "Leads Rejected",
            "Emails Sent",
            "Calls Placed",
            "Replies",
            "Follow Ups Needed",
            "Problems",
            "Summary",
        ]:
            print(f"- {key}: {latest.get(key, '')}")
    else:
        print("- none")
    return 0


def cmd_recent_leads(client: SheetsClient) -> int:
    leads = lead_dicts(client)[-10:]
    if not leads:
        print("No leads found.")
        return 0
    for index, lead in enumerate(reversed(leads), start=1):
        print(f"Lead {index}")
        for key in [
            "Lead ID",
            "Business Name",
            "City",
            "Province",
            "Lead Status",
            "Verification Status",
            "Last Action",
        ]:
            print(f"{key}: {lead.get(key, '')}")
        if index != len(leads):
            print("")
    return 0


def cmd_outreach_summary(client: SheetsClient) -> int:
    rows = outreach_log_dicts(client)
    print(f"total_outreach_log_entries={len(rows)}")
    print_counter("Action Type counts", Counter(row.get("Action Type", "") for row in rows))
    print_counter("Result counts", Counter(row.get("Result", "") for row in rows))
    return 0


def cmd_add_test_lead(client: SheetsClient) -> int:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    row = [
        f"TEST-{int(time.time())}",
        TEST_BUSINESS_NAME,
        "Test Industry",
        "Test City",
        "Ontario",
        "Canada",
        "",
        "",
        "",
        "",
        "Test",
        "Test",
        "Test",
        "0",
        "",
        "Created safe test row",
        "Clear test row",
        "Test",
        now,
        now,
        "Safe test row",
    ]
    client.append_values("'Leads'!A:U", [row])
    print("Added fake test lead only.")
    return 0


def cmd_clear_test_leads(client: SheetsClient) -> int:
    metadata = client.metadata()
    leads_sheet = next(
        (
            sheet["properties"]
            for sheet in metadata.get("sheets", [])
            if sheet["properties"]["title"] == "Leads"
        ),
        None,
    )
    if not leads_sheet:
        raise RuntimeError("Leads tab not found")

    rows = client.values("'Leads'!A:U")
    if not rows:
        print("Removed 0 fake test lead rows.")
        return 0

    header = rows[0]
    try:
        business_idx = header.index("Business Name")
    except ValueError as exc:
        raise RuntimeError("Business Name column not found") from exc

    delete_requests = []
    for zero_based_row, row in reversed(list(enumerate(rows[1:], start=1))):
        business_name = row[business_idx].strip() if len(row) > business_idx else ""
        if business_name == TEST_BUSINESS_NAME:
            delete_requests.append(
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": leads_sheet["sheetId"],
                            "dimension": "ROWS",
                            "startIndex": zero_based_row,
                            "endIndex": zero_based_row + 1,
                        }
                    }
                }
            )

    if delete_requests:
        client.batch_update(delete_requests)
    print(f"Removed {len(delete_requests)} fake test lead row(s).")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Safe Google Sheets helper for Elite Studio v2.")
    parser.add_argument(
        "command",
        choices=[
            "tabs",
            "settings",
            "lead-count",
            "add-test-lead",
            "clear-test-leads",
            "status",
            "recent-leads",
            "outreach-summary",
        ],
    )
    args = parser.parse_args(argv)
    client = SheetsClient()
    commands = {
        "tabs": cmd_tabs,
        "settings": cmd_settings,
        "lead-count": cmd_lead_count,
        "add-test-lead": cmd_add_test_lead,
        "clear-test-leads": cmd_clear_test_leads,
        "status": cmd_status,
        "recent-leads": cmd_recent_leads,
        "outreach-summary": cmd_outreach_summary,
    }
    return commands[args.command](client)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
