"""
Learning Coach Agent — the final step. Compiles the recovery plan,
timetable, recommended resources, and revision priorities into one
structured message and emails it to the student.
"""
from ingestion.load_data import get_student
from utils.llm_client import generate
from utils.email_sender import send_email


def _format_resources(resources: dict) -> str:
    lines = []
    for subject, topics in resources.items():
        for topic, matches in topics.items():
            for m in matches:
                # metadata isn't reliably populated by DirectoryLoader, so pull
                # the Type: line out of the content itself as a fallback
                type_line = next(
                    (l for l in m["content"].splitlines() if l.lower().startswith("type:")),
                    "Type: resource",
                )
                lines.append(f"  - [{topic}] {type_line.strip()} — see: {m['content'][:60]}...")
    return "\n".join(lines) if lines else "  (no matching resources found)"


def send(roll_no: str, recovery_plan: dict, timetable: str, resources: dict, revision: str) -> None:
    student = get_student(roll_no)

    if not recovery_plan:
        print(f"{student['name']} has no weak subjects — skipping learning plan email.")
        return

    plan_text = "\n\n".join(
        f"{subject} (risk: {info['risk']}):\n{info['plan_text']}"
        for subject, info in recovery_plan.items()
    )
    resource_text = "\n".join(
        f"{subject}:\n{_format_resources({subject: topics})}"
        for subject, topics in resources.items()
    )

    body = generate(
        system_prompt=(
            "You are a warm, encouraging learning coach writing directly to "
            "a student. Combine the recovery plan, timetable, resources, and "
            "revision priorities into ONE clear, structured email with "
            "headers: Your Recovery Plan / Weekly Timetable / Recommended "
            "Resources / Revision Priorities. Keep it motivating but concrete "
            "— concrete next steps, not generic encouragement. Under 350 words."
        ),
        user_prompt=(
            f"Student: {student['name']}\n\n"
            f"RECOVERY PLAN:\n{plan_text}\n\n"
            f"TIMETABLE:\n{timetable}\n\n"
            f"RESOURCES:\n{resource_text}\n\n"
            f"REVISION PRIORITIES:\n{revision}"
        ),
        max_tokens=900,
    )

    # send_email(
    #     to=student["email"],
    #     subject="Your personalised catch-up learning plan",
    #     body=body,
    # )
print("Learning plan generated successfully. Email sending skipped.")

if __name__ == "__main__":
    from agents import (
        recovery_plan_agent, difficulty_adaptation_agent,
        timetable_agent, resource_recommendation_agent, revision_planner_agent,
    )
    roll_no = "21CS003"
    plan = recovery_plan_agent.build(roll_no)
    intensity = difficulty_adaptation_agent.adjust(plan)
    tt = timetable_agent.build(plan, intensity)
    res = resource_recommendation_agent.recommend(plan)
    rev = revision_planner_agent.plan(roll_no)
    send(roll_no, plan, tt, res, rev)
