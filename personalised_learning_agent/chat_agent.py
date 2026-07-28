from ingestion.load_data import (
    load_students,
    load_marks,
    load_attendance,
    load_backlog,
)
from rag.retriever import semantic_search
from utils.llm_client import generate


def get_student_context(roll_no: str) -> str:
    students = load_students()
    marks = load_marks()
    attendance = load_attendance()
    backlog = load_backlog()

    student_row = students[students["roll_no"] == roll_no]
    student_marks = marks[marks["roll_no"] == roll_no]
    student_attendance = attendance[
        attendance["roll_no"] == roll_no
    ]
    student_backlog = backlog[backlog["roll_no"] == roll_no]

    if student_row.empty:
        raise ValueError(f"Student {roll_no} was not found.")

    return f"""
Student details:
{student_row.to_string(index=False)}

Marks:
{student_marks.to_string(index=False)}

Attendance:
{student_attendance.to_string(index=False)}

Backlogs:
{student_backlog.to_string(index=False)}
"""


def answer_question(roll_no: str, question: str) -> str:
    student_context = get_student_context(roll_no)

    resources = semantic_search(question, k=3)

    resource_context = "\n\n".join(
        [
            f"Resource {index + 1}:\n"
            f"Content: {content}\n"
            f"Metadata: {metadata}"
            for index, (content, metadata) in enumerate(resources)
        ]
    )

    system_prompt = """
You are a personalised learning assistant for college students.

Answer the student's question using:
1. Their academic records
2. Their marks and attendance
3. Their backlogs
4. Retrieved learning resources

Give a clear, practical and personalised answer.

Do not invent marks, attendance values, subjects, deadlines or resources.
If the available information is insufficient, clearly say so.
"""

    user_prompt = f"""
Student roll number: {roll_no}

Student academic information:
{student_context}

Relevant retrieved learning resources:
{resource_context}

Student question:
{question}
"""

    return generate(
        system_prompt,
        user_prompt,
        max_tokens=1000,
    )


def start_chat() -> None:
    print("\nPersonalised Learning Agent")
    print("---------------------------")

    roll_no = input("Enter your roll number: ").strip()

    print("\nType your questions below.")
    print("Type 'exit' to stop the chat.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit", "stop"}:
            print("Agent: Goodbye!")
            break

        if not question:
            print("Agent: Please enter a question.")
            continue

        try:
            answer = answer_question(roll_no, question)
            print(f"\nAgent: {answer}\n")

        except ValueError as error:
            print(f"\nAgent: {error}\n")
            break

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    start_chat()