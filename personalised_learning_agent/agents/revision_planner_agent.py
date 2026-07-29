"""
Revision Planner Agent — prioritizes pending backlog topics by exam
proximity (soonest exam first) and risk level, and has the LLM turn that
ordering into a short prioritized revision brief. The ordering itself is
rule-based (sorted by date) — only the phrasing is generated.
"""
from datetime import datetime
from ingestion.load_data import load_backlog
from utils.risk_engine import compute_risk
from utils.llm_client import generate


def _prioritized_backlog(roll_no: str) -> list[dict]:
    backlog = load_backlog()
    backlog = backlog[(backlog["roll_no"] == roll_no) & (backlog["status"] == "pending")].copy()
    if backlog.empty:
        return []

    backlog["exam_date"] = backlog.exam_date.apply(
        lambda d: datetime.strptime(str(d), "%Y-%m-%d")
    )
    risk_profile = compute_risk(roll_no)
    backlog["risk_rank"] = backlog["subject"].map(
        lambda s: {"high": 0, "medium": 1, "low": 2}.get(risk_profile.get(s, {}).get("risk", "low"), 2)
    )
    backlog = backlog.sort_values(["exam_date", "risk_rank"])
    return backlog[["subject", "topic", "exam_date", "risk_rank"]].to_dict("records")


def plan(roll_no: str) -> str:
    items = _prioritized_backlog(roll_no)
    if not items:
        return "No pending backlog topics — nothing to prioritize for revision."

    lines = [
        f"- {it['subject']}: {it['topic']} (exam {it['exam_date'].date()})"
        for it in items
    ]

    return generate(
        system_prompt=(
            "You write a short, motivating revision priority list for a "
            "student, based on topics already ordered by exam urgency. "
            "Group by exam if useful, note which 2-3 topics are most urgent, "
            "under 130 words."
        ),
        user_prompt="Pending topics, already ordered by priority:\n" + "\n".join(lines),
        max_tokens=400,
    )


if __name__ == "__main__":
    print(plan("21CS003"))
