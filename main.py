from loginFrame import make_login_frame
from tkinter import *

root = Tk()

root.title("Company Name")
root.geometry("800x600")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

make_login_frame(root)

root.mainloop()
