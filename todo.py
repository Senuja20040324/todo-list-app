import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        content = f.read().strip()
        if not content:  # ← handles empty file
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
    return priorities.get(choice, "Medium")  # Default: Medium

def add_task(title):
    tasks = load_tasks()
    priority = get_priority()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": priority,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task added: [{priority}] {title}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet!")
        return

    # Sort by priority
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks.sort(key=lambda x: priority_order.get(x["priority"], 2))

    print("\n📋 Your Tasks:")
    print(f"  {'ID':<5} {'Priority':<10} {'Status':<8} {'Title':<30} {'Created'}")
    print("  " + "-" * 65)
    for task in tasks:
        status = "✔ Done" if task["done"] else "✘ Todo"
        priority = task.get("priority", "Medium")
        emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(priority, "🟡")
        print(f"  {task['id']:<5} {emoji + priority:<12} {status:<8} {task['title']:<30} {task['created_at']}")

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