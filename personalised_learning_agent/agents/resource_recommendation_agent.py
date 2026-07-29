"""
Resource Recommendation Agent — pure RAG, no generation. For each topic in
the recovery plan, semantically matches against the indexed resource
library (notes/videos/practice sets) and returns the raw matches. The
Learning Coach Agent is what phrases these into the final message.
"""
from rag.retriever import semantic_search


def recommend(recovery_plan: dict, k: int = 2) -> dict:
    """Returns {subject: {topic: [ {content, metadata}, ... ]}}"""
    recommendations = {}
    for subject, info in recovery_plan.items():
        recommendations[subject] = {}
        for topic in info["topics"]:
            matches = semantic_search(f"{subject}: {topic}", k=k)
            recommendations[subject][topic] = [
                {"content": content, "metadata": meta} for content, meta in matches
            ]
    return recommendations


if __name__ == "__main__":
    from agents import recovery_plan_agent
    plan = recovery_plan_agent.build("21CS003")
    import json
    print(json.dumps(recommend(plan), indent=2, default=str))
