# Enhanced Task Tracker CLI 🚀

**A feature-rich command-line tool for managing your tasks efficiently!**

With support for priorities, searching, sorting, and task updates, this Python-based CLI tool helps you organize your tasks like a pro.

---

## Features ✨

1. **Add Tasks** 📝  
   Create new tasks with a title and priority (`High`, `Medium`, or `Low`).  

2. **Update Task Status** 🔄  
   Change task statuses between `todo`, `in-progress`, and `done`.  

3. **Update Task Details** ✏️  
   Modify task titles and priorities with ease.  

4. **List Tasks** 📋  
   View tasks filtered by status, priority, or both, with clear details.  

5. **Delete Tasks** 🗑️  
   Safely remove tasks with confirmation prompts to avoid accidental deletions.  

6. **Search Tasks** 🔍  
   Quickly locate tasks by keywords in their titles.  

7. **Sort Tasks** ⬆️⬇️  
   Organize tasks by:  
   - **ID**  
   - **Title**  
   - **Status**  
   - **Priority**  

8. **Persistent Storage** 💾  
   Save tasks to a `tasks.json` file and reload them on startup.  

9. **User-Friendly Menu** 🎯  
   Intuitive, easy-to-navigate menu with case-insensitive input handling.  

---

## Installation 🛠️

1. **Clone the repository**:  
   ```bash
   git clone https://github.com/your-username/enhanced-task-tracker.git
   cd enhanced-task-tracker
   ```

2. **Ensure Python 3.5+ is installed**:  
   Check your Python version:  
   ```bash
   python --version
   ```

3. **Run the program**:  
   ```bash
   python src/main.py
   ```

---

## Usage 🧑‍💻

Upon running the program, you'll see the following menu:

```text
Enhanced Task Tracker CLI (Python)
1. Add Task
2. Update Task Status
3. Update Task Details
4. List Tasks
5. Delete Task
6. Search Tasks
7. Sort Tasks
8. Exit
Choose an option:
```

Select an option by entering its number and follow the prompts to manage your tasks.

---

## Examples 🌟

### Adding a Task
```text
Choose an option: 1
Enter task title: Learn Python
Enter priority (High, Medium, Low): high
Task 'Learn Python' added with ID 1.
```

### Listing Tasks
```text
Choose an option: 4
Enter status filter (todo, in-progress, done, all): all
Enter priority filter (High, Medium, Low, all): all

Tasks:
ID: 1 | Title: Learn Python | Status: todo | Priority: High
```

### Updating Task Status
```text
Choose an option: 2
Enter task ID to update: 1
Enter new status (todo, in-progress, done): in-progress
Task ID 1 updated to status 'in-progress'.
```

### Updating Task Details
```text
Choose an option: 3
Enter task ID to update: 1
Leave blank to keep current value.
Enter new title (or press Enter to skip): Learn Advanced Python
Enter new priority (High, Medium, Low, or press Enter to skip): Medium
Task ID 1 updated successfully.
```

### Searching Tasks
```text
Choose an option: 6
Enter keyword to search: learn

Search Results:
ID: 1 | Title: Learn Advanced Python | Status: in-progress | Priority: Medium
```

### Sorting Tasks
```text
Choose an option: 7
Sort by: id, title, status, priority
Enter field: priority
Ascending? (yes/no): yes
Tasks sorted successfully.

Tasks:
ID: 1 | Title: Learn Advanced Python | Status: in-progress | Priority: Medium
```

---

## DevOps: CI, Tests, Docker 🛠️

### Continuous Integration (GitHub Actions)
- Workflow: `.github/workflows/ci.yml`
- Runs on every push and pull request:
  - Lint with flake8
  - Check formatting with black
  - Run tests with pytest and coverage

You can see results in the GitHub Actions tab after pushing to GitHub.

### Development Setup
- Optional tools for local dev:
  ```bash
  pip install -r requirements-dev.txt
  ```

- Lint and format checks:
  ```bash
  flake8 src tests
  black --check src tests
  ```

- Run tests with coverage:
  ```bash
  pytest -q --cov=src --cov-report=term-missing
  ```

### Docker (Run Anywhere)
- Build the image:
  ```bash
  docker build -t task-tracker-cli .
  ```
- Run the CLI (stores tasks.json inside the container):
  ```bash
  docker run -it --rm task-tracker-cli
  ```
- Persist tasks to your host (maps current folder):
  ```bash
  docker run -it --rm -v "$PWD:/data" -w /data task-tracker-cli
  ```
  On Windows PowerShell, use:
  ```powershell
  docker run -it --rm -v ${PWD}:/data -w /data task-tracker-cli
  ```

---

## Notes 📌

- **Case-Insensitive Inputs**: Status and priority inputs are case-insensitive (e.g., "high", "HIGH", or "High" are all valid).
- **Error Handling**: The tool provides clear error messages for invalid inputs, such as non-numeric task IDs or invalid statuses.
- **Persistence**: Tasks are saved to `tasks.json` in the current working directory (where you run the program). If the file is missing or corrupted, the program starts with an empty task list.
- **File Permissions**: Ensure the program has write permissions in the directory to save `tasks.json`.

---

## Contributing 🤝

Want to improve the Enhanced Task Tracker? Contributions are welcome!

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Submit a pull request.

---
