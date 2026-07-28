"""
Live attendance connector (Google Sheets).

Attendance is structured, frequently-changing data. It is pulled fresh on
every scheduler run and queried directly with pandas — it deliberately does
NOT go through the RAG/vector store, since threshold checks need exact
values, not semantic similarity search.

Setup:
  1. Create a Google Cloud service account, enable the Sheets + Drive APIs.
  2. Download its JSON key to the path in GOOGLE_SERVICE_ACCOUNT_JSON.
  3. Share the attendance Google Sheet with the service account's
     client_email (found inside that JSON file) as a Viewer.
  4. Put the sheet's ID (from its URL) in ATTENDANCE_SHEET_ID.
"""
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

import config

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


def _get_client():
    creds = Credentials.from_service_account_file(
        config.GOOGLE_SERVICE_ACCOUNT_JSON, scopes=SCOPES
    )
    return gspread.authorize(creds)


def get_attendance_dataframe() -> pd.DataFrame:
    """
    Fetches the live attendance sheet and returns a DataFrame with columns:
    student_id, name, email, total_classes, attended_classes, attendance_percent

    Expected header row in the sheet:
    student_id, name, email, total_classes, attended_classes
    """
    client = _get_client()
    sheet = client.open_by_key(config.ATTENDANCE_SHEET_ID)
    worksheet = sheet.worksheet(config.ATTENDANCE_WORKSHEET_NAME)
    records = worksheet.get_all_records()
    df = pd.DataFrame(records)

    required_cols = {"student_id", "name", "email", "total_classes", "attended_classes"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Attendance sheet is missing expected columns: {missing}")

    df["total_classes"] = pd.to_numeric(df["total_classes"], errors="coerce")
    df["attended_classes"] = pd.to_numeric(df["attended_classes"], errors="coerce")
    df["attendance_percent"] = (df["attended_classes"] / df["total_classes"] * 100).round(2)

    return df
