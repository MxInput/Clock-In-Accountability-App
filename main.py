from time import strftime
from datetime import datetime, timedelta

import csv
import os

import math

import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import *
from functools import partial
from tkinter.font import Font

# main window
root = tk.Tk()
root.title("Clock In: Accountability App")
root.geometry('1000x600')

style = ttk.Style()
style.configure("style.Treeview", rowheight=100, wraplength=10, highlightthickness=0, bd=0, font=('"Segoe UI', 12))
style.configure("style.Treeview.Heading", font=('Segoe UI', 16,'bold')) # Modify the font of the headings
style.layout("style.Treeview", [('style.Treeview.treearea', {'sticky': 'nswe'})])

today_window = None
past_window = None

today_tasks=[]
today_times = []

def initialize_data():
    file_name = 'data.csv'
    found_file = os.path.exists(file_name)

    field_names = ['datetime', 'entry']

    with open(file_name, mode='a') as file:
        writer = csv.DictWriter(file, field_names)
        if not found_file:
            writer.writeheader()
        else:
            read_data()
    file.close()

def read_data():
    file_name = 'data.csv'

    with open(file_name, mode='r') as file:
        csv_file = csv.DictReader(file)
        format = '%Y-%m-%d %H:%M:%S.%f'
        for line in csv_file:
            if datetime.strptime(line['datetime'], format).date() == datetime.today().date():
                today_tasks.insert(-1, line['entry'])
                today_times.insert(-1, datetime.strptime(line['datetime'], format))

initialize_data()

def motion_handler(tree, event):
    f = Font(font=('Segoe UI', 16))
    # A helper function that will wrap a given value based on column width
    def adjust_newlines(val, width, pad=0):
        if not isinstance(val, str):
            return val
        else:
            words = val.split()
            lines = [[],]
            for word in words:
                line = lines[-1] + [word,]
                if f.measure(' '.join(line)) < (width - pad):
                    lines[-1].append(word)
                else:
                    lines[-1] = ' '.join(lines[-1])
                    lines.append([word,])

            if isinstance(lines[-1], list):
                lines[-1] = ' '.join(lines[-1])

            return '\n'.join(lines)

    if (event is None) or (tree.identify_region(event.x, event.y) == "separator"):
        col_widths = [tree.column(cid)['width'] for cid in tree['columns']]

        for iid in tree.get_children():
            new_vals = []
            for (v,w) in zip(tree.item(iid)['values'], col_widths):
                new_vals.append(adjust_newlines(v, w))
            tree.item(iid, values=new_vals)



def close_today_menu():
    global today_window

    today_window.destroy()
    today_window = None

def open_today_menu():
    global today_window 

    if today_window is None:
        today_window = tk.Toplevel(root)
        today_window.title("Today's Entries")
        today_window.geometry("1000x600")
        today_window.protocol("WM_DELETE_WINDOW", close_today_menu)

        Label(today_window, text="Today's Entries", font=("Segoe UI Semibold", 40)).pack(pady=20)
    
    tree_view = ttk.Treeview(today_window, height=5,style="style.Treeview", selectmode="none")
    tree_view.pack(side='left', expand=True, fill=BOTH, padx=(22,5), pady=(0,24))

    verscrlbar = ttk.Scrollbar(today_window,
                               orient='vertical',
                               command = tree_view.yview)
    
    verscrlbar.pack(side="right", fill='x')
    tree_view.configure(xscrollcommand=verscrlbar.set)
   
    tree_view["columns"] = ("1", "2")
    tree_view['show'] = 'headings'

    tree_view.column("1", width = 200, anchor ='c')
    tree_view.column("2", width = 700, anchor ='c')

    tree_view.heading("1", text="Time")
    tree_view.heading("2", text="Entry")

    for x in range(len(today_tasks)):
        count = "L" + str(x+1)
        tree_view.insert("", END, text=count,
                         values=(today_times[x].strftime('%H:%M:%S %p'), today_tasks[x]))

    tree_view.bind('<B1-Motion>', partial(motion_handler, tree_view))
    motion_handler(tree_view, None)   

def close_past_menu():
    global past_window

    past_window.destroy()
    past_window = None

def open_past_menu():
    global past_window

    if past_window is None:
        past_window = tk.Toplevel(root)
        past_window.title("Past Entries")
        past_window.geometry("1000x600")
        past_window.protocol("WM_DELETE_WINDOW", close_past_menu)

        Label(past_window, text="Past Entries", font=("Segoe UI Semibold", 40)).pack(pady=20)

def add_task():
    task = task_entry.get("1.0", "end-1c")
    if task:
        if not today_times or (datetime.now() - today_times[-1]) >= timedelta(hours=1):
            today_times.append(datetime.now())
            today_tasks.append(task)
            task_entry.delete("1.0", "end")
            text_count.config(text="0 / 300")
            with open('data.csv', 'a', newline='') as csv_file:
                field_names = ['datetime', 'entry']
                csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)

                keys = ['datetime', 'entry']
                values = [datetime.now(), task]
                d = {k: v for k, v in zip(keys, values)}

                csv_writer.writerow(d)
            csv_file.close()
                
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
add_button = tk.Button(root, text="ADD", command=add_task, font=("Segoe UI", 20), relief="solid",borderwidth=4)
add_button.pack(side=LEFT, padx=10, expand=True, fill=X)

today_btn = tk.Button(root, text="VIEW TODAY'S ENTRIES", command=open_today_menu, font=("Segoe UI", 20), relief="solid",borderwidth=4)
today_btn.pack(side=LEFT, padx=20, expand=True, fill=X)

previous_btn = tk.Button(root, text="VIEW PAST DAYS", command=open_past_menu, font=("Segoe UI", 20), relief="solid",borderwidth=4)
previous_btn.pack(side=LEFT, padx=10, expand=True, fill=X)

root.mainloop()