import pandas as pd
from config import CSV_PATHS


def _read(path):
    path = str(path)
    if path.endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    return pd.read_csv(path)


def load_students() -> pd.DataFrame:
    return _read(CSV_PATHS["students"])


def load_marks() -> pd.DataFrame:
    return _read(CSV_PATHS["marks"])


def load_attendance() -> pd.DataFrame:
    return _read(CSV_PATHS["attendance"])


def load_backlog() -> pd.DataFrame:
    return _read(CSV_PATHS["backlog"])


def get_student(roll_no: str) -> dict:
    students = load_students().set_index("roll_no")
    if roll_no not in students.index:
        raise ValueError(f"No student found with roll_no={roll_no}")
    return {"roll_no": roll_no, **students.loc[roll_no].to_dict()}
