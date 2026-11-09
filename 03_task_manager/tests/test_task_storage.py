import json

from task import Task
from task_storage import load_tasks, save_tasks


def test_save_and_load_unfinished_task(tmp_path):
    filename = str(tmp_path / "tasks.json")
    tasks = [Task(3, "日本語の課題を読む")]

    save_tasks(filename, tasks)
    restored = load_tasks(filename)

    assert len(restored) == 1
    assert restored[0].task_id == 3
    assert restored[0].title == "日本語の課題を読む"
    assert restored[0].completed is False
    assert restored[0] is not tasks[0]


def test_save_and_load_empty_list(tmp_path):
    filename = str(tmp_path / "tasks.json")

    save_tasks(filename, [])
    restored = load_tasks(filename)
    with open(filename, encoding="utf-8") as file:
        stored = json.load(file)

    assert stored == []
    assert restored == []


# TODO: 完了したタスクを保存し、読み直しても完了状態が残ることを確認する。
def test_save_and_load_preserves_mixed_completion_states(tmp_path):
    filename = str(tmp_path / "tasks.json")
    tasks = [
        Task(1, "コードを読む"),
        Task(2, "仕様を確認する", completed=True),
        Task(3, "テストを書く"),
    ]

    save_tasks(filename, tasks)
    restored = load_tasks(filename)
    with open(filename, encoding="utf-8") as file:
        stored = json.load(file)

    assert stored == [
        {"id": 1, "title": "コードを読む", "completed": False},
        {"id": 2, "title": "仕様を確認する", "completed": True},
        {"id": 3, "title": "テストを書く", "completed": False},
    ]
    assert [
        (task.task_id, task.title, task.completed) for task in restored
    ] == [
        (1, "コードを読む", False),
        (2, "仕様を確認する", True),
        (3, "テストを書く", False),
    ]
    assert all(
        restored_task is not original_task
        for restored_task, original_task in zip(restored, tasks)
    )
