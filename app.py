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
        input_message = f"Enter student's first name ({curr_f_name}): " if curr_f_name else "Enter student's first name: "
        first_name = input(input_message) or curr_f_name
        f_name_validated = validate_name(first_name)
        if f_name_validated != "Valid":
            print(f_name_validated)
            continue
        else:
            break

    while True:
        input_message = f"Enter student's last name ({curr_l_name}): " if curr_l_name else "Enter student's last name: "
        last_name = input(input_message) or curr_l_name
        l_name_validated = validate_name(last_name)
        if l_name_validated != "Valid":
            print(l_name_validated)
            continue
        else:
            break

    while True:
        input_message = f"Enter student's age ({curr_age}): " if curr_age else "Enter student's age: "
        age = input(input_message) or curr_age
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
    console.print(f"{f_name}, {l_name}, {age} added to db", style="green")
    con.commit()
    con.close()
    back_to_menu()


def get_all_students():
    """
    Gets all students from the database, returns list of tuples with each student record and list of ids
    """
    con = sqlite3.connect("dbStudentRecords.db")
    cursor = con.cursor()
    cursor.execute("""SELECT * FROM tbStudents""")
    all_students = cursor.fetchall()
    con.close()
    return all_students


def get_all_student_ids(all_students):
    """
    Loops through all students and returns an array with existing Ids
    """
    student_ids = []
    for student in all_students:
        student_ids.append(student[0])

    return student_ids


def display_all_students(all_students):
    """
    Displays all students in a table
    """
    # student_ids = []

    table = Table(title="All Students", style="cyan")
    table.add_column("ID")
    table.add_column("First Name")
    table.add_column("Last Name")
    table.add_column("Age")

    for student in all_students:
        table.add_row(str(student[0]), student[1], student[2], str(student[3]))

    console.print(table)


def update_student():
    """
    Displays list of all students,
    takes user input (id) for the student to be updated,
    updates the record in the database
    """
    all_students = get_all_students()
    student_ids = get_all_student_ids(all_students)
    display_all_students(all_students)

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

    new_first_name, new_last_name, new_age = get_student_details(
        student[1], student[2], str(student[3]))
    cursor.execute(
        f"""UPDATE tbStudents SET first_name = "{new_first_name}", last_name = "{new_last_name}", age = "{new_age}" WHERE id = {student_id}""")
    print(f"Record Updated - {new_first_name, new_last_name, new_age}")
    con.commit()
    con.close()
    # display the new student list
    all_students = get_all_students()
    display_all_students(all_students)
    back_to_menu()


def delete_confirmation():
    while True:
        console.print(
            "Are you sure you wish to delete this record? This action cannot be reversed. Y/N", style="red")
        user_input = input()
        if user_input.lower() == "y":
            return True

        elif user_input.lower() == "n":
            return False
        else:
            console.print("Invalid Input. Please Enter Y or N", style="red")
            continue


def delete_student():
    all_students = get_all_students()
    student_ids = get_all_student_ids(all_students)
    display_all_students(all_students)

    while True:
        student_id = input(
            "Please enter the id of the student you wish to delete or quit to go back to main menu: ")
        if student_id.lower() == "quit":
            main_menu()
            return
        if student_id.isdigit() and int(student_id) in student_ids:
            print(student_id)
            print("valid")
            break
        else:
            print("Invalid ID")
            continue

    # user_confirmation = delete_confirmation()
    if not delete_confirmation():
        console.print("Deletion canceled", style="yellow")
        manage_students()
    else:
        con = sqlite3.connect("dbStudentRecords.db")
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(f""" DELETE from tbStudents WHERE id = {student_id}""")
        con.commit()
        con.close()

        console.print("Record Deleted!", style="green")
        main_menu()


def manage_students():
    console.print("Manage Students")
    console.print("1. View all students")
    console.print("2. Add Student")
    console.print("3. Update Student")
    console.print("4. Delete Student")
    console.print("5. Back to Main Menu")
    console.print("6. Exit")

    while True:
        user_input = input("Enter your choice: ")
        if user_input.isdigit():
            user_option = int(user_input)
            if user_option == 6:
                quit()
            elif user_option == 5:
                main_menu()
                break
            elif user_option == 1:
                all_students = get_all_students()
                display_all_students(all_students)
                back_to_menu()
                break
            elif user_option == 2:
                add_student()
                break
            elif user_option == 3:
                update_student()
                break
            elif user_option == 4:
                delete_student()
                break
            else:
                print("Invalid option selected")
        else:
            print("Please select a valid option")


def get_modules():
    con = sqlite3.connect('dbStudentRecords.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tbModules")
    modules = cursor.fetchall()
    con.close()
    return modules


def get_modules_ids(all_modules):
    modules_ids = []

    for module in all_modules:
        modules_ids.append(module[0])

    return modules_ids


def display_modules(modules):

    # Display the records in a table
    table = Table(title="Modules", style="cyan")
    table.add_column("Module ID")
    table.add_column("Module Name")

    for module in modules:
        table.add_row(str(module[0]), module[1])

    console.print(table)


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


def calculate_result(mark):
    """
    Calculate the grade based on the marks
    """
    if mark >= 0 and mark < 50:
        return "Unsuccessful"
    elif mark <= 64:
        return "Pass"
    elif mark <= 79:
        return "Merit"
    elif mark >= 80 and mark <= 100:
        return "Distinction"
    else:
        return "Invalid"


def validate_user_input_id(list_ids):
    """
    Takes user input, checks if it is valid and if it exists in the list of IDs
    """

    while True:
        user_input_id = input(
            "Please enter id or quit to go back to main menu: ")
        if user_input_id.lower() == "quit":
            main_menu()
            return

        if user_input_id.isdigit() and int(user_input_id) in list_ids:
            print(user_input_id)
            print("valid")
            break
        else:
            print("Invalid ID")
            continue

    return user_input_id


def add_marks():
    """
    Adds marks for selected student
    """
    all_students = get_all_students()
    display_all_students(all_students)
    student_ids = get_all_student_ids(all_students)
    student_id = validate_user_input_id(student_ids)
    if not student_id:
        return

    all_modules = get_modules()
    display_modules(all_modules)
    module_ids = get_modules_ids(all_modules)
    module_id = validate_user_input_id(module_ids)
    if not module_id:
        return

    while True:
        mark_input = input("Please enter the mark. 0 - 100: ")
        if mark_input.isdigit() and int(mark_input) >= 0 and int(mark_input) <= 100:
            break
        else:
            print("Invalid Input")
    marks = int(mark_input)
    grade = calculate_result(marks)

    con = sqlite3.connect("dbStudentRecords.db")
    cursor = con.cursor()
    cursor.execute(
        f"""SELECT * FROM tbResults WHERE student_id = {student_id} and module_id = {module_id}""")
    result = cursor.fetchone()
    if result:
        cursor.execute(
            f"""UPDATE tbResults SET marks = {marks}, results = '{grade}' WHERE student_id = {student_id} and module_id = {module_id} """)
    else:
        print(result)
        cursor.execute(
            f"""INSERT INTO tbResults (student_id, module_id, marks, results) VALUES ("{student_id}", "{module_id}", "{mark_input}", "{grade}") """)
    con.commit()
    con.close()

    console.print("Marks added successfully", style="green")

    print(f"{student_id}, {module_id}, {mark_input}, {grade}")

    while True:
        console.print("Do you want to add more marks? Y/N: ")
        user_answer = input()
        if user_answer.lower() == "y":
            add_marks()
            break
        elif user_answer.lower() == "n":
            main_menu()
            break
        else:
            print("Invalid input.")


def get_student_results():
    """
    Get all student results
    """
    con = sqlite3.connect("dbStudentRecords.db")
    cursor = con.cursor()
    cursor.execute("""SELECT tbStudents.id, tbStudents.first_name, tbStudents.last_name, tbStudents.age, tbModules.name, tbResults.marks, tbResults.results
                    FROM tbResults
                    LEFT JOIN tbStudents ON tbStudents.id = tbResults.student_id
                    LEFT JOIN tbModules ON tbModules.id = tbResults.module_id""")
    data = cursor.fetchall()
    con.close()
    print(data)
    return data


def generate_report(data):
    """
    Generate report for all students
    """
    student_reports = {}

    # Organize data by student
    for student_id, student_first_name, student_last_name, student_age, module_name, marks, grade in data:
        if student_id not in student_reports:
            student_reports[student_id] = {
                "name": student_first_name + " " + student_last_name,
                "age": student_age,
                "modules": []
            }

        student_reports[student_id]["modules"].append(
            (module_name, marks, grade))

    # Write reports to individual files
    for student_id, student_info in student_reports.items():
        filename = f"Student_{student_id}_Report.txt"
        with open(filename, "w") as file:
            file.write(f"Student ID: {student_id}\n")
            file.write(f"Name: {student_info['name']}\n")
            file.write(f"Age: {student_info['age']}\n\n")
            file.write("Module Results:\n")

            for module_name, marks, grade in student_info["modules"]:
                file.write(f"  {module_name}: Marks={marks}, Grade={grade}\n")

        print(f"Generated report for {student_info['name']} -> {filename}")


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
                modules = get_modules()
                display_modules(modules)
                back_to_menu()
                break
            elif user_option == 4:
                print("Add Marks")
                add_marks()
                break
            elif user_option == 5:
                print("Generate Report")
                data = get_student_results()
                generate_report(data)
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
