# Personalised Learning Agent

Builds a per-student, subject-wise catch-up learning plan by chaining six
agents into one pipeline. Same stack pattern as the Academic Performance
Agent: pandas over CSV for structured data, Chroma for a resource library
RAG store, Claude for generation, SMTP for delivery.

## Pipeline order

```
risk_engine (rule-based)
    -> Recovery Plan Agent       (LLM)  what topics, in what order
    -> Difficulty Adaptation Agent (rule-based) how intense per risk level
    -> Timetable Agent           (LLM)  turns plan + intensity into a weekly grid
    -> Resource Recommendation Agent (RAG) matches topics to notes/videos/practice sets
    -> Revision Planner Agent    (rule-based + LLM phrasing) prioritizes backlog before exams
    -> Learning Coach Agent      (LLM)  compiles everything, emails the student
```

Each agent is a plain function that takes the previous agent's output and
returns structured data (dict/list) — `orchestrator.py` wires them together
so you can swap or reorder agents without touching the others.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # fill in ANTHROPIC_API_KEY, SMTP creds
python -m ingestion.build_vectorstore    # index data/resources/*.txt
```

## Data files (replace samples with real exports)
- `data/students.csv` — roll_no, name, email, dept, year
- `data/marks.csv` — roll_no, subject, exam_type, score, max_score
- `data/attendance.csv` — roll_no, subject, attendance_pct
- `data/backlog.csv` — roll_no, subject, topic, status, exam_date
- `data/resources/*.txt` — one file per resource; first 3 lines are
  `Subject:`, `Topic:`, `Type:` (notes/video/practice) metadata, rest is
  description/link, used for RAG matching in the Resource Recommendation Agent

## Run the full pipeline for one student

```bash
python main.py --student 21CS003
```

## Run a single agent in isolation (useful for testing/debugging)

```bash
python -c "from agents import recovery_plan_agent as a; print(a.build('21CS003'))"
```

## Notes on design choices
- `risk_engine.py` combines marks % and attendance % into low/medium/high
  risk per subject — this drives everything downstream, so it's kept
  deterministic (no LLM) and easy to tune via `config.py` thresholds.
- Difficulty Adaptation is rule-based too: risk level maps to a study-hours
  and days-per-week multiplier. The LLM turns numbers into plans (Recovery
  Plan, Timetable) but doesn't decide the numbers themselves — keeps the
  intensity logic auditable and consistent.
- Resource Recommendation is pure RAG (semantic search over the resource
  library), no generation — it returns matches, and the Learning Coach
  Agent is what phrases them into the final message.
