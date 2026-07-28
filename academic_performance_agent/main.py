"""
Entry point.

Usage:
    python main.py --run-now attendance
    python main.py --run-now deadlines
    python main.py --run-now faculty
    python main.py --run-now hod
    python main.py --run-now hackathons
    python main.py --run-now report --student S001
    python main.py --run-now base_paper --problem "smart irrigation system" \\
        --leader-name "Rahul Verma" --leader-email rahul.verma@example.edu

    python main.py                       # starts the recurring scheduler
"""
import argparse
from apscheduler.schedulers.blocking import BlockingScheduler

from agent.agent_setup import build_agent_executor
from scheduler import jobs


def start_scheduler(agent_executor):
    scheduler = BlockingScheduler()

    scheduler.add_job(lambda: jobs.job_attendance_reminder(agent_executor), "cron", hour=8, id="attendance")
    scheduler.add_job(lambda: jobs.job_pending_deadlines(agent_executor), "cron", hour=8, minute=30, id="deadlines")
    scheduler.add_job(lambda: jobs.job_pre_exam_faculty_alert(agent_executor), "cron", hour=9, id="faculty_alert")
    scheduler.add_job(lambda: jobs.job_hod_subject_alert(agent_executor), "cron", day_of_week="mon", hour=9, id="hod_alert")
    scheduler.add_job(lambda: jobs.job_hackathon_matching(agent_executor), "cron", day_of_week="mon", hour=10, id="hackathons")

    print("Scheduler started. Press Ctrl+C to exit.")
    scheduler.start()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-now",
        choices=["attendance", "deadlines", "faculty", "hod", "hackathons", "report", "base_paper"],
        help="Run one job immediately instead of starting the scheduler (useful for testing).",
    )
    parser.add_argument("--student", help="student_id, required for --run-now report")
    parser.add_argument("--problem", help="problem statement, required for --run-now base_paper")
    parser.add_argument("--leader-name")
    parser.add_argument("--leader-email")
    args = parser.parse_args()

    agent_executor = build_agent_executor()

    if args.run_now == "attendance":
        jobs.job_attendance_reminder(agent_executor)
    elif args.run_now == "deadlines":
        jobs.job_pending_deadlines(agent_executor)
    elif args.run_now == "faculty":
        jobs.job_pre_exam_faculty_alert(agent_executor)
    elif args.run_now == "hod":
        jobs.job_hod_subject_alert(agent_executor)
    elif args.run_now == "hackathons":
        jobs.job_hackathon_matching(agent_executor)
    elif args.run_now == "report":
        if not args.student:
            parser.error("--student is required for --run-now report")
        jobs.job_overall_performance_report(agent_executor, args.student)
    elif args.run_now == "base_paper":
        if not (args.problem and args.leader_name and args.leader_email):
            parser.error("--problem, --leader-name and --leader-email are required for --run-now base_paper")
        jobs.request_base_paper(agent_executor, args.problem, args.leader_name, args.leader_email)
    else:
        start_scheduler(agent_executor)


if __name__ == "__main__":
    main()
