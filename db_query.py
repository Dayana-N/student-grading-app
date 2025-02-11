import sqlite3

from app import main_menu


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
    except Exception as err:
        print(err)
        main_menu()
    return results
