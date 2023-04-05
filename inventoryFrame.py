from tkinter import *


def make_inventory_frame(root, location):

    inventoryFrame = Frame(root, width=800, height=600)
    inventoryFrame.grid(row=0, column=0)

    test = Label(text=location)
    test.place(anchor="center", relx=0.5, rely=0.5)

    return inventoryFrame
