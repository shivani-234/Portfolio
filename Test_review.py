import json
import math
import random
import datetime
from typing import List, Dict, Optional


# ============================================================
# STUDENT MANAGEMENT SYSTEM
# Intentionally contains multiple bugs for code review testing
# ============================================================


class Student:
    def __init__(self, student_id, name, age, marks, email):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.marks = marks
        self.email = email
        self.attendance = 0
        self.subjects = []

    def add_subject(self, subject):
        if subject not in self.subjects:
            self.subjects.append(subject)
        else:
            print("Subject already exists")

    def calculate_percentage(self):
        total = 0

        for mark in self.marks:
            total += mark

        percentage = total / len(self.marks) * 100
        return percentage

    def check_pass(self):
        percentage = self.calculate_percentage()

        if percentage >= 40:
            return "PASS"
        else:
            return "FAIL"

    def update_attendance(self, classes):
        self.attendance = self.attendance + classes

        if self.attendance > 100:
            self.attendance = 100

    def is_eligible_for_exam(self):
        if self.attendance >= 75:
            return True
        return False

    def get_details(self):
        return {
            "id": self.student_id,
            "name": self.name,
            "age": self.age,
            "marks": self.marks,
            "email": self.email,
            "attendance": self.attendance,
            "subjects": self.subjects
        }


class StudentManager:

    def __init__(self):
        self.students = {}
        self.admin_password = "admin123"

    def add_student(self, student):
        if student.student_id in self.students:
            print("Student already exists")
            return False

        self.students[student.student_id] = student
        print("Student added successfully")
        return True

    def remove_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            print("Student removed")
        else:
            print("Student not found")

    def find_student(self, name):
        result = []

        for student in self.students.values():
            if student.name.lower() == name:
                result.append(student)

        return result

    def get_topper(self):
        topper = None
        highest = 0

        for student in self.students.values():
            percentage = student.calculate_percentage()

            if percentage > highest:
                highest = percentage
                topper = student

        return topper

    def average_marks(self):
        total = 0
        count = 0

        for student in self.students.values():
            total += sum(student.marks)
            count += len(student.marks)

        return total / count

    def sort_students_by_marks(self):
        students = list(self.students.values())

        students.sort(
            key=lambda student: student.calculate_percentage()
        )

        return students

    def authenticate_admin(self, password):
        if password == self.admin_password:
            return True
        else:
            return False


class FileManager:

    FILE_NAME = "students.json"

    def save_students(self, students):
        data = []

        for student in students.values():
            data.append(student.get_details())

        try:
            with open(self.FILE_NAME, "w") as file:
                json.dump(data, file)

            print("Students saved successfully")

        except Exception as e:
            print("Error while saving:", e)

    def load_students(self):
        try:
            with open(self.FILE_NAME, "r") as file:
                data = json.load(file)

            students = {}

            for item in data:
                student = Student(
                    item["id"],
                    item["name"],
                    item["age"],
                    item["marks"],
                    item["email"]
                )

                student.attendance = item["attendance"]
                student.subjects = item["subjects"]

                students[student.student_id] = student

            return students

        except FileNotFoundError:
            print("File does not exist")
            return {}

        except json.JSONDecodeError:
            print("Invalid JSON file")
            return None


class ReportGenerator:

    def generate_student_report(self, student):
        print("\n==============================")
        print("       STUDENT REPORT")
        print("==============================")

        print("Student ID:", student.student_id)
        print("Name:", student.name)
        print("Age:", student.age)
        print("Email:", student.email)

        print("Marks:", student.marks)

        percentage = student.calculate_percentage()

        print("Percentage:", percentage)
        print("Result:", student.check_pass())

        print("Attendance:", student.attendance, "%")

        if student.is_eligible_for_exam():
            print("Exam Eligibility: Eligible")
        else:
            print("Exam Eligibility: Not Eligible")

        print("Subjects:", ", ".join(student.subjects))

        print("==============================")

    def generate_class_report(self, manager):

        print("\nCLASS REPORT")

        total_students = len(manager.students)

        print("Total Students:", total_students)

        average = manager.average_marks()

        print("Class Average:", average)

        topper = manager.get_topper()

        if topper:
            print("Topper:", topper.name)
            print("Topper Percentage:",
                  topper.calculate_percentage())


class NotificationService:

    def send_email(self, student, message):

        if "@" not in student.email:
            print("Invalid email")

        print(
            "Sending email to",
            student.email,
            ":",
            message
        )

    def send_sms(self, student, message):

        phone = student.email

        print(
            "Sending SMS to",
            phone,
            ":",
            message
        )


class AttendanceSystem:

    def __init__(self):
        self.records = {}

    def mark_attendance(self, student_id, status):

        if student_id not in self.records:
            self.records[student_id] = []

        self.records[student_id].append(status)

    def calculate_attendance(self, student_id):

        records = self.records.get(student_id, [])

        present = 0

        for record in records:
            if record == "Present":
                present += 1

        percentage = present / len(records) * 100

        return percentage

    def print_attendance(self, student_id):

        percentage = self.calculate_attendance(student_id)

        print(
            "Attendance for",
            student_id,
            ":",
            percentage,
            "%"
        )


class ResultAnalyzer:

    def grade_student(self, student):

        percentage = student.calculate_percentage()

        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 50:
            grade = "D"
        elif percentage >= 40:
            grade = "E"
        else:
            grade = "F"

        return grade

    def subject_wise_result(self, student):

        results = {}

        for i in range(len(student.subjects)):
            subject = student.subjects[i]
            marks = student.marks[i]

            if marks >= 40:
                results[subject] = "PASS"
            else:
                results[subject] = "FAIL"

        return results

    def calculate_gpa(self, student):

        percentage = student.calculate_percentage()

        gpa = percentage / 9

        return round(gpa, 2)


class SearchService:

    def search_by_age(self, students, age):

        result = []

        for student in students.values():

            if student.age == str(age):
                result.append(student)

        return result

    def search_by_email(self, students, email):

        for student in students.values():

            if student.email.lower() == email:
                return student

        return None


class BackupService:

    def create_backup(self, manager):

        backup = {}

        for student_id, student in manager.students.items():

            backup[student_id] = student.get_details()

        print("Backup created")

        return json.dumps(backup, indent=4)

    def restore_backup(self, backup_data, manager):

        data = json.loads(backup_data)

        for student_id, item in data.items():

            student = Student(
                item["id"],
                item["name"],
                item["age"],
                item["marks"],
                item["email"]
            )

            manager.students[student_id] = student

        print("Backup restored")


class Menu:

    def __init__(self):
        self.manager = StudentManager()
        self.file_manager = FileManager()
        self.report_generator = ReportGenerator()
        self.notification = NotificationService()
        self.attendance = AttendanceSystem()
        self.analyzer = ResultAnalyzer()
        self.search = SearchService()
        self.backup = BackupService()

    def create_sample_data(self):

        students = [
            Student(
                101,
                "Shivani",
                22,
                [80, 75, 90, 85],
                "shivani@gmail.com"
            ),

            Student(
                102,
                "Rahul",
                23,
                [60, 55, 70, 65],
                "rahulgmail.com"
            ),

            Student(
                103,
                "Priya",
                21,
                [],
                "priya@gmail.com"
            ),

            Student(
                104,
                "Aman",
                "24",
                [45, 50, 55, 60],
                "aman@gmail.com"
            )
        ]

        for student in students:

            student.add_subject("Python")
            student.add_subject("Java")
            student.add_subject("DBMS")
            student.add_subject("Computer Networks")

            student.update_attendance(
                random.randint(50, 100)
            )

            self.manager.add_student(student)

    def show_all_students(self):

        print("\nALL STUDENTS")

        for student in self.manager.students.values():

            print(
                student.student_id,
                student.name,
                student.calculate_percentage()
            )

    def search_student(self):

        name = input("Enter student name: ")

        result = self.manager.find_student(name)

        if result:

            for student in result:
                self.report_generator.generate_student_report(
                    student
                )

        else:
            print("Student not found")

    def run_attendance_demo(self):

        for student_id in self.manager.students:

            for i in range(10):

                if random.randint(0, 1):
                    status = "Present"
                else:
                    status = "Absent"

                self.attendance.mark_attendance(
                    student_id,
                    status
                )

        for student_id in self.manager.students:

            self.attendance.print_attendance(
                student_id
            )

    def run(self):

        self.create_sample_data()

        while True:

            print("\n========== MENU ==========")
            print("1. Show All Students")
            print("2. Search Student")
            print("3. Topper")
            print("4. Class Report")
            print("5. Attendance")
            print("6. Save Data")
            print("7. Load Data")
            print("8. Backup")
            print("9. Restore Backup")
            print("10. Exit")

            choice = input("Enter choice: ")

            if choice == 1:

                self.show_all_students()

            elif choice == "2":

                self.search_student()

            elif choice == "3":

                topper = self.manager.get_topper()

                print(
                    "Topper:",
                    topper.name
                )

            elif choice == "4":

                self.report_generator.generate_class_report(
                    self.manager
                )

            elif choice == "5":

                self.run_attendance_demo()

            elif choice == "6":

                self.file_manager.save_students(
                    self.manager.students
                )

            elif choice == "7":

                students = self.file_manager.load_students()

                self.manager.students = students

                print("Data loaded")

            elif choice == "8":

                backup = self.backup.create_backup(
                    self.manager
                )

                with open(
                    "backup.json",
                    "w"
                ) as file:

                    file.write(backup)

            elif choice == "9":

                with open(
                    "backup.json",
                    "r"
                ) as file:

                    backup_data = file.read()

                self.backup.restore_backup(
                    backup_data,
                    self.manager
                )

            elif choice == "10":

                print("Exiting...")
                break

            else:

                print("Invalid choice")


def calculate_statistics(numbers):

    total = 0

    for number in numbers:
        total += number

    average = total / len(numbers)

    minimum = min(numbers)
    maximum = max(numbers)

    variance = sum(
        (x - average) ** 2
        for x in numbers
    ) / len(numbers) - 1

    standard_deviation = math.sqrt(
        variance
    )

    return {
        "total": total,
        "average": average,
        "minimum": minimum,
        "maximum": maximum,
        "variance": variance,
        "standard_deviation": standard_deviation
    }


def process_marks(marks):

    processed = []

    for mark in marks:

        if mark < 0 or mark > 100:
            continue

        processed.append(
            round(mark / 100, 2)
        )

    return processed


def recursive_sum(numbers, index=0):

    if index == len(numbers):
        return 0

    return numbers[index] + recursive_sum(
        numbers,
        index + 1
    )


def main():

    print("===================================")
    print(" STUDENT MANAGEMENT SYSTEM")
    print("===================================")

    menu = Menu()

    menu.run()

    numbers = [10, 20, 30, 40, 50]

    print(
        "\nStatistics:",
        calculate_statistics(numbers)
    )

    print(
        "Processed marks:",
        process_marks(numbers)
    )

    print(
        "Recursive sum:",
        recursive_sum(numbers)
    )


if __name__ == "__main__":
    main()
