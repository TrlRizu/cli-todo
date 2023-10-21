import csv
import os
from rich.console import Console
from rich.table import Table

console = Console()

class todos:
    tasks = []

    def __init__(self, task: str, category: str, status=None):
        self.task = task
        self.category = category
        self.status = status if status is not None else 1
    
    def to_dict(self):
        return {"task": self.task, "category": self.category}

    @staticmethod
    def check_headers_exist(file):
        # Read the first line to check for headers
        first_line = file.readline()
        return "task" in first_line and "category" in first_line

    @classmethod
    def adding_task(cls, task: str, category: str):
        task_instance = cls(task, category)
        cls.tasks.append(task_instance.to_dict())

        file_exists = os.path.exists('tasks.csv')

        with open('tasks.csv', "r+", newline="") as file:
            fieldnames = ["task", "category"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Check if the file is empty (no tasks written yet)
            if not file_exists:
                writer.writeheader()  # Write the header if the file is empty

            #Check if headers already exists
            elif not cls.check_headers_exist(file):
                writer.writeheader()

            #write every task in lists
            for todo in cls.tasks:
                writer.writerow(todo)

    @classmethod
    def deleting_task(cls, position: int):
        #Basically look inside tasks.csv
        #only take columns[0] row[uptousertodelete]
        #open the file
        with open('tasks.csv','r+') as file:
            content = csv.DictReader(file)
            data = list(content)
            #remove the index data
            if 0 <= position < len(data): data.pop(position)
                # task = data[position]["task"]
                # print(f"Extracted task: {task}")

        #update the tasks
        with open('tasks.csv', 'w', newline='') as file:
            fieldnames = ["task", "category"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)


    # @classmethod
    # def update_progress(cls)

    @classmethod
    def load_tasks(cls):
        tasks = []
        try:
            with open('tasks.csv', "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    task = cls(row["task"], row["category"])
                    # task.is_done = row.get("is_done", "False") == "True"
                    tasks.append(task)
        except FileNotFoundError:
            pass
        return tasks
