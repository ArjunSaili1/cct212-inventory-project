from random import randint
import sqlite3

stores = ["Toronto", "Mississauga", "Brampton", "Oakville", "Barrie"]
items = ["Soccer ball", "Hockey puck", "Golf club", "Football helmet",
         "Baseball glove", "Tennis racket", "Basketball", "Ping pong paddle"]

con = None

try:
    con = sqlite3.connect("python_db.db")
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Inventory")
    con.commit()

    cur.execute("""
                CREATE TABLE Inventory
                (Id integer PRIMARY KEY,
                Name text NOT NULL,
                Store text NOT NULL,
                Amount integer NOT NULL)
                """)
    con.commit()

    for store in stores:
        for item in items:
            cur.execute("""
                        INSERT INTO Inventory
                        (Name, Store, Amount) VALUES
                        (?, ?, ?)
                        """, (item, store, randint(0, 100)))
    con.commit()

except sqlite3.Error as e:

    print(f"Error {e.args[0]}")

finally:

    if con:
        con.close()
