from time import strftime
from datetime import datetime, timedelta

import tkinter as tk
from tkinter import *
from tkinter import messagebox

# main window
root = tk.Tk()
root.title("Accountability App")
root.geometry('1000x500')

previous_tasks=[]
today_tasks=[]
today_times = []

def add_task():
    task = task_entry.get()
    if task:
        if not today_times or (datetime.now() - today_times[-1]) >= timedelta(hours=1):
            today_times.append(datetime.now())
            today_tasks.append(task)
            task_listbox.insert(tk.END, task)
            task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Come back later!")  
    else:
        messagebox.showwarning("Warning", "Enter something!")  

def check():
    string = "CLOCK IN"
    if today_times:
        if (datetime.now() - today_times[-1]) < timedelta(hours=1):
            
    next.config(text=string)

def time():
    string = strftime('%H:%M:%S %p')
    clock.config(text=string)
    clock.after(1000, time)
    clock.after(1000, check)

# clock 
clock = Label(root)
clock.pack(anchor="center")
time()

# next time
next = Label(root, text="CLOCK IN!")
next.pack(anchor="center")
check()

# input field
task_entry = tk.Entry(root, width=30)
task_entry.pack(pady=10)

# submit button
add_button = tk.Button(root, text="Add", command=add_task)
add_button.pack()

# today's list
task_listbox = tk.Listbox(root, width=40, height=15)
task_listbox.pack(pady=10)

root.mainloop()