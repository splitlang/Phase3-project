import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('students.db')
c = conn.cursor()

# Create the tables if they don't exist
def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, grade_id INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS grades
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, role TEXT)''')
    conn.commit()

# User management functions
def register_user(username, password, role):
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    print("User registered successfully.")

def login_user(username, password):
    c.execute("SELECT id, role FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    if user:
        return user
    else:
        print("Invalid username or password.")
        return None

# Student management functions
def add_student(user_id, name, age, grade_name):
    # Check if the user has the 'teacher' or 'admin' role
    c.execute("SELECT role FROM users WHERE id=?", (user_id,))
    role = c.fetchone()[0]
    if role in ['teacher', 'admin']:
        # Get the grade ID
        grade_id = get_grade_id(grade_name)

        # Add the student
        c.execute("INSERT INTO students (name, age, grade_id) VALUES (?, ?, ?)", (name, age, grade_id))
        conn.commit()
        print("Student added successfully.")
    else:
        print("You don't have permission to add students.")

def view_students(user_id):
    # Check if the user has the 'teacher' or 'admin' role
    c.execute("SELECT role FROM users WHERE id=?", (user_id,))
    role = c.fetchone()[0]
    if role in ['teacher', 'admin']:
        c.execute("SELECT s.id, s.name, s.age, g.name FROM students s JOIN grades g ON s.grade_id = g.id")
        students = c.fetchall()
        if not students:
            print("No students found.")
        else:
            for student in students:
                print(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}")
    else:
        print("You don't have permission to view students.")

def search_student(user_id, student_id):
    # Check if the user has the 'teacher' or 'admin' role
    c.execute("SELECT role FROM users WHERE id=?", (user_id,))
    role = c.fetchone()[0]
    if role in ['teacher', 'admin']:
        c.execute("SELECT s.id, s.name, s.age, g.name FROM students s JOIN grades g ON s.grade_id = g.id WHERE s.id=?", (student_id,))
        student = c.fetchone()
        if student:
            print(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}")
        else:
            print("Student not found.")
    else:
        print("You don't have permission to search students.")

def update_student(user_id, student_id, name=None, age=None, grade_name=None):
    # Check if the user has the 'teacher' or 'admin' role
    c.execute("SELECT role FROM users WHERE id=?", (user_id,))
    role = c.fetchone()[0]
    if role in ['teacher', 'admin']:
        # Get the current student information
        c.execute("SELECT name, age, g.name FROM students s JOIN grades g ON s.grade_id = g.id WHERE s.id=?", (student_id,))
        current_info = c.fetchone()
        if current_info:
            current_name, current_age, current_grade = current_info

            # Update the student information
            new_name = name if name else current_name
            new_age = age if age else current_age

            # Get the new grade ID
            new_grade_id = get_grade_id(grade_name) if grade_name else get_grade_id(current_grade)

            c.execute("UPDATE students SET name=?, age=?, grade_id=? WHERE id=?", (new_name, new_age, new_grade_id, student_id))
            conn.commit()
            print("Student information updated successfully.")
        else:
            print("Student not found.")
    else:
        print("You don't have permission to update students.")

def remove_student(user_id, student_id):
    # Check if the user has the 'teacher' or 'admin' role
    c.execute("SELECT role FROM users WHERE id=?", (user_id,))
    role = c.fetchone()[0]
    if role in ['teacher', 'admin']:
        c.execute("DELETE FROM students WHERE id=?", (student_id,))
        if c.rowcount > 0:
            conn.commit()
            print("Student removed successfully.")
        else:
            print("Student not found.")
    else:
        print("You don't have permission to remove students.")

def get_grade_id(grade_name):
    c.execute("SELECT id FROM grades WHERE name=?", (grade_name,))
    grade_id = c.fetchone()
    if not grade_id:
        c.execute("INSERT INTO grades (name) VALUES (?)", (grade_name,))
        grade_id = c.lastrowid
        conn.commit()
    else:
        grade_id = grade_id[0]
    return grade_id

create_tables()