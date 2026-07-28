import argparse
from orchestrator import run_for_student
from ingestion.load_data import load_students


def main():
    parser = argparse.ArgumentParser(description="Personalised Learning Agent")
    parser.add_argument("--student", type=str, help="Roll number to run the pipeline for")
    parser.add_argument("--all", action="store_true", help="Run for every student in students.csv")

    args = parser.parse_args()

    if args.student:
        run_for_student(args.student)
    elif args.all:
        for roll_no in load_students()["roll_no"]:
            run_for_student(roll_no)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
