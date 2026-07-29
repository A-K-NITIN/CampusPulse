# Academic Performance Agent (backend)

A single LangChain agent (brain: an OpenRouter model) exposed with tools,
triggered by a scheduler, that covers all 7 functionalities:

1. Hackathon discovery + student email
2. Attendance % reminders
3. Base paper / document delivery to team leaders (on demand)
4. Pre-exam alerts to subject faculty about poor performers
5. Overall student performance reports
6. HOD alerts for low subject averages, with improvement suggestions
7. Deadline reminders (hackathon registration, assignments, tasks)

## Architecture

```
Live Google Sheet (attendance) ---\
Local CSVs (marks, faculty, HOD,   >--> decision/checks.py (hardcoded rules,
  deadlines, students, hackathons)-/     NO LLM here — decides WHO/WHAT)
                                              |
                                              v
                              scheduler/jobs.py (builds a plain-language
                                task per flagged case)
                                              |
                                              v
                          agent/agent_setup.py (ONE LangChain agent,
                            OpenRouter model, with tools below)
                                              |
                    -------------------------------------------------
                    |            |                |                |
            hackathon tools  base_paper tools  student_report   send_email
            (local CSV +     (local RAG +      (marks.csv        (SMTP —
             DuckDuckGo)      Arxiv)            aggregation)      final step)
```

**Key design decisions, and why:**

- **Attendance is NOT embedded into RAG.** It's structured, numeric, and
  changes daily — it's pulled live from Google Sheets into a DataFrame and
  queried directly with exact thresholds. RAG/vector search is only used for
  base paper metadata, where you're matching on *meaning* (a problem
  statement to a paper's topic), not exact values.
- **Thresholds are hardcoded in `config.py`**, not decided by the LLM. The
  decision layer (`decision/checks.py`) has zero LLM calls — it's plain
  pandas logic. The agent is only invoked afterwards, to draft/send the
  message for whatever was already flagged.
- **One agent, many tools** — not 7 separate agents. `agent/agent_setup.py`
  builds a single `AgentExecutor` with all tools; each scheduled job just
  gives it a different plain-language task string per flagged case.
- **Embeddings are local (sentence-transformers), not via OpenRouter** —
  OpenRouter is used purely as the chat "brain"; embeddings for the RAG
  store run locally and are free, avoiding a second API dependency.
- **Live web search uses DuckDuckGo** (`langchain_community` tool, no API
  key required) as the fallback for hackathon discovery. Swap in Tavily or
  SerpAPI later if you want higher-quality results and have a key.
- **Base paper search is hybrid**: local RAG store (curated/approved papers)
  first, Arxiv (`ArxivQueryRun`) as a live fallback.
- **Function 3 is on-demand, not scheduled** — a team leader submitting a
  problem statement isn't a periodic event. `scheduler/jobs.request_base_paper()`
  is written to be called directly, e.g. from an API endpoint you add later.

## Setup

1. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```
   cp .env.example .env
   ```
   Fill in:
   - `OPENROUTER_API_KEY`, `OPENROUTER_MODEL` — get a key at https://openrouter.ai
   - `GOOGLE_SERVICE_ACCOUNT_JSON`, `ATTENDANCE_SHEET_ID` — see below
   - `SMTP_USERNAME`, `SMTP_PASSWORD` (use a Gmail **App Password**, not your real password)

3. **Google Sheets (live attendance)**
   - Create a Google Cloud project → enable the **Google Sheets API** and
     **Google Drive API** → create a **Service Account** → download its JSON
     key into `credentials/service_account.json`.
   - Open your attendance Google Sheet → click Share → paste the service
     account's `client_email` (inside the JSON file) → give it **Viewer** access.
   - Copy the sheet's ID from its URL (`.../d/<THIS_PART>/edit`) into
     `ATTENDANCE_SHEET_ID`.
   - Expected sheet header row: `student_id, name, email, total_classes, attended_classes`

4. **Add your real data**
   Replace the sample rows in `data/csv/*.csv` with real data (same column
   headers). Drop actual base paper PDFs into `data/documents/base_papers/`
   and list them in its `metadata.csv`.

5. **Build the RAG index**
   ```
   python -m rag.ingest
   ```
   Re-run this any time `data/documents/base_papers/metadata.csv` changes.

6. **Test a single function before running everything on a schedule**
   ```
   python main.py --run-now attendance
   python main.py --run-now deadlines
   python main.py --run-now faculty
   python main.py --run-now hod
   python main.py --run-now hackathons
   python main.py --run-now report --student S001
   python main.py --run-now base_paper --problem "smart irrigation system" \
       --leader-name "Rahul Verma" --leader-email rahul.verma@example.edu
   ```

7. **Run continuously (starts the scheduler)**
   ```
   python main.py
   ```
   Default schedule (edit in `main.py`):
   - 8:00 AM daily — attendance reminders
   - 8:30 AM daily — deadline reminders
   - 9:00 AM daily — pre-exam faculty alerts
   - 9:00 AM Mondays — HOD subject alerts
   - 10:00 AM Mondays — hackathon matching

## Folder structure

```
config.py                    All settings, loaded from .env
main.py                      Entry point (scheduler + --run-now testing)
data/csv/*.csv                Sample structured data — replace with real data
data/documents/base_papers/   Base paper PDFs + metadata.csv (RAG source)
sheets/google_sheets_client.py  Live attendance connector (Google Sheets)
decision/checks.py           Deterministic rules — no LLM here
rag/vectorstore.py           Builds/loads the base-paper vector index
rag/ingest.py                Run to (re)build the index
tools/                       LangChain tools: email, hackathon search,
                              base paper retrieval, student report
agent/agent_setup.py         The single agent + system prompt + tool list
scheduler/jobs.py            One function per functionality — builds the
                              task string per flagged case, invokes the agent
```

## What's assumed / left for you to fill in

- **Which hackathon site(s)** to scrape periodically into
  `data/csv/hackathons_seed.csv` — not built here; `search_local_hackathons`
  just reads whatever's in that CSV. Add a scraper script when ready.
- **Function 3's entry point** — currently a Python function
  (`request_base_paper`), not wired to a web form/API yet. Wrap it in a
  small FastAPI/Flask endpoint if your team leader needs a submission form.
- **Faculty/HOD channel** — currently email only, per your earlier answer.
