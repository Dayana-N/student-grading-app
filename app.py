import sqlite3

from rich.console import Console
from rich.table import Table

from tables import create_dbtables

console = Console()


def execute_query(query, commit, fetch=None):
    """
    Execute database queries,
    takes in the query,
    commit: bool, indicates if changes need to be commited
    fetch: fetchone or fetchall based on the amount of results expected
    """
    try:
        con = sqlite3.connect("dbStudentRecords.db")
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(query)
        if fetch == "fetchone":
            results = cursor.fetchone()
        elif fetch == "fetchall":
            results = cursor.fetchall()
        else:
            results = ''

        if commit:
            con.commit()
        con.close()
        return results
    except Exception as err:
        print(err)
        main_menu()
    return


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
    query = f"""INSERT INTO tbStudents (first_name, last_name, age) VALUES ("{f_name}", "{l_name}", {age})"""
    execute_query(query, True)
    back_to_menu()


def get_all_students():
    """
    Gets all students from the database, returns list of tuples with each student record and list of ids
    """
    query = "SELECT * FROM tbStudents"
    fetch = "fetchall"
    all_students = execute_query(query, False, fetch)
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

    table = Table(title="All Students", style="cyan")
    table.add_column("ID")
    table.add_column("First Name")
    table.add_column("Last Name")
    table.add_column("Age")

    for student in all_students:
        table.add_row(str(student[0]), student[1], student[2], str(student[3]))

    console.print(table)


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


def update_student():
    """
    Displays list of all students,
    takes user input (id) for the student to be updated,
    updates the record in the database
    """
    # Gets all the students data from db, stores all ids in a list
    # displays the students in a table
    all_students = get_all_students()
    student_ids = get_all_student_ids(all_students)
    display_all_students(all_students)

    # validate user input for id to be updated
    student_id = validate_user_input_id(student_ids)
    if not student_id:
        return

    query = f"SELECT * FROM tbStudents WHERE id = {student_id}"
    student = execute_query(query, False, "fetchone")
    # gets the new details for the student, if no input, the value is unchanged
    new_first_name, new_last_name, new_age = get_student_details(
        student[1], student[2], str(student[3]))
    # updates the records in the db
    query = f"""UPDATE tbStudents SET first_name = "{new_first_name}", last_name = "{new_last_name}", age = "{new_age}" WHERE id = {student_id}"""
    execute_query(query, True)

    # display the new student list
    all_students = get_all_students()
    display_all_students(all_students)
    back_to_menu()


def delete_confirmation():
    """
    Asks the user for confirmation before record is deleted
    """
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
    """
    Function to delete students from the db
    """
    # gets all the students from db, puts all ids in a list, displays all the student data
    all_students = get_all_students()
    student_ids = get_all_student_ids(all_students)
    display_all_students(all_students)
    # validates user's choice for id to be deleted
    student_id = validate_user_input_id(student_ids)
    if not student_id:
        return
    # display delete confirmation menu, if users cancels the deletion is cancelled
    if not delete_confirmation():
        console.print("Deletion cancelled", style="yellow")
        manage_students()
    else:
        query = f""" DELETE from tbStudents WHERE id = {student_id}"""
        execute_query(query, True)
        console.print("Record Deleted!", style="green")
        main_menu()


def manage_students():
    """
    Manage students menu
    """
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
    """
    Gets all modules from the database
    """
    query = "SELECT * FROM tbModules"
    modules = execute_query(query, False, "fetchall")
    return modules


def get_modules_ids(all_modules):
    """
    Creates a list of ids
    """
    modules_ids = []

    for module in all_modules:
        modules_ids.append(module[0])

    return modules_ids


def display_modules(modules):
    """
    Displays the list modules in a table
    modules: list of tuples
    """
    # Display the records in a table
    table = Table(title="Modules", style="cyan")
    table.add_column("Module ID")
    table.add_column("Module Name")

    for module in modules:
        table.add_row(str(module[0]), module[1])

    console.print(table)


def back_to_menu():
    """
    Displays a menu to the user with options to go back to main menu or quit the program
    """
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


def display_records():
    """
    Gets records from the database and displays them in table
    """
    query = """SELECT tbStudents.id, tbStudents.first_name, tbStudents.last_name, tbModules.name, tbResults.marks, tbResults.results
                        FROM tbStudents LEFT JOIN tbResults ON tbStudents.id = tbResults.student_id
                        LEFT JOIN tbModules ON tbResults.module_id = tbModules.id"""
    students = execute_query(query, False, "fetchall")

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


def validate_input_marks():
    """
    Validate user input for marks
    """
    while True:
        mark_input = input("Please enter the mark. 0 - 100: ")
        if mark_input.isdigit() and int(mark_input) >= 0 and int(mark_input) <= 100:
            return int(mark_input)
        else:
            print("Invalid Input")


def add_more_marks_menu():
    """
    Menu to provide easy access to add marks function
    """
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


def add_marks():
    """
    Add/update marks for selected student
    """
    # Gets all student data from db and displays it into table
    all_students = get_all_students()
    display_all_students(all_students)
    # stores all student ids in a list
    student_ids = get_all_student_ids(all_students)
    # gets the user input for id and validates it
    student_id = validate_user_input_id(student_ids)

    if not student_id:
        return

    # Gets all modules from db and displays them into table
    all_modules = get_modules()
    display_modules(all_modules)
    # stores all modules id into list
    module_ids = get_modules_ids(all_modules)
    # gets user input for module id and validates it
    module_id = validate_user_input_id(module_ids)

    if not module_id:
        return

    # gets user input for marks and validates it
    mark_input = validate_input_marks()
    marks = int(mark_input)
    grade = calculate_result(marks)  # calculate the grade based on the mark

    # checks the database if the record for this mark exists
    # if it does then it updates the record, if it doesn't it creates the record
    query = f"""SELECT * FROM tbResults WHERE student_id = {student_id} and module_id = {module_id}"""
    result = execute_query(query, False, "fetchone")

    if result:
        query = f"""UPDATE tbResults SET marks = {marks}, results = '{grade}' WHERE student_id = {student_id} and module_id = {module_id} """
        execute_query(query, True)
    else:
        print(result)
        query = f"""INSERT INTO tbResults (student_id, module_id, marks, results) VALUES ("{student_id}", "{module_id}", "{mark_input}", "{grade}")"""
        execute_query(query, True)

    console.print("Marks added successfully", style="green")

    print(f"{student_id}, {module_id}, {mark_input}, {grade}")
    add_more_marks_menu()


def get_student_results():
    """
    Get all student results
    """
    query = """SELECT tbStudents.id, tbStudents.first_name, tbStudents.last_name, tbStudents.age, tbModules.name, tbResults.marks, tbResults.results
                    FROM tbResults
                    LEFT JOIN tbStudents ON tbStudents.id = tbResults.student_id
                    LEFT JOIN tbModules ON tbModules.id = tbResults.module_id"""
    data = execute_query(query, False, "fetchall")

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

    print(student_reports)
    write_report(student_reports)


def write_report(student_reports):
    """
    Write reports to individual files
    """

    for student_id, student_info in student_reports.items():
        filename = f"Student_{student_id}_Report.txt"
        with open(filename, "w") as file:
            file.write("       Certificate \n")
            file.write("============================\n")
            file.write(f"Name: {student_info['name']}\n")
            file.write(f"Age: {student_info['age']}\n\n")
            file.write("Module Results:\n")
            file.write("============================\n")

            for module_name, marks, grade in student_info["modules"]:
                file.write(f"{module_name}: {marks},      {grade}\n")
            file.write("=================================\n")
            file.write(f"     Overall grade: Grade \n")
            file.write("=================================\n")

            console.print(
                f"Generated report for {student_info['name']} - {filename}", style="cyan")


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
                display_records()
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
            elif user_option == 7:
                print("secret option number 7")
                break
            else:
                print("Invalid option selected")
        else:
            print("Please select a valid option")


def main():
    create_dbtables()
    main_menu()


if __name__ == "__main__":
    main()
