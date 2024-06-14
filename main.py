from student_management import (
    register_user, login_user,
    add_student, view_students, search_student,
    update_student, remove_student
)

def main():
    print("Hello, Welcome to Studility!")

    # Register new users
    register = input("Do you want to register a new user? (y/n) ")
    if register.lower() == 'y':
        username = input("Enter username: ")
        password = input("Enter password: ")
        role = input("Enter role (student/teacher/admin): ")
        register_user(username, password, role)

    # Login
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = login_user(username, password)
    if user:
        user_id, role = user
        print(f"Logged in as {role}")

        while True:
            if role == 'student':
                print("1. View Courses")
                print("2. Enroll in Course")
                # ... (add more student options)
            elif role == 'teacher':
                print("1. Add Student")
                print("2. View Students")
                print("3. Search Student")
                print("4. Update Student")
                print("5. Remove Student")
            elif role == 'admin':
                print("1. Register User")
                # ... (add more admin options)

            choice = input("Enter your choice: ")
            if choice == '1':
                if role == 'teacher':
                    name = input("Enter Student Name: ")
                    age = int(input("Enter Student Age: "))
                    grade = input("Enter Student Grade: ")
                    add_student(user_id, name, age, grade)
                elif role == 'admin':
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    user_role = input("Enter role (student/teacher/admin): ")
                    register_user(username, password, user_role)
            elif choice == '2':
                if role == 'teacher':
                    view_students(user_id)
                # ... (handle other options)
            elif choice == '3':
                if role == 'teacher':
                    student_id = int(input("Enter Student ID: "))
                    search_student(user_id, student_id)
            elif choice == '4':
                if role == 'teacher':
                    student_id = int(input("Enter Student ID: "))
                    name = input("Enter new name (or press Enter to skip): ")
                    age = input("Enter new age (or press Enter to skip): ")
                    grade = input("Enter new grade (or press Enter to skip): ")
                    update_student(user_id, student_id, name=name if name else None, age=int(age) if age else None, grade_name=grade if grade else None)
            elif choice == '5':
                if role == 'teacher':
                    student_id = int(input("Enter Student ID: "))
                    remove_student(user_id, student_id)

            logout = input("Do you want to logout? (y/n) ")
            if logout.lower() == 'y':
                break

    else:
        print("Login failed.")

if __name__ == "__main__":
    main()