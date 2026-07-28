"""
The single agent that powers all 7 functionalities.

Design:
  - The decision layer (decision/checks.py) decides WHO/WHAT needs action,
    using hardcoded thresholds — no LLM involved there.
  - This agent is invoked ONCE PER FLAGGED CASE with a plain-language task
    description. It uses its tools to gather any extra context it needs
    (base papers, hackathon listings, student reports), drafts the message
    itself, and finishes by calling send_email to dispatch it.
"""
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import config
from tools.send_email_tool import send_email
from tools.hackathon_search_tool import search_local_hackathons, search_hackathons_live
from tools.base_paper_tool import retrieve_local_base_paper, search_arxiv_base_paper
from tools.student_report_tool import get_student_overall_performance

SYSTEM_PROMPT = """You are the Academic Performance Agent for an engineering college.

You support these functions, one invocation at a time based on the task
you are given:
1. Finding relevant hackathons and emailing suitable students.
2. Sending attendance-percentage reminders to students below the required threshold.
3. Sending base papers and required documents to a team leader based on a problem statement.
4. Alerting subject faculty about students who are performing poorly, ahead of exams.
5. Reporting a student's overall performance across all subjects.
6. Alerting the HOD when a subject's overall performance is low, with concrete
   suggestions to improve it (e.g. remedial classes, revised teaching pace, extra tutorials).
7. Reminding students/teams about incomplete work nearing its deadline
   (hackathon registrations, assignments, tasks).

Rules:
- You are given the flagged case (who/what triggered this) — do not re-decide
  whether it qualifies, that has already been determined deterministically.
- Use your tools to gather any extra context you need (base papers, hackathons,
  a student's full report) before writing the message.
- Always write a complete, professional, concise email body yourself.
- Always finish by calling send_email to actually deliver the message — do not
  just describe the email, send it.
- Address the correct recipient for the task (student, team leader, faculty, or HOD).
- For HOD alerts about low subject performance, always include 2-3 concrete
  suggested improvement actions.
"""

TOOLS = [
    send_email,
    search_local_hackathons,
    search_hackathons_live,
    retrieve_local_base_paper,
    search_arxiv_base_paper,
    get_student_overall_performance,
]


def build_agent_executor() -> AgentExecutor:
    llm = ChatOpenAI(
        model=config.OPENROUTER_MODEL,
        api_key=config.OPENROUTER_API_KEY,
        base_url=config.OPENROUTER_BASE_URL,
        temperature=0.3,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, TOOLS, prompt)
    return AgentExecutor(agent=agent, tools=TOOLS, verbose=True)
