import sqlite3

con = None

try:
    con = sqlite3.connect("python_db.db")
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Employees")
    con.commit()

    cur.execute("""
                CREATE TABLE Employees 
                (Employee_Id integer PRIMARY KEY,
                Employee_Name text NOT NULL,
                Employee_Email text NOT NULL,
                Employee_Password text NOT NULL,
                Employee_Store_Name text NOT NULL)
                """)
    con.commit()

except sqlite3.Error as e:

    print(f"Error {e.args[0]}")

finally:

    if con:
        con.close()
