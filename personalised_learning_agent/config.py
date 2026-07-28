import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RESOURCES_DIR = DATA_DIR / "resources"
CHROMA_DIR = BASE_DIR / "chroma_db"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)

# --- Risk thresholds ---
RISK_HIGH_MARK_PCT = float(os.getenv("RISK_HIGH_MARK_PCT", 40))
RISK_HIGH_ATTENDANCE_PCT = float(os.getenv("RISK_HIGH_ATTENDANCE_PCT", 65))
RISK_MEDIUM_MARK_PCT = float(os.getenv("RISK_MEDIUM_MARK_PCT", 60))
RISK_MEDIUM_ATTENDANCE_PCT = float(os.getenv("RISK_MEDIUM_ATTENDANCE_PCT", 75))

# --- Difficulty adaptation baseline (medium risk) ---
BASE_HOURS_PER_WEEK = float(os.getenv("BASE_HOURS_PER_WEEK", 6))
BASE_DAYS_PER_WEEK = int(os.getenv("BASE_DAYS_PER_WEEK", 4))

# risk_level -> multiplier applied to the base hours/days above
INTENSITY_MULTIPLIER = {
    "low": 0.6,
    "medium": 1.0,
    "high": 1.5,
}

CSV_PATHS = {
    "students": DATA_DIR / "students.csv",
    "marks": DATA_DIR / "marks.csv",
    "attendance": DATA_DIR / "attendance.csv",
    "backlog": DATA_DIR / "backlog.csv",
}
