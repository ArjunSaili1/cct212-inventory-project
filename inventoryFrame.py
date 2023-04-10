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


class InventoryFrame:
    def __init__(self, root, location):
        self.connection = sqlite3.connect("python_db.db")
        self.cursor = self.connection.cursor()
        self.location = location
        self.frame = Frame(root, width=800, height=600)
        self.frame.grid(row=0, column=0)
        self.tree = None
        self.tree_font = ("arial", 15)
        self.label_font = ("courier", 30, "bold")
        self.button_font = ("courier", 15, "bold")
        self.heading_font = ("courier", 15, "bold")

    def build_tree(self):
        main_heading = Label(self.frame, text=f"{self.location} Store Items",
                             font=self.label_font)
        item_name = Label(self.frame, text="Item: ",
                          font=self.heading_font)
        amount = Label(self.frame, text="Amount: ",
                       font=self.heading_font)
        vcmd = self.frame.register(
            validate_alpha)  # we have to wrap the command
        item_entry = Entry(self.frame, validate="key",
                           validatecommand=(vcmd, '%P'))
        vcmd2 = self.frame.register(
            validate_digit)  # we have to wrap the command
        amount_entry = Entry(self.frame, validate="key",
                             validatecommand=(vcmd2, '%P'))
        try:
            rows = self.cursor.execute(
                f"SELECT * FROM Inventory WHERE Store='{self.location}'")
            self.tree = ttk.Treeview(self.frame, show="headings", height=150)
            style = ttk.Style()
            style.configure("Treeview.Heading", font=self.tree_font)
            self.tree['columns'] = ("ID", "Item Name", "Count")
            self.tree.column("ID", anchor=CENTER, minwidth=50)
            self.tree.column("Item Name", anchor=CENTER, minwidth=100)
            self.tree.column("Count", anchor=CENTER, minwidth=50)
            self.tree.heading("ID", text="ID", anchor=W)
            self.tree.heading("Item Name", text="Item", anchor=CENTER)
            self.tree.heading("Count", text="Count ", anchor=W)
            add_button = Button(self.frame, text="Add Items to this store",
                                font=self.heading_font,
                                command=lambda: self.add_database(
                                    item_entry.get(),
                                    amount_entry.get()))
            delete_button = Button(self.frame, text="Delete Selected",
                                   command=self.delete_from_db,
                                   font=self.button_font)
            update_button = Button(self.frame, text="Update Selected",
                                   font=self.button_font,
                                   command=lambda: self.update_init(item_entry,
                                                                    amount_entry,
                                                                    add_button))
            for row in rows:
                self.tree["height"] += 1
                self.tree.insert(parent='', index="end", iid=row[0],
                                 values=(row[0], row[1], row[3]))
            self.tree.place(anchor="center", relwidth=0.75, relx=0.4, rely=0.5,
                            height=200)
            main_heading.place(anchor="nw", bordermode="outside", in_=self.tree,
                               relx=0, rely=0, y=-50)
            delete_button.place(anchor="center", relx=0.89, rely=0.46)
            update_button.place(anchor="center", relx=0.89, rely=0.54)
            item_name.place(anchor="e", relx=0.1, rely=0.80)
            item_entry.place(relwidth=0.325, relx=0.1, rely=0.79)
            amount.place(anchor="e", relx=0.55, rely=0.80)
            amount_entry.place(relwidth=0.325, relx=0.55, rely=0.79)
            add_button.place(anchor="center", relwidth=0.85, relx=0.45,
                             rely=0.89)
            scrollbar = Scrollbar(orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.place(anchor="nw", rely=0.12, in_=self.tree, height=166)
        except sqlite3.Error as e:
            print(f"Error {e.args[0]}")
        return self.frame

    def add_database(self, item, amount):
        try:
            if item and amount:
                response = messagebox.askokcancel("Add Item",
                                                  f"Do you wish to add the item '{item}' with amount "
                                                  f"{amount} to the {self.location} Inventory?")

                if response:
                    messagebox.showinfo("Add Status",
                                        "Item added.")
                    self.cursor.execute(
                        f"INSERT INTO Inventory(Name, Store, Amount) VALUES "
                        f"('{item}', '{self.location}', "
                        f"'{amount}')")
                    self.connection.commit()
                    self.refresh_lists()
                else:
                    messagebox.showinfo("Add Status",
                                        "Operation Cancelled.")
            else:
                messagebox.showinfo("Add Status",
                                    "Please enter a valid Name/Amount!")
        except sqlite3.Error as e:
            print(f"Error {e.args[0]}")

    def delete_from_db(self):
        try:
            item_id = int(self.tree.focus())
            try:
                query = self.cursor.execute("SELECT Name FROM Inventory "
                                            f"WHERE Store='{self.location}' "
                                            f"AND Id={item_id}")
                item_name = query.fetchone()
                response = messagebox.askokcancel("Delete Item",
                                              f"Are you sure you would like to "
                                              f"delete {item_name[0]} from your "
                                              f"inventory? This action cannot be "
                                              f"undone")
                if response:
                    self.cursor.execute("DELETE FROM Inventory "
                                    f"WHERE Store='{self.location}' "
                                    f"AND Id={item_id}")
                    self.connection.commit()
                    self.refresh_lists()
                else:
                    messagebox.showinfo("Delete Status",
                                    "Operation Cancelled.")

            except sqlite3.Error as e:
                print(f"Error {e.args[0]}")

        except:
            print("test")

    def refresh_lists(self):
        self.tree.delete(*self.tree.get_children())
        rows = self.cursor.execute(
            f"SELECT * FROM Inventory WHERE Store='{self.location}'")
        item_count = 0
        for row in rows:
            item_count += 1
            self.tree.insert(parent='', index="end", iid=row[0],
                             values=(row[0], row[1], row[3]))
        self.tree["height"] = item_count

    def update_init(self, item_entry, amount_entry, add_button):
        try:
            entry = self.cursor.execute("SELECT Id,Name,Store,Amount "
                                        "FROM Inventory")
            for (id, name, store, amount) in entry:
                if id == int(self.tree.focus()):
                    item_entry.delete(0, END)
                    item_entry.insert(0, name)
                    amount_entry.delete(0, END)
                    amount_entry.insert(0, amount)
                    add_button.config(text="Update selected item in the store",
                                      command=lambda: self.update_database(item_entry,
                                                                           amount_entry,
                                                                           add_button))
        except sqlite3.Error as e:
            print(f"Error {e.args[0]}")

    def update_database(self, item_entry, amount_entry, add_button):
        new_name = item_entry.get()
        new_amount = amount_entry.get()
        item_id = int(self.tree.focus())
        try:
            response = None
            if new_name and new_amount:
                entry = self.cursor.execute(f"SELECT Name,Store,Amount FROM Inventory WHERE Id={item_id}")
                for (name, store, amount) in entry:
                    response = messagebox.askokcancel("Update Item",
                                                      f"Do you wish to update the item '{name}' with an amount "
                                                      f"of {amount} to '{new_name}' with an amount "
                                                      f"of {new_amount}?")
                if response:
                    messagebox.showinfo("Update Status", "Item updated.")
                    exec_statement = f"UPDATE Inventory SET Name = " \
                                     f"'{new_name}', Amount = '{new_amount}' " \
                                     f"WHERE Id = '{item_id}';"
                    self.cursor.execute(exec_statement)
                    self.tree.delete(*self.tree.get_children())
                    self.connection.commit()
                    self.refresh_lists()
                else:
                    messagebox.showinfo("Update Status", "Operation cancelled.")
                item_entry.delete(0, END)
                amount_entry.delete(0, END)
                add_button.config(text="Add Items to this store",
                                  command=lambda: self.add_database(new_name,
                                                                    new_amount))
        except sqlite3.Error as e:
            print(f"Error {e.args[0]}")


