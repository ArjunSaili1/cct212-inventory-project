from inventoryFrame import make_inventory_frame
import signupFrame
import sqlite3
from tkinter import *


def login(root, username_entry, password_entry, valid_combos, dne_label, incorrect_label):
    usernameInput = username_entry.get()
    passwordInput = password_entry.get()
    if usernameInput.lower() in valid_combos:
        if passwordInput == valid_combos[usernameInput.lower()][0]:
            make_inventory_frame(root, valid_combos[usernameInput.lower()][1])
        else:
            dne_label.place_forget()
            incorrect_label.place(anchor="center", relx=0.5, rely=0.5)
    else:
        incorrect_label.place_forget()
        dne_label.place(anchor="center", relx=0.5, rely=0.5)


def signup(root):
    signupFrame.make_signup_frame(root)


def make_login_frame(root):

    validCombos = {}
    con = None

    try:
        con = sqlite3.connect("python_db.db")
        cur = con.cursor()

        loginData = cur.execute("SELECT Username,Password,Store FROM Employees")

        for (username, password, store) in loginData:
            validCombos[username] = (password, store)

    except sqlite3.Error as e:

        print(f"Error {e.args[0]}")

    finally:

        if con:
            con.close()

    smallFont = ("arial", 16, "bold")
    largeFont = ("arial", 72, "bold")

    loginFrame = Frame(root, width=800, height=600)
    loginFrame.grid(row=0, column=0)

    companyLabel = Label(loginFrame, text="Company Name", font=largeFont)
    companyLabel.place(anchor="center", relx=0.5, rely=0.2)

    usernameFrame = Frame(loginFrame)
    usernameFrame.place(anchor="center", relx=0.5, rely=0.4)
    usernameLabel = Label(usernameFrame, text="username: ", font=smallFont)
    usernameLabel.pack(side="left")
    usernameEntry = Entry(usernameFrame, font=smallFont, width=30)
    usernameEntry.pack(side="right")
    usernameEntry.focus_set()

    passwordFrame = Frame(loginFrame)
    passwordFrame.place(anchor="center", relx=0.5, rely=0.45)
    passwordLabel = Label(passwordFrame, text="password: ", font=smallFont)
    passwordLabel.pack(side="left")
    passwordEntry = Entry(passwordFrame, font=smallFont, width=30, show="*")
    passwordEntry.pack(side="right")

    loginButton = Button(loginFrame, text="Login", font=smallFont, width=15, height=2, command=lambda: login(root, usernameEntry, passwordEntry, validCombos, DNELabel, incorrectLabel))
    loginButton.place(anchor="center", relx=0.5, rely=0.575)

    signupButton = Button(loginFrame, text="Signup", font=smallFont, width=15, height=2, command=lambda: signup(root))
    signupButton.place(anchor="center", relx=0.5, rely=0.95)

    DNELabel = Label(loginFrame, text="The username you have entered does not exist please try again or press signup", font=smallFont, fg="red")
    incorrectLabel = Label(loginFrame, text="The password you have entered is incorrect please try again", font=smallFont, fg="red")
