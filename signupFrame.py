from inventoryFrame import InventoryFrame
import loginFrame
import sqlite3
from tkinter import *


def signup(root, username_entry, password_entry, store_variable, missing_label, exists_label):
    if username_entry.get() == "" or password_entry.get() == "":
        exists_label.place_forget()
        missing_label.place(anchor="center", relx=0.5, rely=0.55)
    else:
        missing_label.place_forget()
        con = None

        try:
            con = sqlite3.connect("python_db.db")
            cur = con.cursor()

            usernameData = cur.execute("SELECT Username FROM Employees")
            usernames = []

            for (username,) in usernameData:
                usernames.append(username)

            if username_entry.get().lower() in usernames:
                exists_label.place(anchor="center", relx=0.5, rely=0.55)
            else:
                cur.execute("""
                            INSERT INTO Employees (Username, Password, Store) 
                            VALUES (?, ?, ?)
                            """, (username_entry.get(), password_entry.get(), store_variable.get()))
                con.commit()
                InventoryFrame(root, store_variable.get()).build_tree()

        except sqlite3.Error as e:

            print(f"Error {e.args[0]}")

        finally:

            if con:
                con.close()


def back(root):
    loginFrame.make_login_frame(root)


def make_signup_frame(root):

    smallFont = ("courier", 16, "bold")
    largeFont = ("courier", 72, "bold")

    signupFrame = Frame(root, width=800, height=600)
    signupFrame.grid(row=0, column=0)

    companyLabel = Label(signupFrame, text="Sports World", font=largeFont)
    companyLabel.place(anchor="center", relx=0.5, rely=0.2)

    usernameFrame = Frame(signupFrame)
    usernameFrame.place(anchor="center", relx=0.5, rely=0.4)
    usernameLabel = Label(usernameFrame, text="Username: ", font=smallFont)
    usernameLabel.pack(side="left")
    usernameEntry = Entry(usernameFrame, font=smallFont, width=30)
    usernameEntry.pack(side="right")
    usernameEntry.focus_set()

    passwordFrame = Frame(signupFrame)
    passwordFrame.place(anchor="center", relx=0.5, rely=0.45)
    passwordLabel = Label(passwordFrame, text="Password: ", font=smallFont)
    passwordLabel.pack(side="left")
    passwordEntry = Entry(passwordFrame, font=smallFont, width=30, show="*")
    passwordEntry.pack(side="right")

    storeFrame = Frame(signupFrame)
    storeFrame.place(anchor="center", relx=0.5, rely=0.5)
    storeLabel = Label(storeFrame, text="store: ", font=smallFont)
    storeLabel.pack(side="left")
    stores = ["Toronto", "Mississauga", "Brampton", "Oakville", "Barrie"]
    storeVariable = StringVar(storeFrame)
    storeVariable.set(stores[0])
    storeMenu = OptionMenu(storeFrame, storeVariable, *stores)
    storeMenu.pack(side="right")

    signupButton = Button(signupFrame, text="Sign Up", font=smallFont, width=15, height=2, command=lambda: signup(root, usernameEntry, passwordEntry, storeVariable, missingLabel, existsLabel))
    signupButton.place(anchor="center", relx=0.5, rely=0.625)

    backButton = Button(signupFrame, text="< Back", font=smallFont, command=lambda: back(root))
    backButton.place(anchor="center", relx=0.06, rely=0.024)

    missingLabel = Label(signupFrame, text="The username or password you have entered is invalid please try again", font=smallFont, fg="red")
    existsLabel = Label(signupFrame, text="The username you have entered already exists please login", font=smallFont, fg="red")
