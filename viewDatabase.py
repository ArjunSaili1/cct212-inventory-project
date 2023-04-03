import sqlite3

con = None

try:
    con = sqlite3.connect("python_db.db")
    cur = con.cursor()

    # cur.execute("""
    #            INSERT INTO Employees
    #            (Employee_Name, Employee_Email, Employee_Store_Name) VALUES
    #            ("Keenan", "KMAN11APPLEWOOD@gmail.com", "Nowhere")
    #            """)
    # con.commit()

    rows = cur.execute("SELECT * FROM Inventory")
    # rows = cur.execute("SELECT * FROM Employees")

    for row in rows:
        print(row)


except sqlite3.Error as e:

    print(f"Error {e.args[0]}")

finally:

    if con:
        con.close()
