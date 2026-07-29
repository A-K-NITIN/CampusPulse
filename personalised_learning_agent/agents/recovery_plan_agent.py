"""
Recovery Plan Agent — for each weak subject, orders the pending backlog
topics into a study sequence (foundational topics first, exam-critical
topics prioritized), with a one-line rationale per topic.
"""
from ingestion.load_data import load_backlog, get_student
from utils.risk_engine import compute_risk, weak_subjects
from utils.llm_client import generate


def build(roll_no: str) -> dict:
    """Returns {subject: {"risk": ..., "plan_text": ..., "topics": [pending topic names]}}"""
    student = get_student(roll_no)
    risk_profile = compute_risk(roll_no)
    backlog = load_backlog()
    backlog = backlog[(backlog["roll_no"] == roll_no) & (backlog["status"] == "pending")]

    plan = {}
    for subject in weak_subjects(roll_no):
        topics = backlog[backlog["subject"] == subject]["topic"].tolist()
        if not topics:
            continue

        plan_text = generate(
            system_prompt=(
                "You are an academic recovery planner. Given a student's weak "
                "subject and pending topics, order them into a logical study "
                "sequence (prerequisites before dependent topics) and give a "
                "one-line reason for the order. Keep it under 120 words, as a "
                "short numbered list."
            ),
            user_prompt=(
                f"Student: {student['name']}\n"
                f"Subject: {subject}\n"
                f"Risk level: {risk_profile[subject]['risk']}\n"
                f"Pending topics: {', '.join(topics)}"
            ),
        )
        plan[subject] = {
            "risk": risk_profile[subject]["risk"],
            "plan_text": plan_text,
            "topics": topics,
        }
    return plan


if __name__ == "__main__":
    import json
    print(json.dumps(build("21CS003"), indent=2))
