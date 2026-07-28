"""
Wires the six agents together in order. Each function's output feeds the
next — swap or reorder agents here without touching their internals.
"""
from agents import (
    recovery_plan_agent,
    difficulty_adaptation_agent,
    timetable_agent,
    resource_recommendation_agent,
    revision_planner_agent,
    learning_coach_agent,
)


def run_for_student(roll_no: str) -> None:
    print(f"[1/6] Recovery Plan Agent — building subject-wise plan for {roll_no}")
    plan = recovery_plan_agent.build(roll_no)

    if not plan:
        print(f"No weak subjects detected for {roll_no} — nothing to send.")
        return

    print("[2/6] Difficulty Adaptation Agent — computing study intensity")
    intensity = difficulty_adaptation_agent.adjust(plan)

    print("[3/6] Timetable Agent — building weekly schedule")
    timetable = timetable_agent.build(plan, intensity)

    print("[4/6] Resource Recommendation Agent — matching topics to resources")
    resources = resource_recommendation_agent.recommend(plan)

    print("[5/6] Revision Planner Agent — prioritizing backlog for exams")
    revision = revision_planner_agent.plan(roll_no)

    print("[6/6] Learning Coach Agent — compiling and emailing the student")
    learning_coach_agent.send(roll_no, plan, timetable, resources, revision)

    print("Done.")


if __name__ == "__main__":
    run_for_student("21CS003")
