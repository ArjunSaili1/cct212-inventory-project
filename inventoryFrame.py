from tkinter import *
from tkinter import ttk
import sqlite3


def validate_alpha(input) -> bool:
    if input.isalpha() or input == " ":
        return True
    elif input == "":
        return True
    else:
        return False


def validate_digit(input):
    if input.isdigit():
        return True
    elif input == "":
        return True
    else:
        return False


def make_inventory_frame(root, location):
    smallFont = ("arial", 16, "bold")
    labelFont = ("arial", 30, "bold")
    headingFont = ("arial", 15,)
    inventory_frame = Frame(root, width=800, height=600)
    inventory_frame.grid(row=0, column=0)
    main_heading = Label(inventory_frame, text=f"{location} Store Items", font=labelFont)
    add_button = Button(inventory_frame, text="Add Items to this store", font=headingFont)
    delete_button = Button(inventory_frame, text="Delete Selected")
    update_button = Button(inventory_frame, text="Update Selected")
    item_name = Label(inventory_frame, text="Item: ",
                         font=headingFont)
    amount = Label(inventory_frame, text="Amount: ",
                      font=headingFont)
    vcmd = inventory_frame.register(validate_alpha)  # we have to wrap the command
    item_entry = Entry(inventory_frame, validate="key", validatecommand=(vcmd, '%P'))
    vcmd2 = inventory_frame.register(
        validate_digit)  # we have to wrap the command
    amount_entry = Entry(inventory_frame, validate="key",
                       validatecommand=(vcmd2, '%P'))
    try:
        db = sqlite3.connect("python_db.db")
        db_cursor = db.cursor()
        rows = db_cursor.execute(
            f"SELECT * FROM Inventory WHERE Store='{location}'")
        inventory_tree = ttk.Treeview(inventory_frame, show="headings")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=headingFont, )
        inventory_tree['columns'] = ("ID", "Item Name", "Count")
        inventory_tree.column("ID", anchor=CENTER, minwidth=100)
        inventory_tree.column("Item Name", anchor=CENTER, minwidth=300)
        inventory_tree.column("Count", anchor=CENTER, minwidth=200)
        inventory_tree.heading("ID", text="ID", anchor=W)
        inventory_tree.heading("Item Name", text="Item", anchor=CENTER)
        inventory_tree.heading("Count", text="Count ", anchor=W)
        item_count = 0
        for row in rows:
            item_count += 1
            inventory_tree.insert(parent='', index="end", iid=row[0],
                                  values=(row[0], row[1], row[3]))
        inventory_tree["height"] = item_count
        inventory_tree.place(anchor="center", relwidth=0.85, relx=0.45, rely=0.5)
        main_heading.place(anchor="nw", bordermode="outside", in_=inventory_tree, relx=0, rely=0, y=-50)

        delete_button.place(anchor="center", relx=0.94, rely=0.46)
        update_button.place(anchor="center", relx=0.94, rely=0.54)

        item_name.place(anchor="e",  relx=0.1, rely=0.80)
        item_entry.place(relwidth=0.325, relx=0.1, rely=0.79)
        amount.place(anchor="e", relx=0.55, rely=0.80)
        amount_entry.place(relwidth=0.325, relx=0.55, rely=0.79)
        add_button.place(anchor="center", relwidth=0.85, relx=0.45, rely=0.89)
    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
    return inventory_frame
