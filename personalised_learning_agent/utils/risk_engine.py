"""
Rule-based risk scoring — deliberately no LLM here. Risk level drives every
downstream agent (recovery plan depth, study intensity, timetable load), so
it needs to be deterministic and easy to audit/tune via config.py.
"""
from ingestion.load_data import load_marks, load_attendance
from config import (
    RISK_HIGH_MARK_PCT, RISK_HIGH_ATTENDANCE_PCT,
    RISK_MEDIUM_MARK_PCT, RISK_MEDIUM_ATTENDANCE_PCT,
)


def _level(marks_pct: float, attendance_pct: float) -> str:
    if marks_pct < RISK_HIGH_MARK_PCT or attendance_pct < RISK_HIGH_ATTENDANCE_PCT:
        return "high"
    if marks_pct < RISK_MEDIUM_MARK_PCT or attendance_pct < RISK_MEDIUM_ATTENDANCE_PCT:
        return "medium"
    return "low"


def compute_risk(roll_no: str) -> dict:
    """Returns {subject: {"risk": "high"/"medium"/"low", "marks_pct": .., "attendance_pct": ..}}"""
    marks = load_marks()
    marks = marks[marks["roll_no"] == roll_no].copy()
    marks["marks_pct"] = marks["score"] / marks["max_score"] * 100
    marks_by_subject = marks.set_index("subject")["marks_pct"]

    attendance = load_attendance()
    attendance = attendance[attendance["roll_no"] == roll_no]
    attendance_by_subject = attendance.set_index("subject")["attendance_pct"]

    subjects = set(marks_by_subject.index) | set(attendance_by_subject.index)

    profile = {}
    for subject in subjects:
        m = marks_by_subject.get(subject, 100.0)   # assume fine if no data
        a = attendance_by_subject.get(subject, 100.0)
        profile[subject] = {
            "risk": _level(m, a),
            "marks_pct": round(float(m), 1),
            "attendance_pct": round(float(a), 1),
        }
    return profile


def weak_subjects(roll_no: str) -> list[str]:
    profile = compute_risk(roll_no)
    return [s for s, v in profile.items() if v["risk"] in ("medium", "high")]
