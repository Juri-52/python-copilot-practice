from task import Task


class TaskManager:
    def __init__(self, tasks: list[Task]):
        self.tasks = list(tasks)

    def add_task(self, title: str) -> Task:
        next_id = max((task.task_id for task in self.tasks), default=0) + 1
        task = Task(next_id, title)
        self.tasks.append(task)
        return task

    def complete_task(self, task_id: int) -> None:
        for task in self.tasks:
            if task.task_id == task_id:
                task.complete()
                return
        raise ValueError("タスクが見つかりません")
