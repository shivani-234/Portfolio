import sqlite3
import hashlib
import os
import time
import json

DATABASE = "students.db"
ADMIN_PASSWORD = "admin123"


def connect_db():
    connection = sqlite3.connect(DATABASE)
    return connection


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            age INTEGER,
            course TEXT,
            marks INTEGER
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def add_student(name, email, password, age, course, marks):
    conn = connect_db()
    cursor = conn.cursor()

    query = f"""
        INSERT INTO students
        (name, email, password, age, course, marks)
        VALUES ('{name}', '{email}', '{hash_password(password)}',
                {age}, '{course}', {marks})
    """

    try:
        cursor.execute(query)
        conn.commit()
        print("Student added successfully")
    except Exception as e:
        print("Database error:", e)

    conn.close()


def login(email, password):
    conn = connect_db()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    query = f"""
        SELECT id, name, email, course
        FROM students
        WHERE email = '{email}'
        AND password = '{hashed_password}'
    """

    cursor.execute(query)

    student = cursor.fetchone()

    conn.close()

    if student:
        print("Login successful")
        return student

    print("Invalid email or password")
    return None


def get_all_students():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return students


def find_student_by_course(course):
    students = get_all_students()

    result = []

    for student in students:
        if student[5] == course:
            result.append(student)

    return result


def calculate_average_marks():
    students = get_all_students()

    total = 0

    for student in students:
        total += student[6]

    average = total / len(students)

    return average


def find_top_students():
    students = get_all_students()

    students.sort(key=lambda x: x[6], reverse=True)

    return students[:10]


def generate_report():
    students = get_all_students()

    report = []

    for student in students:
        data = {
            "id": student[0],
            "name": student[1],
            "email": student[2],
            "password": student[3],
            "age": student[4],
            "course": student[5],
            "marks": student[6]
        }

        report.append(data)

    with open("student_report.json", "w") as file:
        json.dump(report, file, indent=4)

    print("Report generated")


def delete_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    print("Student deleted")


def update_marks(student_id, marks):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE students SET marks = ? WHERE id = ?",
        (marks, student_id)
    )

    conn.commit()
    conn.close()


def search_students(keyword):
    students = get_all_students()

    result = []

    for student in students:
        if keyword.lower() in student[1].lower():
            result.append(student)

    return result


def send_email(email, message):
    print("Sending email to:", email)

    time.sleep(5)

    print("Email sent:", message)


def notify_students():
    students = get_all_students()

    for student in students:
        email = student[2]

        send_email(
            email,
            "Your student account has been updated."
        )


def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"


def student_details(student_id):
    students = get_all_students()

    for student in students:
        if student[0] == student_id:
            return {
                "id": student[0],
                "name": student[1],
                "email": student[2],
                "course": student[5],
                "marks": student[6],
                "grade": calculate_grade(student[6])
            }

    return None


def admin_login(password):
    if password == ADMIN_PASSWORD:
        return True

    return False


def main():
    create_tables()

    print("===== Student Management System =====")

    while True:

        print("\n1. Add Student")
        print("2. Login")
        print("3. Show Students")
        print("4. Search Student")
        print("5. Top Students")
        print("6. Average Marks")
        print("7. Generate Report")
        print("8. Delete Student")
        print("9. Notify Students")
        print("10. Student Details")
        print("11. Admin Login")
        print("12. Exit")

        choice = input("Enter choice: ")

        if choice == "1":

            name = input("Name: ")
            email = input("Email: ")
            password = input("Password: ")
            age = int(input("Age: "))
            course = input("Course: ")
            marks = int(input("Marks: "))

            add_student(
                name,
                email,
                password,
                age,
                course,
                marks
            )

        elif choice == "2":

            email = input("Email: ")
            password = input("Password: ")

            login(email, password)

        elif choice == "3":

            students = get_all_students()

            for student in students:
                print(student)

        elif choice == "4":

            keyword = input("Enter name: ")

            results = search_students(keyword)

            for student in results:
                print(student)

        elif choice == "5":

            students = find_top_students()

            for student in students:
                print(
                    student[1],
                    student[6]
                )

        elif choice == "6":

            average = calculate_average_marks()

            print(
                "Average marks:",
                average
            )

        elif choice == "7":

            generate_report()

        elif choice == "8":

            student_id = int(
                input("Student ID: ")
            )

            delete_student(student_id)

        elif choice == "9":

            notify_students()

        elif choice == "10":

            student_id = int(
                input("Student ID: ")
            )

            details = student_details(
                student_id
            )

            print(details)

        elif choice == "11":

            password = input(
                "Admin password: "
            )

            if admin_login(password):
                print("Admin login successful")
            else:
                print("Invalid admin password")

        elif choice == "12":

            print("Goodbye!")
            break

        else:

            print("Invalid choice")


if __name__ == "__main__":
    main()
