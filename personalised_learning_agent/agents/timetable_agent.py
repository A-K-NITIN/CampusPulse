"""
Timetable Agent — turns the recovery plan + intensity numbers into an
actual weekly schedule (which subject on which day, how long).
"""
from utils.llm_client import generate


def build(recovery_plan: dict, intensity: dict) -> str:
    """Returns a formatted weekly timetable as text."""
    if not recovery_plan:
        return "No catch-up subjects identified — no timetable needed."

    subject_summaries = []
    for subject, info in recovery_plan.items():
        i = intensity.get(subject, {})
        subject_summaries.append(
            f"- {subject} (risk: {info['risk']}): {i.get('days_per_week')} sessions/week, "
            f"{i.get('session_minutes')} min/session, topics in order: "
            f"{', '.join(info['topics'])}"
        )

    return generate(
        system_prompt=(
            "You build a simple weekly study timetable (Mon-Sun) from a list "
            "of subjects, their weekly session count, and session length. "
            "Distribute sessions across the week without overloading any single "
            "day, spread subjects out rather than clustering, and leave at "
            "least one full rest day. Output as a compact day-by-day list."
        ),
        user_prompt="Subjects to schedule:\n" + "\n".join(subject_summaries),
        max_tokens=500,
    )


if __name__ == "__main__":
    from agents import recovery_plan_agent, difficulty_adaptation_agent
    plan = recovery_plan_agent.build("21CS003")
    intensity = difficulty_adaptation_agent.adjust(plan)
    print(build(plan, intensity))
