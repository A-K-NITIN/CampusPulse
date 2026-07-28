"""Function 5 helper: overall performance across all subjects."""
import pandas as pd
from langchain.tools import tool

import config
from decision.checks import compute_overall_performance


@tool
def get_student_overall_performance(student_id: str) -> str:
    """
    Returns a student's marks across all subjects and their overall average
    percentage.

    Args:
        student_id: e.g. 'S001'
    """
    marks_df = pd.read_csv(config.MARKS_CSV)
    report = compute_overall_performance(marks_df, student_id)
    if not report["subjects"]:
        return f"No marks found for student {student_id}."

    lines = [f"Overall performance for {student_id} (average: {report['overall_percent']}%):"]
    for s in report["subjects"]:
        lines.append(
            f"  - {s['subject_name']} ({s['subject_code']}): {s['marks']}/{s['max_marks']} = {s['percent']}%"
        )
    return "\n".join(lines)
