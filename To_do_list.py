import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import datetime
import threading
from plyer import notification

# File to store tasks
TASKS_FILE = "tasks.json"

# Load and save tasks
def load_tasks():
    return json.load(open(TASKS_FILE, "r")) if os.path.exists(TASKS_FILE) else []

def save_tasks():
    json.dump(tasks, open(TASKS_FILE, "w"), indent=4)

# Add or Edit a task
def manage_task(edit=False):
    selected = task_list.curselection()
    if edit and not selected:
        return messagebox.showwarning("Warning", "Select a task to edit!")

    task = tasks[selected[0]] if edit else {}
    task["name"] = simpledialog.askstring("Task", "Enter task description:", initialvalue=task.get("name", ""))
    task["due_date"] = simpledialog.askstring("Due Date", "YYYY-MM-DD (optional):", initialvalue=task.get("due_date", "No deadline"))
    task["priority"] = simpledialog.askstring("Priority", "High, Medium, Low:", initialvalue=task.get("priority", "Medium"))

    if task["name"]:
        if edit:
            tasks[selected[0]] = task
        else:
            tasks.append(task)
        update_task_list()
        save_tasks()
        check_notifications()

# Remove selected task
def remove_task():
    selected = task_list.curselection()
    if selected:
        tasks.pop(selected[0])
        update_task_list()
        save_tasks()

# Update task display
def update_task_list():
    task_list.delete(0, tk.END)
    today = datetime.date.today()

    for task in tasks:
        due, status = task["due_date"], "No Deadline"
        if due != "No deadline":
            try:
                days_left = (datetime.datetime.strptime(due, "%Y-%m-%d").date() - today).days
                status = "🔥 Due Today!" if days_left == 0 else f"📅 Due in {days_left} days" if days_left > 0 else "❌ Overdue!"
            except ValueError:
                status = "Invalid Date"

        task_list.insert(tk.END, f"{task['name']} | {due} | {task['priority']} | {status}")

# Send notifications for due tasks
def check_notifications():
    today = datetime.date.today().strftime("%Y-%m-%d")
    for task in tasks:
        if task["due_date"] == today:
            notification.notify(title="Task Reminder 🔔", message=f"'{task['name']}' is due today!", timeout=10)

# Auto-check notifications every minute
def auto_check():
    check_notifications()
    threading.Timer(60, auto_check).start()

# GUI Setup
root = tk.Tk()
root.title("Smart To-Do List ✅")

task_list = tk.Listbox(root, width=60, height=10)
task_list.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Add Task", command=lambda: manage_task(False)).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Edit Task", command=lambda: manage_task(True)).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Remove Task", command=remove_task).grid(row=0, column=2, padx=5)

tasks = load_tasks()
update_task_list()
auto_check()

root.mainloop()
