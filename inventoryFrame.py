from tkinter import *
from tkinter import ttk
import sqlite3


def make_inventory_frame(root, location):
    inventory_frame = Frame(root)
    inventory_frame.grid(row=0, column=0)

    try:
        db = sqlite3.connect("python_db.db")
        db_cursor = db.cursor()
        rows = db_cursor.execute(
            f"SELECT * FROM Inventory WHERE Store='{location}'")
        inventory_tree = ttk.Treeview(inventory_frame, show="headings")
        inventory_tree['columns'] = ("ID", "Item Name", "Count")
        inventory_tree.column("ID", anchor=CENTER, stretch=NO, width=100)
        inventory_tree.column("Item Name", anchor=CENTER, stretch=NO, width=300)
        inventory_tree.column("Count", anchor=CENTER, stretch=NO, width=200)
        inventory_tree.heading("ID", text="ID", anchor=W)
        inventory_tree.heading("Item Name", text="Item", anchor=CENTER)
        inventory_tree.heading("Count", text="Count ", anchor=W)
        item_count = 0
        for row in rows:
            item_count += 1
            inventory_tree.insert(parent='', index="end", iid=row[0],
                                  values=(row[0], row[1], row[3]))
        inventory_tree["height"] = item_count
        inventory_tree.pack()
    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
    return inventory_frame
