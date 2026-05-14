import tkinter as tk
from tkinter import *

root = tk.Tk()
root.title("Accountability App")
root.geometry('350x200')

lbl = Label(root, text="HI")
lbl.grid()

def clicked():
    lbl.configure(text="Clicked")

btn = Button(root, text="click",
             fg="red", command=clicked)

btn.grid(column=1, row=6)

root.mainloop()