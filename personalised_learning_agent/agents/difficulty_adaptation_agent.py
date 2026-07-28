"""
Difficulty Adaptation Agent — converts risk level into concrete study
intensity (hours/week, days/week, session length). Rule-based: the numbers
need to be consistent and auditable, not creatively generated.
"""
from config import BASE_HOURS_PER_WEEK, BASE_DAYS_PER_WEEK, INTENSITY_MULTIPLIER


def adjust(recovery_plan: dict) -> dict:
    """Takes recovery_plan_agent.build() output, returns
    {subject: {"hours_per_week": .., "days_per_week": .., "session_minutes": ..}}"""
    intensity = {}
    for subject, info in recovery_plan.items():
        risk = info["risk"]
        mult = INTENSITY_MULTIPLIER.get(risk, 1.0)
        hours = round(BASE_HOURS_PER_WEEK * mult, 1)
        days = min(6, round(BASE_DAYS_PER_WEEK * mult))
        session_minutes = round((hours / days) * 60) if days else 0

        intensity[subject] = {
            "risk": risk,
            "hours_per_week": hours,
            "days_per_week": days,
            "session_minutes": session_minutes,
        }
    return intensity


if __name__ == "__main__":
    from agents import recovery_plan_agent
    plan = recovery_plan_agent.build("21CS003")
    import json
    print(json.dumps(adjust(plan), indent=2))
