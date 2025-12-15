import csv
import json
import os
from datetime import datetime
# ----------------------------------
# CREATE FILES WITH HEADERS (ONCE)
# ----------------------------------2
def initialize_files():
    if not os.path.exists("students.csv"):
        with open("students.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Roll", "Name", "Department", "Year"])
    if not os.path.exists("marks.csv"):
        with open("marks.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Roll", "Subject", "Marks"])
# ----------------------------------
# ADD STUDENT DETAILS
# ----------------------------------
def add_student():
    roll = input("Enter Roll No: ")
    name = input("Enter Name: ")
    department = input("Enter Department: ")
    year = input("Enter Year of joining: ")

    with open("students.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([roll, name, department, year])

    print("Student details added successfully!\n")


# ----------------------------------
# ADD MARKS
# ----------------------------------
def add_marks():
    roll = input("Enter Roll No: ")
    subject = input("Enter Subject: ")
    marks = input("Enter Marks: ")

    with open("marks.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([roll, subject, marks])

    print("Marks added successfully!\n")


# ----------------------------------
# LOG ATTENDANCE
# ----------------------------------
def log_attendance():
    roll = input("Enter Roll No: ")
    status = input("Present or Absent: ")

    with open("attendance.txt", "a") as f:
        f.write(f"{datetime.now().date()} - Roll:{roll} - {status}\n")

    print("Attendance logged successfully!\n")


# ----------------------------------
# ASSIGN PROJECT
# ----------------------------------
def assign_project():
    roll = input("Enter Roll No: ")
    project = input("Enter Project Name: ")
    completed = input("Completed? (yes/no): ")

    try:
        with open("projects.json", "r") as f:
            data = json.load(f)
    except:
        data = {}

    data[roll] = {
        "project": project,
        "completed": completed
    }

    with open("projects.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Project assigned successfully!\n")


# ----------------------------------
# SEARCH STUDENT REPORT
# ----------------------------------
def search_student():
    search_roll = input("Enter Roll No to search: ")
    print("\n----- STUDENT REPORT -----")

    # Student Details
    with open("students.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Roll"] == search_roll:
                print(f"Name: {row['Name']}")
                print(f"Department: {row['Department']}")
                print(f"Year: {row['Year']}")

    # Marks + Average
    total = 0
    count = 0
    with open("marks.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Roll"] == search_roll:
                marks = int(row["Marks"])
                total += marks
                count += 1
                result = "PASS" if marks >= 35 else "FAIL"
                print(f"Subject: {row['Subject']} | Marks: {marks} | {result}")

    if count > 0:
        avg = total / count
        print(f"Average Marks: {avg:.2f}")

    # Project Status
    try:
        with open("projects.json", "r") as f:
            data = json.load(f)
            if search_roll in data:
                print(
                    f"Project: {data[search_roll]['project']} | Completed: {data[search_roll]['completed']}"
                )
    except:
        pass

    print("---------------------------\n")


# ----------------------------------
# GRADE CALCULATION
# ----------------------------------
def calculate_grade(avg):
    if avg >= 80:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 35:
        return "C"
    else:
        return "FAIL"


# ----------------------------------
# DEPARTMENT-WISE REPORT
# ----------------------------------
def department_wise_report():
    dept = input("Enter Department Name: ")
    print(f"\n--- Department Wise Report ({dept}) ---")

    students = {}

    with open("students.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Department"].lower() == dept.lower():
                students[row["Roll"]] = row["Name"]

    if not students:
        print("No students found in this department.\n")
        return

    for roll, name in students.items():
        total = 0
        count = 0

        with open("marks.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Roll"] == roll:
                    total += int(row["Marks"])
                    count += 1

        if count > 0:
            avg = total / count
            grade = calculate_grade(avg)
            print(f"Roll: {roll} | Name: {name} | Avg: {avg:.2f} | Grade: {grade}")
        else:
            print(f"Roll: {roll} | Name: {name} | No marks data")

    print("----------------------------------\n")


# ----------------------------------
# MENU SYSTEM
# ----------------------------------
def menu():
    initialize_files()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. Add Marks")
        print("3. Log Attendance")
        print("4. Assign Project")
        print("5. Search Student Report")
        print("6. Department Wise Report")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_marks()
        elif choice == "3":
            log_attendance()
        elif choice == "4":
            assign_project()
        elif choice == "5":
            search_student()
        elif choice == "6":
            department_wise_report()
        elif choice == "7":
            print("Exiting... Bye!")
            break
        else:
            print("Invalid choice! Try again.\n")
# ----------------------------------
# RUN PROGRAM
# ----------------------------------
menu()
