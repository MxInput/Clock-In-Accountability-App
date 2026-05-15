from time import strftime
from datetime import datetime, timedelta

import math

import tkinter as tk
import tkinter.font
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

# main window
root = tk.Tk()
root.title("Clock In: Accountability App")
root.geometry('1000x600')

today_window = None

previous_tasks=[]
today_tasks=[]
today_times = []

def close_today_menu():
    global today_window

    today_window.destroy()
    today_window = None

def open_today_menu():
    global today_window 

    if today_window is None:
        today_window = tk.Toplevel(root)
        today_window.title("Today's Entries")
        today_window.geometry("250x150")
        today_window.protocol("WM_DELETE_WINDOW", close_today_menu)

        Label(today_window, text="Today's Entries", font=("Segoe UI", 11)).pack(pady=20)

def add_task():
    task = task_entry.get("1.0", "end-1c")
    if task:
        if not today_times or (datetime.now() - today_times[-1]) >= timedelta(hours=1):
            today_times.append(datetime.now())
            today_tasks.append(task)
            task_entry.delete("1.0", "end")
            text_count.config(text="0 / 300")
        else:
            messagebox.showwarning("Warning", "Come back later!")  
    else:
        messagebox.showwarning("Warning", "Enter something!")  

def check():
    string = "CLOCK IN"
    if today_times:
        if (datetime.now() - today_times[-1]) < timedelta(hours=1):
            target = today_times[-1] + timedelta(hours=1)
            diff = target - datetime.now()
            diff = diff.total_seconds()

            secs = math.floor(diff%60)
            mins = math.ceil(diff/60) - 1
            
            string = "Clock-in after " + str(mins) + " minutes " + str(secs) + " seconds"
    next.config(text=string) 

def time():
    string = strftime('%H:%M:%S %p')
    clock.config(text=string)
    clock.after(1000, time)
    clock.after(1000, check)

def limit_text(event):
    max_chars = 300
    text = task_entry.get("1.0", "end-1c")
    inputted_chars = len(text)
    string = str(inputted_chars) + " / " + str(max_chars)
    text_count.config(text=string)

    if len(text) >= max_chars and event.keysym not in ("BackSpace", "Delete"):
        return "break" 
    
def limit_paste(event):
    max_chars = 300
    text = task_entry.get("1.0", "end-1c")
    inputted_chars = len(text)
    clipboard = root.clipboard_get()

    if len(clipboard) > max_chars - inputted_chars:
        left_to_get = max_chars - inputted_chars 
        left_over = clipboard[:left_to_get]
        task_entry.insert(END, left_over)
    else:
        task_entry.insert(END, clipboard)
    text = task_entry.get("1.0", "end-1c")
    inputted_chars = len(text)
    string = str(inputted_chars) + " / " + str(max_chars)
    text_count.config(text=string)
    return "break"

# clock 
clock = Label(root, font=("Segoe UI Semibold", 40))
clock.pack(anchor="center")
time()

# next time
next = Label(root, text="CLOCK IN!", font=("Segoe UI", 20))
next.pack(anchor="center")
check()

# input field
task_entry = tk.Text(root, width=40, height=10, font=("Segoe UI", 11))
task_entry.pack(pady=10)

task_entry.bind("<KeyPress>", limit_text)
task_entry.bind("<KeyRelease>", limit_text)
task_entry.bind("<<Paste>>", limit_paste)

text_count = Label(root, text="0 / 300", font=("Segoe UI", 8))
text_count.pack(anchor="center")

# submit button
add_button = tk.Button(root, text="ADD", command=add_task, font=("Segoe UI", 20))
add_button.pack()

previous_btn = tk.Button(root, text="VIEW TODAY'S ENTRIES", command=open_today_menu, font=("Segoe UI", 20))
previous_btn.pack()

previous_btn = tk.Button(root, text="VIEW PAST DAYS", command=add_task, font=("Segoe UI", 20))
previous_btn.pack()

root.mainloop()