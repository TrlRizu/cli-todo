"""
MORE THINGS TO ADD:
1. HELP FUNCTION FOR DELETE & SHOW
2. UPDATE PROGRESS OF TASK
3. PERHAPS A TIMER FOR COMPLETION OF TASK?


"""

import typer
from typing_extensions import Annotated
from rich.console import Console
from rich.table import Table
from model import todos
from datetime import datetime
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

console = Console()

app = typer.Typer(rich_markup_mode="rich")

#adding tasks
@app.command()
def add(task: str = typer.Argument(..., help="Type of [cyan]TASK[/cyan]"),
    category: str = typer.Argument(..., help="[red]Classification[/red] of the task"),
    date: str = typer.Argument(datetime.now().strftime("%H:%M %Y-%m-%d"),help="Date & Time"),
    status: bool = typer.Argument(False, help="[red]Status of the task[/red] e.g: '13:01 2023-08-12'")):

    """
    [green]ADDS[/green] new tasks to the list. :sparkles:
    """
    # print(f"Adding: {task}, {category}, {status}")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(f"[green]Adding {task}, {category} into the list...", total=None)
        #Unnecessary I know
        # time.sleep(1)
        todos.adding_task(task,category,status,date)
    show()
    print("Done!")


#Deleting tasks
@app.command()
def delete(position: str):
    """
    [red]REMOVES[/red] tasks from the list. :fire:
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(f"[red]Deleting {position} from the list...", total=None)
        # time.sleep(1)
        todos.deleting_task(position)
    show()
    print("Done!")

@app.command()
def update(position: int, status: bool):
    """
    [blue]UPDATES[/blue] the status of the specified task. :gear:
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(f"[purple]Updating {position} to {status}...", total=None)
        # time.sleep(1)
        todos.update_status(position, status)
    show()
    print("Done!")




#Display the tasks
@app.command()
def show():
    """
    [yellow]DISPLAYS[/yellow] the task lists. :computer:
    """

    # console.print("[bold magenta]TODOS[/bold magenta]!", "💻")
    tasks = todos.load_tasks()

    # print(f"Loaded {len(tasks)} tasks from the CSV file")  # Debugging line


    if tasks:
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("#", style="dim", width=6)
        table.add_column("Todo", min_width=20)
        table.add_column("Category", min_width=12, justify="right")
        table.add_column("Status", min_width=12, justify="right")
        table.add_column("Due date", min_width=24, justify="right")

        #Hardcoded for now
        def get_category_colour(category):
            colours = {'Learn': 'cyan', 'Coding': 'red', 'Study': 'cyan', 'Misc': 'green'}
            if category in colours:
                return colours[category]
            return 'white'

        def calculatehourscolour(date):
            for task in tasks:
                x = datetime.strptime(date, "%H:%M %Y-%m-%d")
                y = datetime.strptime(datetime.now().strftime("%H:%M %Y-%m-%d"), "%H:%M %Y-%m-%d")
                # return 'green' if x.hour-y.hour > 3 else 'yellow' if 3 > x.hour-y.hour > 1  else 'red'
                #this is OBVIOUSLY WRONG
                if x < y:
                    return 'red'
                else:
                    if x.month-y.month or x.month > y.month or x.day > y.day or x.hour-y.hour >= 3:
                        return 'green'
                    elif 3 > x.hour-y.hour > 1:
                        return 'yellow'
                    elif x.hour-y.hour < 1:
                        return 'red'


        for idx, task in enumerate(tasks, start=0):
            colour = get_category_colour(task.category)
            urgency = calculatehourscolour(task.due_date)
            # console.log(task.due_date)
            done = '✅' if task.status == True else '❌'
            table.add_row(str(idx), task.task, f'[{colour}]{task.category}[/{colour}]', done, f'[{urgency}]{task.due_date}[/{urgency}]')
        console.print(table)
    else:
        console.print("No tasks to display", style="yellow")




if __name__ == "__main__":
    app()
