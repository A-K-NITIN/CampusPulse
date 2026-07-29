"""
Gmail API sender — replaces SMTP entirely.

Works over HTTPS (port 443), so it is never blocked by college/ISP firewalls
that block SMTP ports 587 / 465.

--- One-time setup ---
1. Go to https://console.cloud.google.com/
2. Create a project (or reuse the one for Google Sheets).
3. Enable "Gmail API" for that project.
4. Go to APIs & Services → Credentials → Create Credentials → OAuth client ID.
   - Application type: Desktop app
   - Download the JSON → save it as  credentials/gmail_oauth_client.json
5. Run:  python -m tools.gmail_auth
   A browser tab opens → sign in → grant permission → token saved automatically.
6. From now on all emails go through Gmail API automatically.

Config keys used (from .env):
    GMAIL_OAUTH_CLIENT_JSON   path to the downloaded OAuth client JSON
    GMAIL_TOKEN_JSON          path where the access/refresh token is stored
    SMTP_FROM_EMAIL           the Gmail address that sends (must match the account
                              you authenticated with in step 5)
"""
import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import config

# Only the send scope is needed
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def _get_credentials() -> Credentials:
    """Load saved token or run the browser-based OAuth flow (first time only)."""
    token_path = config.GMAIL_TOKEN_JSON
    client_path = config.GMAIL_OAUTH_CLIENT_JSON
    creds = None

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(client_path):
                raise FileNotFoundError(
                    f"Gmail OAuth client file not found: {client_path}\n"
                    "Follow the setup instructions in tools/gmail_sender.py to create it."
                )
            flow = InstalledAppFlow.from_client_secrets_file(client_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the token for future runs
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return creds


def send_via_gmail_api(to_email: str, subject: str, body: str) -> str:
    """Send an email using the Gmail API. Returns a success/failure string."""
    creds = _get_credentials()
    service = build("gmail", "v1", credentials=creds)

    msg = MIMEMultipart()
    msg["From"] = config.SMTP_FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    return f"Email sent to {to_email} with subject '{subject}'."
