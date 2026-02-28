##Task: Build a functional To-Do List Application using Python from scratch.
## It should be a practical, interactive command-line application.


## A simple ToDo list application using Click library.
import click

tasks = []
## displays menu of tasks that are stored in a Python list
def show_menu():
    click.echo("\nMenu:")
    click.echo("\n".join([
        "1. Add Task",
        "2. View Tasks",
        "3. Delete Task",
        "4. Exit"
    ]))
## User interaction
## Functions to add, view, and delete tasks from the ToDo list.
def add_task():
    task = click.prompt("Enter the task you want to add")
    tasks.append(task)
    click.echo(f"Task '{task}' added to your ToDo list.")

def view_tasks():
    if tasks:
        click.echo("Your ToDo List:")
        for idx, task in enumerate(tasks, start=1):
            click.echo(f"{idx}. {task}")
            ## Error handling for empty list
    else:
        click.echo("Your ToDo list is empty.")

def delete_task():
    if tasks:
        click.echo("Your ToDo List:")
        for idx, task in enumerate(tasks, start=1):
            click.echo(f"{idx}. {task}")
        task_num = click.prompt("Enter the task number you want to delete", type=int)
        if 1 <= task_num <= len(tasks):
            removed_task = tasks.pop(task_num - 1)
            click.echo(f"Task '{removed_task}' deleted from your ToDo list.")
            ## Error handling for invalid task number
        else:
            click.echo("Invalid task number.")
            ## Error handling for empty list
    else:
        click.echo("Your ToDo list is empty.")

##welcomes users 
@click.command()
@click.option('--name', prompt='Enter your name', help='Your name')
def todo(name):
    click.echo(f"Welcome {name} to your ToDo List!")
    click.echo("Let's get started with your tasks.")

    while True:
        show_menu()
        choice = click.prompt("Please enter your choice", type=int)

        if choice == 1:
            add_task()
        elif choice == 2:
            view_tasks()
        elif choice == 3:
            delete_task()
        elif choice == 4:
            click.echo("Goodbye! Have a productive day!")
            break
        ##Error handling for invalid menu choice
        else:
            click.echo("Invalid choice. Please try again.")

if __name__ == '__main__':
    todo()
