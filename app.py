import sqlite3

from rich.console import Console
from rich.table import Table

from tables import create_dbtables

console = Console()


def validate_name(name_input):
    """
    Validates the name input
    """
    if not name_input.strip():
        return "Name cannot be empty"
    elif not name_input.isalpha():
        return "Invalid input. Name must include alpabet letters"
    elif len(name_input) <= 2 or len(name_input) > 50:
        return "Name must be between 2 and 50 characters"
    else:
        return "Valid"


def validate_age(age):
    """
    Validates user input for age
    """
    if age.isdigit() and int(age) > 0 and int(age) <= 120:
        return "Valid"
    else:
        return "Age must be whole number between 1 and 120"


def get_student_details(curr_f_name=None, curr_l_name=None, curr_age=None):
    """
    Gets user input and returns first_name, last_name and age
    """
    while True:
        first_name = input("Enter student's first name: ")
        f_name_validated = validate_name(first_name)
        if f_name_validated != "Valid":
            print(f_name_validated)
            continue
        else:
            break

    while True:
        last_name = input("Enter student's last name: ")
        l_name_validated = validate_name(last_name)
        if l_name_validated != "Valid":
            print(l_name_validated)
            continue
        else:
            break

    while True:
        age = input("Enter student's age: ")
        age_validated = validate_age(age)
        if age_validated != "Valid":
            print(age_validated)
            continue
        else:
            break
    return first_name, last_name, int(age)


def add_student():
    """
    Add new student to tbStudents table (id, first_name, last_name, age)
    """

    f_name, l_name, age = get_student_details()
    con = sqlite3.connect("dbStudentRecords.db")
    cursor = con.cursor()
    cursor.execute(f"""
    INSERT INTO tbStudents (first_name, last_name, age) VALUES ("{f_name}", "{l_name}", {age})
    """)
    print(f"{f_name}, {l_name}, {age} added to db")
    con.commit()
    con.close()


def display_all_students():
    """
    Displays all students in a table, returns array with student ids
    """

    con = sqlite3.connect("dbStudentRecords.db")
    cursor = con.cursor()
    cursor.execute("""SELECT * FROM tbStudents""")
    all_students = cursor.fetchall()
    con.close()

    student_ids = []

    table = Table(title="All Students")
    table.add_column("ID")
    table.add_column("First Name")
    table.add_column("Last Name")
    table.add_column("Age")

    for student in all_students:
        student_ids.append(student[0])
        table.add_row(str(student[0]), student[1], student[2], str(student[3]))

    console.print(table)
    return student_ids


def update_student():
    student_ids = display_all_students()

    while True:
        student_id = input(
            "Please enter the id of the student you wish to update: ")
        if student_id.isdigit() and int(student_id) in student_ids:
            print(student_id)
            print("valid")
            break
        else:
            print("Invalid ID")
            continue

    con = sqlite3.connect("dbStudentRecords.db")
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM tbStudents WHERE id = {student_id}")
    student = cursor.fetchone()

    new_first_name, new
    con.close()
    print(student)


def delete_student():
    pass


def manage_students():
    console.print("Manage Students")
    console.print("1. Add Student")
    console.print("2. Update Student")
    console.print("3. Delete Student")
    console.print("4. Back to Main Menu")
    console.print("5. Exit")

    while True:
        user_input = input("Enter your choice: ")
        if user_input.isdigit():
            user_option = int(user_input)
            if user_option == 5:
                quit()
            elif user_option == 4:
                main_menu()
                break
            elif user_option == 1:
                add_student()
                break
            elif user_option == 2:
                update_student()
                break
            elif user_option == 3:
                delete_student()
                break
            else:
                print("Invalid option selected")
        else:
            print("Please select a valid option")


def view_modules():

    con = sqlite3.connect('dbStudentRecords.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tbModules")
    modules = cursor.fetchall()
    con.close()

    # Display the records in a table
    table = Table(title="Modules", style="cyan")
    table.add_column("Module ID")
    table.add_column("Module Name")

    for module in modules:
        table.add_row(str(module[0]), module[1])

    console.print(table)
    back_to_menu()


def back_to_menu():
    console.print("Press 1. To go back to the main menu", style="bold")
    console.print("Press 2. To exit", style="bold")
    while True:
        user_input = input("Enter your choice: ")
        if user_input.isdigit():
            user_input = int(user_input)
            if user_input == 1:
                main_menu()
                break
            elif user_input == 2:
                quit()
                break
            else:
                console.print("Invalid option selected", style="bold")
        else:
            console.print("Please select a valid option", style="bold")


def view_records():
    """
    View records in the database
    student_records = {student_id:}
    """
    con = sqlite3.connect('dbStudentRecords.db')
    cursor = con.cursor()
    cursor.execute("""SELECT tbStudents.id, tbStudents.first_name, tbStudents.last_name, tbModules.name, tbResults.marks, tbResults.results
                        FROM tbStudents LEFT JOIN tbResults ON tbStudents.id = tbResults.student_id
                        LEFT JOIN tbModules ON tbResults.module_id = tbModules.id""")
    students = cursor.fetchall()
    print(students)
    con.close()

    # Display the records in a table
    table = Table(title="Student Records", style="cyan")
    table.add_column("Student ID")
    table.add_column("Name")
    table.add_column("Module")
    table.add_column("Marks")
    table.add_column("Results")

    for student in students:
        table.add_row(str(student[0]), f"{student[1]} {student[2]}", student[3] or "", str(
            student[4] or ""), student[5] or "")

    console.print(table)
    back_to_menu()


def main_menu():
    """
    Main menu for the application
    """
    while True:
        console.print("Please enter one of the following options: ")
        console.print("1. View Records")
        console.print("2. Manage Students")
        console.print("3. View Modules")
        console.print("4. Add Marks")
        console.print("5. Generate Report")
        console.print("6. Exit")

        user_input = input("Enter your choice: ")
        if user_input.isdigit():
            user_option = int(user_input)
            if user_option == 6:
                quit()
            elif user_option == 1:
                view_records()
                break
            elif user_option == 2:
                manage_students()
                break
            elif user_option == 3:
                print("manage Modules")
                view_modules()
            elif user_option == 4:
                print("Add Marks")
            elif user_option == 5:
                print("Generate Report")
            else:
                print("Invalid option selected")
        else:
            print("Please select a valid option")


def main():
    create_dbtables()
    print('Tables created successfully from main')
    main_menu()


if __name__ == "__main__":
    main()
