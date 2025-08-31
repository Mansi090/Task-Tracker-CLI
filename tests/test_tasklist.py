import os
import sys
from pathlib import Path

# Make src importable when running tests from project root
THIS_DIR = Path(__file__).parent
SRC_DIR = (THIS_DIR / ".." / "src").resolve()
sys.path.insert(0, str(SRC_DIR))

from main import TaskList  # noqa: E402


def test_add_and_internal_state():
    tl = TaskList()
    tl.add_task("Task A", "High")
    tl.add_task("Task B", "Low")
    assert len(tl.tasks) == 2
    assert tl.tasks[0].title == "Task A"
    assert tl.tasks[0].priority == "High"
    assert tl.tasks[1].priority == "Low"


def test_update_status_and_validation(capsys):
    tl = TaskList()
    tl.add_task("Task A", "High")
    tl.update_task_status(1, "in-progress")
    assert tl.tasks[0].status == "in-progress"

    # invalid status prints error and does not change
    tl.update_task_status(1, "invalid-status")
    assert tl.tasks[0].status == "in-progress"
    captured = capsys.readouterr().out
    assert "Invalid status" in captured


def test_update_details():
    tl = TaskList()
    tl.add_task("Old", "Low")
    tl.update_task(1, title="New", priority="Medium")
    t = tl.tasks[0]
    assert t.title == "New"
    assert t.priority == "Medium"


def test_search_and_sort(capsys):
    tl = TaskList()
    tl.add_task("Learn Python", "High")
    tl.add_task("Write README", "Medium")
    tl.search_tasks("learn")
    out = capsys.readouterr().out.lower()
    assert "learn python" in out

    # sort by title ascending
    tl.sort_tasks("title", True)
    titles = [t.title for t in tl.tasks]
    assert titles == sorted(titles)


def test_save_and_load_roundtrip(tmp_path: Path):
    file_path = tmp_path / "tasks.json"

    tl = TaskList()
    tl.add_task("One", "High")
    tl.add_task("Two", "Low")
    tl.save_to_file(str(file_path))

    tl2 = TaskList()
    tl2.load_from_file(str(file_path))

    assert len(tl2.tasks) == 2
    assert tl2.next_id == 3
    assert tl2.tasks[0].title == "One"
