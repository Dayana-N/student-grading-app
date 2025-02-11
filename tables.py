import sqlite3


def create_dbtables():
    """Creates tables in the database"""
    con = sqlite3.connect('dbStudentRecords.db')
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbStudents  (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER NOT NULL)''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbModules  (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS tbResults (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                module_id INTEGER NOT NULL,
                marks INTEGER NOT NULL,
                results TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES tbStudents(id) ON DELETE CASCADE,
                FOREIGN KEY (module_id) REFERENCES tbModules(id) ON DELETE CASCADE)''')

    con.commit()
    con.close()
