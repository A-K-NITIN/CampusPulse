"""
One job function per functionality. Each scheduled job:
  1. Pulls the relevant data (live Sheets / CSVs).
  2. Applies the deterministic checks from decision/checks.py.
  3. For every flagged case, invokes the agent with a plain-language task.

Function 3 (base paper request) is intentionally NOT scheduled here — it's
triggered on demand (e.g. a team leader submitting a problem statement via
an API endpoint you add later). See request_base_paper() below.
"""
import pandas as pd

import config
from decision import checks
from sheets.google_sheets_client import get_attendance_dataframe


def job_attendance_reminder(agent_executor):
    """Function 2."""
    attendance_df = get_attendance_dataframe()
    flagged = checks.check_low_attendance(attendance_df)

    for _, row in flagged.iterrows():
        task = (
            f"Send an attendance reminder email to {row['name']} ({row['email']}). "
            f"Their current attendance is {row['attendance_percent']}%, which is below "
            f"the required {config.ATTENDANCE_THRESHOLD}%. Politely urge them to attend "
            f"classes regularly and mention the shortfall clearly."
        )
        agent_executor.invoke({"input": task})


def job_pre_exam_faculty_alert(agent_executor):
    """Function 4."""
    marks_df = pd.read_csv(config.MARKS_CSV)
    faculty_df = pd.read_csv(config.FACULTY_CSV)

    upcoming = checks.check_exams_approaching(marks_df)
    poor = checks.check_poor_performers(upcoming)

    for subject_code, group in poor.groupby("subject_code"):
        faculty_row = faculty_df[faculty_df["subject_code"] == subject_code]
        if faculty_row.empty:
            continue
        faculty_email = faculty_row.iloc[0]["faculty_email"]
        faculty_name = faculty_row.iloc[0]["faculty_name"]
        subject_name = group.iloc[0]["subject_name"]
        student_list = ", ".join(f"{r.student_id} ({r.percent}%)" for r in group.itertuples())

        task = (
            f"Send an email to {faculty_name} ({faculty_email}), the faculty for "
            f"{subject_name} ({subject_code}). Their exam is coming up soon. "
            f"The following students are currently below {config.POOR_PERFORMER_PERCENT}%: "
            f"{student_list}. Ask the faculty to consider extra support for these students "
            f"before the exam."
        )
        agent_executor.invoke({"input": task})


def job_hod_subject_alert(agent_executor):
    """Function 6."""
    marks_df = pd.read_csv(config.MARKS_CSV)
    hod_df = pd.read_csv(config.HOD_CSV)
    students_df = pd.read_csv(config.STUDENTS_CSV)

    low_subjects = checks.check_subject_low_average(marks_df)

    for _, row in low_subjects.iterrows():
        # Department lookup: whichever department most of this subject's students belong to.
        subj_students = marks_df[marks_df["subject_code"] == row["subject_code"]]["student_id"]
        dept_matches = students_df[students_df["student_id"].isin(subj_students)]["department"]
        if dept_matches.empty:
            continue
        department = dept_matches.mode()[0]
        hod_row = hod_df[hod_df["department"] == department]
        if hod_row.empty:
            continue

        task = (
            f"Send an email to {hod_row.iloc[0]['hod_name']} ({hod_row.iloc[0]['hod_email']}), "
            f"HOD of {department}. The subject {row['subject_name']} ({row['subject_code']}) "
            f"has a class average of {row['average_percent']}%, below the expected "
            f"{config.SUBJECT_AVG_THRESHOLD}%. Alert the HOD and suggest 2-3 concrete ways "
            f"to improve outcomes in this subject."
        )
        agent_executor.invoke({"input": task})


def job_pending_deadlines(agent_executor):
    """Function 7."""
    deadlines_df = pd.read_csv(config.DEADLINES_CSV)
    students_df = pd.read_csv(config.STUDENTS_CSV)

    flagged = checks.check_pending_deadlines(deadlines_df)

    for _, row in flagged.iterrows():
        student_row = students_df[students_df["student_id"] == row["student_id"]]
        if student_row.empty:
            continue
        email = student_row.iloc[0]["email"]
        name = student_row.iloc[0]["name"]

        task = (
            f"Send a reminder email to {name} ({email}) about an incomplete task: "
            f"'{row['task_name']}' ({row['category']}), due on {row['deadline_date']} "
            f"({row['days_left']} day(s) left). Encourage them to complete/submit it in time."
        )
        agent_executor.invoke({"input": task})


def job_hackathon_matching(agent_executor):
    """Function 1: match hackathons to students based on their skills/profile."""
    students_df = pd.read_csv(config.STUDENTS_CSV)

    for _, student in students_df.iterrows():
        task = (
            f"Find hackathons relevant to {student['name']}'s skills ({student['skills']}) "
            f"using your hackathon search tools (check the local list first, then search live "
            f"if needed). If you find a good match, email {student['name']} ({student['email']}) "
            f"with the hackathon name, a short description, the registration link, and the "
            f"deadline. If nothing relevant is found, do not send an email."
        )
        agent_executor.invoke({"input": task})


def job_overall_performance_report(agent_executor, student_id: str):
    """Function 5: on-demand or scheduled report for one student."""
    students_df = pd.read_csv(config.STUDENTS_CSV)
    student_row = students_df[students_df["student_id"] == student_id]
    email_hint = f" Their email is {student_row.iloc[0]['email']}." if not student_row.empty else ""

    task = (
        f"Get the overall performance report for student {student_id} across all subjects "
        f"using your report tool, then email a short, encouraging summary of it to that "
        f"student.{email_hint}"
    )
    agent_executor.invoke({"input": task})


def request_base_paper(agent_executor, problem_statement: str, team_leader_name: str, team_leader_email: str):
    """Function 3: on-demand trigger (e.g. called from an API endpoint later)."""
    task = (
        f"A team led by {team_leader_name} ({team_leader_email}) needs a base paper and "
        f"reference material for this problem statement: \"{problem_statement}\". "
        f"Search the local base paper store first, then Arxiv if nothing suitable is found. "
        f"Email {team_leader_name} with the paper title(s), a one-line relevance note, and "
        f"how to access it (local file path or Arxiv link)."
    )
    agent_executor.invoke({"input": task})
