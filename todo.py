import json
import os
from datetime import datetime
from colorama import init, Fore, Back, Style

# Initialize colorama (required for Windows)
init(autoreset=True)

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
    print(f"\n{Fore.CYAN}Select Priority:")
    print(f"  {Fore.RED}1. 🔴 High")
    print(f"  {Fore.YELLOW}2. 🟡 Medium")
    print(f"  {Fore.GREEN}3. 🟢 Low")
    choice = input(f"{Fore.WHITE}Choose (1/2/3): ")
    priorities = {"1": "High", "2": "Medium", "3": "Low"}
    return priorities.get(choice, "Medium")

def get_due_date():
    while True:
        due_date = input(f"{Fore.CYAN}Enter due date (YYYY-MM-DD) or press Enter to skip: ").strip()
        if due_date == "":
            return None
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            return due_date
        except ValueError:
            print(f"{Fore.RED}❌ Invalid format! Please use YYYY-MM-DD (e.g. 2026-05-10)")

def check_due_status(due_date):
    if not due_date:
        return f"{Fore.WHITE}No due date"
    today = datetime.now().date()
    due = datetime.strptime(due_date, "%Y-%m-%d").date()
    diff = (due - today).days
    if diff < 0:
        return f"{Fore.RED}⚠️  Overdue!"
    elif diff == 0:
        return f"{Fore.MAGENTA}⏰ Due Today!"
    elif diff <= 3:
        return f"{Fore.YELLOW}⚡ Due in {diff} day(s)"
    else:
        return f"{Fore.GREEN}📅 {due_date}"

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
    print(f"{Fore.GREEN}✅ Task added: [{priority}] {title}{due_info}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print(f"{Fore.YELLOW}No tasks yet!")
        return

    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks.sort(key=lambda x: priority_order.get(x["priority"], 2))

    print(f"\n{Fore.CYAN}{'='*65}")
    print(f"{Fore.CYAN}  📋 YOUR TASKS")
    print(f"{Fore.CYAN}{'='*65}")

    for task in tasks:
        # Status color
        if task["done"]:
            status = f"{Fore.GREEN}✔ Done  "
        else:
            status = f"{Fore.RED}✘ Todo  "

        # Priority color
        priority = task.get("priority", "Medium")
        priority_colors = {
            "High":   f"{Fore.RED}🔴 High  ",
            "Medium": f"{Fore.YELLOW}🟡 Medium",
            "Low":    f"{Fore.GREEN}🟢 Low   "
        }
        priority_display = priority_colors.get(priority, f"{Fore.YELLOW}🟡 Medium")

        # Title color (grey if done)
        title_display = f"{Fore.WHITE}{task['title']}" if not task["done"] else f"{Fore.WHITE}{Style.DIM}{task['title']}"

        due_status = check_due_status(task.get("due_date"))

        print(f"  {Fore.WHITE}[{task['id']}] {priority_display} | {status} | {title_display}")
        print(f"       {due_status}")
        print()

    print(f"{Fore.CYAN}{'='*65}")

def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"{Fore.GREEN}🎉 Task {task_id} marked as done!")
            return
    print(f"{Fore.RED}Task not found.")

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print(f"{Fore.YELLOW}🗑️  Task {task_id} deleted.")

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
        print(f"{Fore.GREEN}✅ No overdue tasks!")
    else:
        print(f"\n{Fore.RED}⚠️  Overdue Tasks ({len(overdue)}):")
        for task in overdue:
            print(f"  {Fore.RED}❗ [{task['id']}] {task['title']} - was due {task['due_date']}")

def search_tasks(keyword):
    tasks = load_tasks()
    keyword = keyword.lower()
    results = [t for t in tasks if keyword in t["title"].lower()]

    if not results:
        print(f"{Fore.YELLOW}🔍 No tasks found for: '{keyword}'")
        return

    print(f"\n{Fore.CYAN}{'='*65}")
    print(f"{Fore.CYAN}  🔍 Search Results for: '{keyword}' ({len(results)} found)")
    print(f"{Fore.CYAN}{'='*65}")

    for task in results:
        # Status color
        if task["done"]:
            status = f"{Fore.GREEN}✔ Done  "
        else:
            status = f"{Fore.RED}✘ Todo  "

        # Priority color
        priority = task.get("priority", "Medium")
        priority_colors = {
            "High":   f"{Fore.RED}🔴 High  ",
            "Medium": f"{Fore.YELLOW}🟡 Medium",
            "Low":    f"{Fore.GREEN}🟢 Low   "
        }
        priority_display = priority_colors.get(priority, f"{Fore.YELLOW}🟡 Medium")
        due_status = check_due_status(task.get("due_date"))

        # Highlight keyword in title
        highlighted = task["title"].replace(
            keyword, f"{Fore.MAGENTA}{keyword}{Fore.WHITE}"
        )

        print(f"  {Fore.WHITE}[{task['id']}] {priority_display} | {status} | {highlighted}")
        print(f"       {due_status}")
        print()

    print(f"{Fore.CYAN}{'='*65}")

def main():
    while True:
        print(f"\n{Fore.CYAN}{'='*25}")
        print(f"{Fore.CYAN}   ✅ TO-DO APP")
        print(f"{Fore.CYAN}{'='*25}")
        print(f"{Fore.WHITE}1. ➕ Add Task")
        print(f"{Fore.WHITE}2. 📋 List Tasks")
        print(f"{Fore.WHITE}3. ✔️  Complete Task")
        print(f"{Fore.WHITE}4. 🗑️  Delete Task")
        print(f"{Fore.WHITE}5. ⚠️  Show Overdue Tasks")
        print(f"{Fore.WHITE}6. 🔍 Search Tasks")
        print(f"{Fore.WHITE}7. 🚪 Exit")
        choice = input(f"{Fore.CYAN}Choose: ")

        if choice == "1":
            title = input(f"{Fore.WHITE}Task title: ")
            add_task(title)
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            task_id = int(input(f"{Fore.WHITE}Task ID to complete: "))
            complete_task(task_id)
        elif choice == "4":
            task_id = int(input(f"{Fore.WHITE}Task ID to delete: "))
            delete_task(task_id)
        elif choice == "5":
            show_overdue()
        elif choice == "6":
            keyword = input(f"{Fore.WHITE}Enter search keyword: ")
            search_tasks(keyword)
        elif choice == "7":
            print(f"{Fore.GREEN}Goodbye! 👋")
            break
        else:
            print(f"{Fore.RED}Invalid choice.")

if __name__ == "__main__":
    main()