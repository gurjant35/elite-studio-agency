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
REPORT_FILE = Path("/root/elite-studio-v2/GOOGLE_SHEETS_CONNECTION_TEST.md")
TEST_RANGE = "Settings!A1"
TEST_VALUE = "Google Sheets connection OK"
SCOPE = "https://www.googleapis.com/auth/spreadsheets"


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
    assertion = unsigned + "." + b64url(signature)
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def main() -> int:
    service_account = json.loads(SERVICE_ACCOUNT_FILE.read_text())
    token = get_access_token(service_account)
    headers = {"Authorization": f"Bearer {token}"}
    base = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}"

    metadata_response = requests.get(base, headers=headers, timeout=30)
    metadata_response.raise_for_status()
    metadata = metadata_response.json()
    tabs = [sheet["properties"]["title"] for sheet in metadata.get("sheets", [])]

    write_response = requests.put(
        f"{base}/values/{TEST_RANGE}",
        headers={**headers, "Content-Type": "application/json"},
        params={"valueInputOption": "RAW"},
        json={"range": TEST_RANGE, "majorDimension": "ROWS", "values": [[TEST_VALUE]]},
        timeout=30,
    )
    write_response.raise_for_status()

    read_response = requests.get(
        f"{base}/values/{TEST_RANGE}",
        headers=headers,
        timeout=30,
    )
    read_response.raise_for_status()
    values = read_response.json().get("values", [])
    read_back = values[0][0] if values and values[0] else ""
    ok = read_back == TEST_VALUE

    report = [
        "# Google Sheets Connection Test",
        "",
        f"Sheet ID: `{SHEET_ID}`",
        f"Service account: `{service_account.get('client_email', '')}`",
        "",
        "## Metadata Read",
        "",
        f"Spreadsheet title: `{metadata.get('properties', {}).get('title', '')}`",
        "",
        "Tabs found:",
        "",
        *[f"- {tab}" for tab in tabs],
        "",
        "## Write/Read Test",
        "",
        f"Write target: `{TEST_RANGE}`",
        f"Written value: `{TEST_VALUE}`",
        f"Read back value: `{read_back}`",
        "",
        f"Result: `{'success' if ok else 'failure'}`",
        "",
        "No Hermes configs or services were changed. No real lead data was written.",
        "",
    ]
    REPORT_FILE.write_text("\n".join(report))
    print("SUCCESS" if ok else "FAILURE")
    print(f"Spreadsheet title: {metadata.get('properties', {}).get('title', '')}")
    print("Tabs: " + ", ".join(tabs))
    print(f"{TEST_RANGE}: {read_back}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
