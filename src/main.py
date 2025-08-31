import json
import os
from typing import List, Dict, Optional

# Constants for valid statuses and priorities
VALID_STATUSES = {"todo", "in-progress", "done"}
VALID_PRIORITIES = {"High", "Medium", "Low"}

# Task structure
class Task:
    def __init__(self, task_id: int, title: str, status: str = "todo", priority: str = "Low"):
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")
        if not title.strip():
            raise ValueError("Task title cannot be empty.")
        if status.lower() not in VALID_STATUSES:
            raise ValueError(f"Invalid status. Valid options: {', '.join(VALID_STATUSES)}")
        if priority.capitalize() not in VALID_PRIORITIES:
            raise ValueError(f"Invalid priority. Valid options: {', '.join(VALID_PRIORITIES)}")
        self.id = task_id
        self.title = title.strip()
        self.status = status.lower()
        self.priority = priority.capitalize()

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "priority": self.priority
        }

# Task List Manager
class TaskList:
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str, priority: str) -> None:
        try:
            task = Task(self.next_id, title, priority=priority)
            self.tasks.append(task)
            print(f"Task '{title}' added with ID {task.id}.")
            self.next_id += 1
        except ValueError as e:
            print(f"Error: {e}")

    def update_task_status(self, task_id: int, status: str) -> None:
        task = self._find_task(task_id)
        if not task:
            print("Error: Task not found.")
            return
        if status.lower() not in VALID_STATUSES:
            print(f"Error: Invalid status. Valid options: {', '.join(VALID_STATUSES)}")
            return
        task.status = status.lower()
        print(f"Task ID {task_id} updated to status '{status}'.")

    def update_task(self, task_id: int, title: Optional[str] = None, priority: Optional[str] = None) -> None:
        task = self._find_task(task_id)
        if not task:
            print("Error: Task not found.")
            return
        try:
            if title is not None and title.strip():
                task.title = title.strip()
            if priority is not None:
                if priority.capitalize() not in VALID_PRIORITIES:
                    print(f"Error: Invalid priority. Valid options: {', '.join(VALID_PRIORITIES)}")
                    return
                task.priority = priority.capitalize()
            if title is not None or priority is not None:
                print(f"Task ID {task_id} updated successfully.")
            else:
                print("No changes made to task.")
        except ValueError as e:
            print(f"Error: {e}")

    def list_tasks(self, status_filter: str = "all", priority_filter: str = "all") -> None:
        status_filter = status_filter.lower()
        priority_filter = priority_filter.lower()
        if status_filter not in VALID_STATUSES | {"all"}:
            print(f"Error: Invalid status filter. Valid options: {', '.join(VALID_STATUSES | {'all'})}")
            return
        if priority_filter not in {p.lower() for p in VALID_PRIORITIES} | {"all"}:
            print(f"Error: Invalid priority filter. Valid options: {', '.join(VALID_PRIORITIES | {'all'})}")
            return
        print("\nTasks:")
        count = 0
        for task in self.tasks:
            if (status_filter == "all" or task.status == status_filter) and \
               (priority_filter == "all" or task.priority.lower() == priority_filter):
                print(f"ID: {task.id} | Title: {task.title} | Status: {task.status} | Priority: {task.priority}")
                count += 1
        if count == 0:
            print("No tasks found.")

    def delete_task(self, task_id: int) -> None:
        task = self._find_task(task_id)
        if not task:
            print("Error: Task not found.")
            return
        while True:
            confirm = input(f"Are you sure you want to delete task '{task.title}'? (yes/no): ").strip().lower()
            if confirm in ["yes", "no"]:
                break
            print("Error: Please enter 'yes' or 'no'.")
        if confirm == "yes":
            self.tasks.remove(task)
            print(f"Task ID {task_id} deleted.")
        else:
            print("Deletion cancelled.")

    def search_tasks(self, keyword: str) -> None:
        if not keyword.strip():
            print("Error: Keyword cannot be empty.")
            return
        keyword = keyword.lower()
        print("\nSearch Results:")
        count = 0
        for task in self.tasks:
            if keyword in task.title.lower():
                print(f"ID: {task.id} | Title: {task.title} | Status: {task.status} | Priority: {task.priority}")
                count += 1
        if count == 0:
            print("No tasks found matching the keyword.")

    def sort_tasks(self, by: str, ascending: bool = True) -> None:
        valid_fields = {"id", "title", "status", "priority"}
        if by.lower() not in valid_fields:
            print(f"Error: Invalid sort field. Valid options: {', '.join(valid_fields)}")
            return
        try:
            self.tasks.sort(key=lambda t: getattr(t, by.lower()), reverse=not ascending)
            print("Tasks sorted successfully.")
            self.list_tasks()
        except AttributeError:
            print("Error: Failed to sort tasks.")

    def save_to_file(self, filename: str) -> None:
        try:
            with open(filename, "w") as f:
                json.dump({
                    "tasks": [t.to_dict() for t in self.tasks],
                    "next_id": self.next_id
                }, f, indent=4)
            print(f"Tasks saved to {filename}.")
        except (IOError, PermissionError) as e:
            print(f"Error: Failed to save tasks to {filename}. {e}")

    def load_from_file(self, filename: str) -> None:
        if not os.path.exists(filename):
            print(f"Warning: File {filename} does not exist. Starting with an empty task list.")
            return
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.tasks = []
                max_id = 0
                for task_data in data.get("tasks", []):
                    task = Task(
                        task_data["id"],
                        task_data["title"],
                        task_data.get("status", "todo"),
                        task_data.get("priority", "Low")
                    )
                    self.tasks.append(task)
                    max_id = max(max_id, task.id)
                self.next_id = max(max_id + 1, data.get("next_id", 1))
            print(f"Tasks loaded from {filename}.")
        except json.JSONDecodeError:
            print(f"Error: {filename} contains invalid JSON. Starting with an empty task list.")
            self.tasks, self.next_id = [], 1
        except (IOError, PermissionError) as e:
            print(f"Error: Failed to load tasks from {filename}. {e}")
            self.tasks, self.next_id = [], 1

    def _find_task(self, task_id: int) -> Optional[Task]:
        return next((task for task in self.tasks if task.id == task_id), None)

# CLI Menu
def display_menu():
    print("\nEnhanced Task Tracker CLI (Python)")
    print("1. Add Task")
    print("2. Update Task Status")
    print("3. Update Task Details")
    print("4. List Tasks")
    print("5. Delete Task")
    print("6. Search Tasks")
    print("7. Sort Tasks")
    print("8. Exit")

def main():
    task_list = TaskList()
    file_path = "tasks.json"
    task_list.load_from_file(file_path)

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            title = input("Enter task title: ").strip()
            priority = input("Enter priority (High, Medium, Low): ").strip()
            task_list.add_task(title, priority)

        elif choice == "2":
            try:
                task_id = int(input("Enter task ID to update: ").strip())
                status = input("Enter new status (todo, in-progress, done): ").strip()
                task_list.update_task_status(task_id, status)
            except ValueError:
                print("Error: Invalid task ID. Please enter a number.")

        elif choice == "3":
            try:
                task_id = int(input("Enter task ID to update: ").strip())
                print("Leave blank to keep current value.")
                title = input("Enter new title (or press Enter to skip): ").strip()
                priority = input("Enter new priority (High, Medium, Low, or press Enter to skip): ").strip()
                task_list.update_task(task_id, title or None, priority or None)
            except ValueError:
                print("Error: Invalid task ID. Please enter a number.")

        elif choice == "4":
            status = input("Enter status filter (todo, in-progress, done, all): ").strip()
            priority = input("Enter priority filter (High, Medium, Low, all): ").strip()
            task_list.list_tasks(status, priority)

        elif choice == "5":
            try:
                task_id = int(input("Enter task ID to delete: ").strip())
                task_list.delete_task(task_id)
            except ValueError:
                print("Error: Invalid task ID. Please enter a number.")

        elif choice == "6":
            keyword = input("Enter keyword to search: ").strip()
            task_list.search_tasks(keyword)

        elif choice == "7":
            print("Sort by: id, title, status, priority")
            by = input("Enter field: ").strip()
            order = input("Ascending? (yes/no): ").strip().lower()
            ascending = order == "yes"
            task_list.sort_tasks(by, ascending)

        elif choice == "8":
            task_list.save_to_file(file_path)
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Please select a number between 1 and 8.")

if __name__ == "__main__":
    main()