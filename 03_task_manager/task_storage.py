import json

from task import Task


def load_tasks(filename: str) -> list[Task]:
    with open(filename, encoding="utf-8") as file:
        records = json.load(file)
    return [Task(row["id"], row["title"], row["completed"]) for row in records]


def save_tasks(filename: str, tasks: list[Task]) -> None:
    records = [
        {
            "id": task.task_id,
            "title": task.title,
            "completed": task.completed,
        }
        for task in tasks
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)
