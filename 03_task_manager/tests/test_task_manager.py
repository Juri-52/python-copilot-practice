import pytest

from task import Task
from task_manager import TaskManager


def test_add_task_to_empty_manager():
    manager = TaskManager([])

    created = manager.add_task("復習する")

    assert created.task_id == 1
    assert created.title == "復習する"
    assert created.completed is False
    assert manager.tasks == [created]


def test_new_id_uses_largest_existing_id():
    original = Task(5, "コードを読む")
    manager = TaskManager([original, Task(2, "ノートを書く")])

    created = manager.add_task("テストを書く")

    assert created.task_id == 6
    assert len(manager.tasks) == 3
    assert manager.tasks[0] is original
    assert original.title == "コードを読む"


# TODO: 完了処理、対象外のタスク、存在しないID、再度の完了をテストする。
def test_complete_task_marks_only_the_requested_task_as_completed():
    first = Task(1, "コードを読む")
    target = Task(2, "仕様を確認する")
    third = Task(3, "テストを書く", completed=True)
    manager = TaskManager([first, target, third])

    manager.complete_task(2)

    assert [task.completed for task in manager.tasks] == [False, True, True]
    assert [(task.task_id, task.title) for task in manager.tasks] == [
        (1, "コードを読む"),
        (2, "仕様を確認する"),
        (3, "テストを書く"),
    ]


def test_complete_task_raises_for_unknown_id():
    manager = TaskManager([Task(1, "コードを読む")])

    with pytest.raises(ValueError, match="^タスクが見つかりません$"):
        manager.complete_task(99)


def test_complete_task_can_be_called_twice():
    manager = TaskManager([Task(1, "コードを読む")])

    manager.complete_task(1)
    manager.complete_task(1)

    assert manager.tasks[0].completed is True
