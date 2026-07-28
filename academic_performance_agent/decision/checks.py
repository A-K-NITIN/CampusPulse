"""
Deterministic rule layer.

No LLM calls happen in this file. It reads structured data (live Sheets +
local CSVs) and applies hardcoded threshold rules to decide WHO/WHAT needs
attention. The agent (agent/agent_setup.py) is only invoked afterwards, to
draft and send messages for whatever this layer flags.
"""
from datetime import date
import pandas as pd

import config


def check_low_attendance(attendance_df: pd.DataFrame) -> pd.DataFrame:
    """Function 2: students below the attendance threshold."""
    return attendance_df[attendance_df["attendance_percent"] < config.ATTENDANCE_THRESHOLD].copy()


def check_poor_performers(marks_df: pd.DataFrame) -> pd.DataFrame:
    """Function 4: students scoring below the 'poor performer' cutoff, per subject."""
    marks_df = marks_df.copy()
    marks_df["percent"] = (marks_df["marks"] / marks_df["max_marks"] * 100).round(2)
    return marks_df[marks_df["percent"] < config.POOR_PERFORMER_PERCENT]


def check_subject_low_average(marks_df: pd.DataFrame) -> pd.DataFrame:
    """Function 6: subjects whose class average is below threshold -> HOD alert."""
    marks_df = marks_df.copy()
    marks_df["percent"] = marks_df["marks"] / marks_df["max_marks"] * 100
    subject_avg = (
        marks_df.groupby(["subject_code", "subject_name"])["percent"]
        .mean()
        .reset_index()
        .rename(columns={"percent": "average_percent"})
    )
    subject_avg["average_percent"] = subject_avg["average_percent"].round(2)
    return subject_avg[subject_avg["average_percent"] < config.SUBJECT_AVG_THRESHOLD]


def check_pending_deadlines(deadlines_df: pd.DataFrame, days_before: int = None) -> pd.DataFrame:
    """Function 7: incomplete tasks whose deadline is within N days."""
    days_before = days_before if days_before is not None else config.DEADLINE_WARNING_DAYS
    deadlines_df = deadlines_df.copy()
    deadlines_df["deadline_date"] = pd.to_datetime(deadlines_df["deadline_date"]).dt.date
    today = date.today()
    deadlines_df["days_left"] = deadlines_df["deadline_date"].apply(lambda d: (d - today).days)
    pending = deadlines_df[deadlines_df["status"].str.lower() != "completed"]
    return pending[(pending["days_left"] >= 0) & (pending["days_left"] <= days_before)]


def check_exams_approaching(marks_df: pd.DataFrame, days_before: int = None) -> pd.DataFrame:
    """Helper for function 4: only consider poor performers whose exam is within N days."""
    days_before = days_before if days_before is not None else config.EXAM_ALERT_DAYS_BEFORE
    marks_df = marks_df.copy()
    marks_df["exam_date"] = pd.to_datetime(marks_df["exam_date"]).dt.date
    today = date.today()
    marks_df["days_to_exam"] = marks_df["exam_date"].apply(lambda d: (d - today).days)
    return marks_df[(marks_df["days_to_exam"] >= 0) & (marks_df["days_to_exam"] <= days_before)]


def compute_overall_performance(marks_df: pd.DataFrame, student_id: str) -> dict:
    """Function 5: a single student's performance across all subjects."""
    student_marks = marks_df[marks_df["student_id"] == student_id].copy()
    if student_marks.empty:
        return {"student_id": student_id, "subjects": [], "overall_percent": None}

    student_marks["percent"] = (student_marks["marks"] / student_marks["max_marks"] * 100).round(2)
    subjects = student_marks[["subject_code", "subject_name", "marks", "max_marks", "percent"]].to_dict("records")
    overall_percent = round(student_marks["percent"].mean(), 2)
    return {"student_id": student_id, "subjects": subjects, "overall_percent": overall_percent}
