import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def get_priority():
    print("\nSelect Priority:")
    print("  1. 🔴 High")
    print("  2. 🟡 Medium")
    print("  3. 🟢 Low")
    choice = input("Choose (1/2/3): ")
    priorities = {"1": "High", "2": "Medium", "3": "Low"}
    return priorities.get(choice, "Medium")

def get_due_date():
    while True:
        due_date = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ").strip()
        if due_date == "":
            return None  # No due date
        try:
            datetime.strptime(due_date, "%Y-%m-%d")  # Validate format
            return due_date
        except ValueError:
            print("❌ Invalid format! Please use YYYY-MM-DD (e.g. 2026-05-10)")

def check_due_status(due_date):
    if not due_date:
        return ""
    today = datetime.now().date()
    due = datetime.strptime(due_date, "%Y-%m-%d").date()
    diff = (due - today).days
    if diff < 0:
        return "⚠️ Overdue!"
    elif diff == 0:
        return "⏰ Due Today!"
    elif diff <= 3:
        return f"⚡ Due in {diff} day(s)"
    else:
        return f"📅 {due_date}"

def add_task(title):
    tasks = load_tasks()
    priority = get_priority()
    due_date = get_due_date()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(task)
    save_tasks(tasks)
    due_info = f" | Due: {due_date}" if due_date else ""
    print(f"✅ Task added: [{priority}] {title}{due_info}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet!")
        return

    # Sort by priority
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks.sort(key=lambda x: priority_order.get(x["priority"], 2))

    print("\n📋 Your Tasks:")
    print("  " + "-" * 75)
    for task in tasks:
        status = "✔ Done" if task["done"] else "✘ Todo"
        priority = task.get("priority", "Medium")
        emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(priority, "🟡")
        due_status = check_due_status(task.get("due_date"))
        print(f"  ID: {task['id']}  {emoji}{priority:<8} | {status:<8} | {task['title']:<25} | {due_status}")
    print("  " + "-" * 75)

def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"🎉 Task {task_id} marked as done!")
            return
    print("Task not found.")

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print(f"🗑️ Task {task_id} deleted.")

def show_overdue():
    tasks = load_tasks()
    today = datetime.now().date()
    overdue = []
    for task in tasks:
        if task.get("due_date") and not task["done"]:
            due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            if due < today:
                overdue.append(task)
    if not overdue:
        print("✅ No overdue tasks!")
    else:
        print(f"\n⚠️ Overdue Tasks ({len(overdue)}):")
        for task in overdue:
            print(f"  ❗ [{task['id']}] {task['title']} - was due {task['due_date']}")

def main():
    while True:
        print("\n==== TO-DO APP ====")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Show Overdue Tasks")
        print("6. Exit")
        choice = input("Choose: ")

        if choice == "1":
            title = input("Task title: ")
            add_task(title)
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            task_id = int(input("Task ID to complete: "))
            complete_task(task_id)
        elif choice == "4":
            task_id = int(input("Task ID to delete: "))
            delete_task(task_id)
        elif choice == "5":
            show_overdue()
        elif choice == "6":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()