from task_manager import TaskManager
from task_storage import load_tasks, save_tasks


def main() -> None:
    manager = TaskManager(load_tasks("tasks.json"))
    manager.add_task("テストを書く")
    manager.complete_task(2)
    save_tasks("tasks_result.json", manager.tasks)

    restored = load_tasks("tasks_result.json")
    print("再読み込みしたタスク:")
    for task in restored:
        status = "完了" if task.completed else "未完了"
        print(f"{task.task_id}: {task.title} [{status}]")


if __name__ == "__main__":
    main()
