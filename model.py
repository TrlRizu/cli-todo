import csv
import os
from rich.console import Console
from rich.table import Table

console = Console()

class todos:
    tasks = []

    def __init__(self, task: str, category: str, status: bool):
        self.task = task
        self.category = category
        #might change to bool
        self.status = False if status != True else True
    
    def to_dict(self):
        return {"task": self.task, "category": self.category, "status": self.status}

    @staticmethod
    def check_headers_exist(file):
        # Read the first line to check for headers
        first_line = file.readline()
        return "task" in first_line and "category" and "status" in first_line

    @classmethod
    def adding_task(cls, task: str, category: str):
        task_instance = cls(task, category)
        cls.tasks.append(task_instance.to_dict())

        file_exists = os.path.exists('tasks.csv')

        with open('tasks.csv', "r+", newline="") as file:
            fieldnames = ["task", "category", "status"]
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
            fieldnames = ["task", "category", "status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    @classmethod
    def update_status(cls, position: int, status: bool):
        tasks = cls.load_tasks()
        if 0 <= position < len(tasks):
            task = tasks[position]
            task.status = status
            # console.log(task.status)

        with open('tasks.csv', "w", newline="") as file:
            fieldnames = ["task", "category", "status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for task in tasks:
                writer.writerow(task.to_dict())


    @classmethod
    def load_tasks(cls):
        tasks = []
        try:
            with open('tasks.csv', "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    #  task = cls(row["task"], row["category"], row["status"] == 'True')
                    task = cls(row["task"], row["category"], row["status"] == 'True')
                    # console.log(task.status)
                    # task.status = False if row.get("status", "False") else True
                    tasks.append(task)
        except FileNotFoundError:
            pass
        return tasks
