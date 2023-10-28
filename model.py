import csv
import os
from rich.console import Console
from datetime import datetime

console = Console()

class todos:
    tasks = []

    def __init__(self, task: str, category: str, status: bool, due_date: None):
        self.task = task
        self.category = category
        #might change to bool
        self.status = False if status != True else True
        self.due_date = due_date
    
    def to_dict(self):
        return {"task": self.task, "category": self.category, "status": self.status, "due_date": self.due_date.strftime("%H:%M %Y-%m-%d") if self.due_date else None}

    @staticmethod
    def check_headers_exist(file):
        # Read the first line to check for headers
        first_line = file.readline()
        return "task" in first_line and "category" and "status" and "due_date" in first_line

    @classmethod
    def adding_task(cls, task: str, category: str, status: bool, due_datestr=str):
        try:
            due_date = datetime.strptime(due_datestr, "%H:%M %Y-%m-%d")
        except ValueError:
            console.print("Invalid date format.")
        task_instance = cls(task, category, status, due_date)
        cls.tasks.append(task_instance.to_dict())

        file_exists = os.path.exists('tasks.csv')

        with open('tasks.csv', "r+", newline="") as file:
            fieldnames = ["task", "category", "status", "due_date"]
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
    def deleting_task(cls, position: str):
        #Basically look inside tasks.csv
        #only take columns[0] row[uptousertodelete]
        #open the file
        if position.isnumeric():
            with open('tasks.csv','r+') as file:
                content = csv.DictReader(file)
                data = list(content)
                #remove the index data
                if 0 <= int(position) < len(data): data.pop(int(position))
        elif position == 'all':
            with open('tasks.csv','r+') as file:
                file.truncate(0)
                return
        else:
            print('Not recognized')


        #update the tasks
        with open('tasks.csv', 'w', newline='') as file:
            fieldnames = ["task", "category", "status", "due_date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    @classmethod
    def update_status(cls, position: int, status: bool):
        with open('tasks.csv','r', newline="") as file:
            data = []
            content = csv.DictReader(file)
            for row in content:
                data.append(row)
            if 0 <= position < len(data):
            # Update the status of the task at the given position
                data[position]['status'] = str(status)

            # if 0 <= position < len(data):
            #     task = data[position]
            #     task.status = status
        with open('tasks.csv', 'w') as file:
            fieldnames = ["task", "category", "status", "due_date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    @classmethod
    def load_tasks(cls):
        tasks = []
        try:
            with open('tasks.csv', "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    task = cls(row["task"], row["category"], row["status"] == 'True', row["due_date"])
                    tasks.append(task)
        except FileNotFoundError:
            pass
        return tasks
