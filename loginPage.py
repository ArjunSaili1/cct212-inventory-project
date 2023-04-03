from tkinter import *

font = ("arial", 16, "bold")
largeFont = ("arial", 72, "bold")


def login(button):
    button.config(bg="red", fg="black")


def forgot_password():
    pass


def signup():
    pass


root = Tk()
root.title("Login")
root.geometry("800x600")
root.resizable(False, False)

companyLabel = Label(root, text="Company Name", font=largeFont)

nameLabel = Label(root, text="name", font=font)
nameEntry = Entry(root, justify="center", font=font, width=30)
nameEntry.focus_set()

passwordLabel = Label(root, text="password", font=font)
passwordEntry = Entry(root, justify="center", font=font, width=30)

login = Button(root, text="Login", font=font, width=15, height=2)
forgotPassword = Button(root, text="Forgot Password?", font=font, width=15, height=2)
signup = Button(root, text="Signup", font=font, width=15, height=2)

# clickMe = Button(root, bg="blue", fg="yellow", text="Click Me", width=25,
#                 height=5, command=lambda: change(clickMe))

companyLabel.place(anchor="center", relx=0.5, rely=0.25)
nameLabel.place(anchor="center", relx=0.5, rely=0.4)
nameEntry.place(anchor="center", relx=0.5, rely=0.44)
passwordLabel.place(anchor="center", relx=0.5, rely=0.5)
passwordEntry.place(anchor="center", relx=0.5, rely=0.54)

login.place(anchor="center", relx=0.5, rely=0.64)
forgotPassword.place(anchor="center", relx=0.4, rely=0.95)
signup.place(anchor="center", relx=0.6, rely=0.95)

root.mainloop()
