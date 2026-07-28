import os
from dotenv import load_dotenv

load_dotenv()

# --- OpenRouter (LLM brain) ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

# --- Embeddings (local, free — used for RAG only, NOT via OpenRouter) ---
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# --- Vector store ---
VECTORSTORE_DIR = os.getenv("VECTORSTORE_DIR", "./vectorstore")

# --- Google Sheets (live attendance) ---
GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "./credentials/service_account.json")
ATTENDANCE_SHEET_ID = os.getenv("ATTENDANCE_SHEET_ID", "")
ATTENDANCE_WORKSHEET_NAME = os.getenv("ATTENDANCE_WORKSHEET_NAME", "Sheet1")

# --- Email (SMTP) ---
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USERNAME)

# --- Local CSV data paths ---
DATA_DIR = os.getenv("DATA_DIR", "./data/csv")
STUDENTS_CSV = f"{DATA_DIR}/students.csv"
MARKS_CSV = f"{DATA_DIR}/marks.csv"
FACULTY_CSV = f"{DATA_DIR}/faculty.csv"
HOD_CSV = f"{DATA_DIR}/hod.csv"
DEADLINES_CSV = f"{DATA_DIR}/deadlines.csv"
HACKATHONS_CSV = f"{DATA_DIR}/hackathons_seed.csv"

BASE_PAPERS_DIR = os.getenv("BASE_PAPERS_DIR", "./data/documents/base_papers")
BASE_PAPERS_METADATA_CSV = f"{BASE_PAPERS_DIR}/metadata.csv"

# --- Thresholds (deterministic rules — NOT decided by the LLM) ---
ATTENDANCE_THRESHOLD = float(os.getenv("ATTENDANCE_THRESHOLD", 75))
PASS_MARK_PERCENT = float(os.getenv("PASS_MARK_PERCENT", 40))
POOR_PERFORMER_PERCENT = float(os.getenv("POOR_PERFORMER_PERCENT", 50))
SUBJECT_AVG_THRESHOLD = float(os.getenv("SUBJECT_AVG_THRESHOLD", 55))
DEADLINE_WARNING_DAYS = int(os.getenv("DEADLINE_WARNING_DAYS", 3))
EXAM_ALERT_DAYS_BEFORE = int(os.getenv("EXAM_ALERT_DAYS_BEFORE", 5))
