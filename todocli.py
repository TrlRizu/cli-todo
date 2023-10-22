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

console = Console()

app = typer.Typer(rich_markup_mode="rich")

#adding tasks
@app.command()
def add(task: str = typer.Argument(..., rich_help_panel="Type of [cyan]TASK[/cyan]"),
    category: str = typer.Argument(..., rich_help_panel="[red]Classification[/red] of the task")):

    """
    [green]ADDS[/green] new tasks to the list. :sparkles:
    """
    print(f"Adding: {task}, {category}")
    # print(f"Creating user: ")

    todos.adding_task(task,category)
    show()


#Deleting tasks
@app.command()
def delete(position: int):
    """
    [red]REMOVES[/red] tasks from the list. :fire:
    """
    typer.echo(f"deleting {position}")
    todos.deleting_task(position)
    show()

@app.command()
def update(position: int, status: bool):
    todos.update_status(position, status)
    show()



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

        #Hardcoded for now
        def get_category_color(category):
            colours = {'Learn': 'cyan', 'Coding': 'red', 'Study': 'cyan', 'Misc': 'green'}
            if category in colours:
                return colours[category]
            return 'white'

        for idx, task in enumerate(tasks, start=0):
            colour = get_category_color(task.category)
            done = '✅' if task.status == True else '❌'
            table.add_row(str(idx), task.task, f'[{colour}]{task.category}[/{colour}]', done)
        console.print(table)
    else:
        console.print("No tasks to display", style="yellow")




if __name__ == "__main__":
    app()
