import sqlite3

con = None

try:
    con = sqlite3.connect("python_db.db")
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Employees")
    con.commit()

    cur.execute("""
                CREATE TABLE Employees 
                (Id integer PRIMARY KEY,
                Username text NOT NULL,
                Password text NOT NULL,
                Store text NOT NULL)
                """)
    con.commit()

except sqlite3.Error as e:

    print(f"Error {e.args[0]}")

finally:

    if con:
        con.close()
