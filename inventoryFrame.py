from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3


def validate_alpha(input) -> bool:
    if input.isalpha() or input == " " or " " in input:
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


def delete_from_db(inventory_table, location):
    con = sqlite3.connect("python_db.db")
    cursor = con.cursor()
    item_id = int(inventory_table.focus())
    try:
        query = cursor.execute("SELECT Name FROM Inventory "
                               f"WHERE Store='{location}' "
                               f"AND Id={item_id}")
        item_name = query.fetchone()
        response = messagebox.askokcancel("Delete Item",
                                          f"Are you sure you would like to "
                                          f"delete {item_name[0]} from your "
                                          f"inventory? This action cannot be "
                                          f"undone")
        if response:
            cursor.execute("DELETE FROM Inventory "
                           f"WHERE Store='{location}' "
                           f"AND Id={item_id}")
            con.commit()
        else:
            messagebox.showinfo("Delete Status",
                                "Operation Cancelled.")
    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")


def add_database(inventory_table, item_entry, amount_entry, location):
    try:
        con = sqlite3.connect("python_db.db")
        cur = con.cursor()
        if item_entry.get() and amount_entry.get():
            response = messagebox.askokcancel("Add Item",
            f"Do you wish to add the item '{item_entry.get()}' with amount "
            f"{amount_entry.get()} to the {location} Inventory?")

            if response:
                messagebox.showinfo("Add Status",
                                    "Item added.")
                cur.execute(
                    f"INSERT INTO Inventory(Name, Store, Amount) VALUES "
                    f"('{item_entry.get()}', '{location}', "
                    f"'{amount_entry.get()}')")
                con.commit()
                con.close()
                refresh_lists(inventory_table, location)
            else:
                messagebox.showinfo("Add Status",
                                    "Operation Cancelled.")
        else:
            messagebox.showinfo("Add Status",
                                "Please enter a valid Name/Amount!")
    except sqlite3.Error as e:

        print(f"Error {e.args[0]}")


def update_database(inventory_table, item_entry, amount_entry, add_button,
                    location):
    try:
        con = sqlite3.connect("python_db.db")
        cur = con.cursor()
        response = None
        if item_entry.get() and amount_entry.get():
            entry = cur.execute("SELECT Id,Name,Store,Amount FROM Inventory")
            for (id, name, store, amount) in entry:
                if id == int(inventory_table.focus()):
                    response = messagebox.askokcancel("Update Item",
                    f"Do you wish to update the item '{name}' with an amount "
                    f"of {amount} to '{item_entry.get()}' with an amount "
                    f"of {amount_entry.get()}?")

            if response:
                messagebox.showinfo("Update Status", "Item updated.")
                exec_statement = f"UPDATE Inventory SET Name = " \
                                 f"'{item_entry.get()}', Amount = '{amount_entry.get()}' WHERE Id = '{int(inventory_table.focus())}';"

                entry = cur.execute(exec_statement)

                inventory_table.delete(*inventory_table.get_children())
                con.commit()
                con.close()
                refresh_lists(inventory_table, location)
            else:
                messagebox.showinfo("Update Status", "Operation cancelled.")

            item_entry.delete(0, END)
            amount_entry.delete(0, END)
            add_button.config(text="Add Items to this store",
                              command=lambda: add_database(inventory_table,
                                                           item_entry,
                                                           amount_entry,
                                                           location))

    except sqlite3.Error as e:

        print(f"Error {e.args[0]}")


def update_init(inventory_table, item_entry, amount_entry, add_button,
                location):
    try:
        con = sqlite3.connect("python_db.db")
        cur = con.cursor()

        entry = cur.execute("SELECT Id,Name,Store,Amount FROM Inventory")

        for (id, name, store, amount) in entry:
            if id == int(inventory_table.focus()):
                item_entry.delete(0, END)
                item_entry.insert(0, name)
                amount_entry.delete(0, END)
                amount_entry.insert(0, amount)
                add_button.config(text="Update selected item in the store",
                                  command=lambda: update_database(
                                      inventory_table, item_entry, amount_entry,
                                      add_button, location))

        con.close()

    except sqlite3.Error as e:

        print(f"Error {e.args[0]}")


def refresh_lists(inventory_table, location):
    inventory_table.delete(*inventory_table.get_children())
    db = sqlite3.connect("python_db.db")
    db_cursor = db.cursor()
    rows = db_cursor.execute(
        f"SELECT * FROM Inventory WHERE Store='{location}'")
    item_count = 0
    for row in rows:
        item_count += 1
        inventory_table.insert(parent='', index="end", iid=row[0],
                               values=(row[0], row[1], row[3]))
    inventory_table["height"] = item_count


def make_inventory_frame(root, location):
    smallFont = ("arial", 16, "bold")
    labelFont = ("arial", 30, "bold")
    headingFont = ("arial", 15)
    inventory_frame = Frame(root, width=800, height=600)
    inventory_frame.grid(row=0, column=0)
    main_heading = Label(inventory_frame, text=f"{location} Store Items",
                         font=labelFont)
    item_name = Label(inventory_frame, text="Item: ",
                      font=headingFont)
    amount = Label(inventory_frame, text="Amount: ",
                   font=headingFont)
    vcmd = inventory_frame.register(
        validate_alpha)  # we have to wrap the command
    item_entry = Entry(inventory_frame, validate="key",
                       validatecommand=(vcmd, '%P'))
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
        add_button = Button(inventory_frame, text="Add Items to this store",
                            font=headingFont,
                            command=lambda: add_database(inventory_tree,
                                                         item_entry,
                                                         amount_entry,
                                                         location))
        delete_button = Button(inventory_frame, text="Delete Selected",
                               command=lambda: delete_from_db(inventory_tree,
                                                              location))
        update_button = Button(inventory_frame, text="Update Selected",
                               command=lambda: update_init(inventory_tree,
                                                           item_entry,
                                                           amount_entry,
                                                           add_button,
                                                           location))
        for row in rows:
            item_count += 1
            inventory_tree.insert(parent='', index="end", iid=row[0],
                                  values=(row[0], row[1], row[3]))
        inventory_tree["height"] = item_count
        inventory_tree.place(anchor="center", relwidth=0.85, relx=0.45,
                             rely=0.5)
        main_heading.place(anchor="nw", bordermode="outside",
                           in_=inventory_tree, relx=0, rely=0, y=-50)

        delete_button.place(anchor="center", relx=0.94, rely=0.46)
        update_button.place(anchor="center", relx=0.94, rely=0.54)

        item_name.place(anchor="e", relx=0.1, rely=0.80)
        item_entry.place(relwidth=0.325, relx=0.1, rely=0.79)
        amount.place(anchor="e", relx=0.55, rely=0.80)
        amount_entry.place(relwidth=0.325, relx=0.55, rely=0.79)
        add_button.place(anchor="center", relwidth=0.85, relx=0.45, rely=0.89)
    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
    return inventory_frame
