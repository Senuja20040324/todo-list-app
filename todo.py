import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(title):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task added: {title}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet!")
        return
    print("\n📋 Your Tasks:")
    for task in tasks:
        status = "✔" if task["done"] else "✘"
        print(f"  [{status}] {task['id']}. {task['title']} ({task['created_at']})")

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

def main():
    while True:
        print("\n==== TO-DO APP ====")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")
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
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()