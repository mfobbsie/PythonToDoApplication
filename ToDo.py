##ToDo.py
import click
from datetime import date

# -----------------------------
# Data Stores
# -----------------------------
tasks = []

# Reflection + streak tracking
reflections = []   # list of {"date": date, "completed": [...], "feeling": "...", "tomorrow": "..."}
streak_count = 0
last_reflection_date = None


# -----------------------------
# Helper: Display Menu
# -----------------------------
def show_menu():
    click.echo("\nMenu:")
    click.echo("\n".join([
        "1. Add Task",
        "2. View Tasks",
        "3. Delete Task",
        "4. View Recommended Tasks",
        "5. Daily Reflection",
        "6. View Streaks / Consistency",
        "7. Exit"
    ]))


# -----------------------------
# Add Task
# -----------------------------
def add_task():
    name = click.prompt("What task would you like to add?")

    energy = click.prompt(
        "What energy level does this task require? (low, mid, high)",
        type=click.Choice(["low", "mid", "high"], case_sensitive=False)
    )

    outcome = click.prompt(
        "How do you hope to feel after completing it? (rested, productive, inspired)",
        type=click.Choice(["rested", "productive", "inspired"], case_sensitive=False)
    )

    task = {"name": name, "energy": energy, "outcome": outcome}
    tasks.append(task)

    click.echo(f"Added '{name}' — a {energy}-energy task aimed at helping you feel {outcome}.")


# -----------------------------
# View Tasks
# -----------------------------
def view_tasks():
    if tasks:
        click.echo("\nYour To‑Do List:")
        for idx, task in enumerate(tasks, start=1):
            click.echo(
                f"{idx}. {task['name']} "
                f"(energy: {task['energy']}, outcome: {task['outcome']})"
            )
    else:
        click.echo("Your list is empty — a fresh slate.")


# -----------------------------
# Delete Task
# -----------------------------
def delete_task():
    if not tasks:
        click.echo("Your To‑Do list is empty.")
        return

    view_tasks()
    task_num = click.prompt("Which task number would you like to delete?", type=int)

    if 1 <= task_num <= len(tasks):
        removed = tasks.pop(task_num - 1)
        click.echo(f"Removed '{removed['name']}' from your list.")
    else:
        click.echo("That number doesn’t match any task.")


# -----------------------------
# Recommended Tasks
# -----------------------------
def view_recommended_tasks(name):
    if not tasks:
        click.echo("No tasks available to recommend yet.")
        return

    click.echo("\nHow would you like your recommendations?")
    click.echo("1. Based on your current energy level")
    click.echo("2. Based on how you want to feel afterward")

    choice = click.prompt("Choose an option", type=int)

    if choice == 1:
        energy = click.prompt(
            f"Where’s your energy at today, {name}? (low, mid, high)",
            type=click.Choice(["low", "mid", "high"], case_sensitive=False)
        )
        filtered = [t for t in tasks if t["energy"] == energy]

        click.echo(f"\nTasks that match your {energy} energy:")
        if filtered:
            for t in filtered:
                click.echo(f"- {t['name']} ({t['outcome']})")
        else:
            click.echo("Nothing fits that energy level right now.")

    elif choice == 2:
        outcome = click.prompt(
            "How do you want to feel when you're done? (rested, productive, inspired)",
            type=click.Choice(["rested", "productive", "inspired"], case_sensitive=False)
        )
        filtered = [t for t in tasks if t["outcome"] == outcome]

        click.echo(f"\nTasks that help you feel {outcome}:")
        if filtered:
            for t in filtered:
                click.echo(f"- {t['name']} (energy: {t['energy']})")
        else:
            click.echo("No tasks match that feeling yet.")

    else:
        click.echo("That’s not a valid option.")


# -----------------------------
# Daily Reflection
# -----------------------------
def daily_reflection(name):
    global streak_count, last_reflection_date

    today = date.today()

    if last_reflection_date == today:
        click.echo("You’ve already completed today’s reflection.")
        return

    click.echo("\n🌙 Daily Reflection")

    completed = click.prompt(
        f"What did you complete today, {name}? (comma‑separated, or 'none')"
    )

    completed_list = (
        [c.strip() for c in completed.split(",")]
        if completed.lower() != "none"
        else []
    )

    feeling = click.prompt("How did completing your tasks feel?")
    tomorrow = click.prompt("What’s one thing you’d like to focus on tomorrow?")

    reflections.append({
        "date": today,
        "completed": completed_list,
        "feeling": feeling,
        "tomorrow": tomorrow
    })

    # Update streak
    if completed_list:
        if last_reflection_date == today.replace(day=today.day - 1):
            streak_count += 1
        else:
            streak_count = 1
    else:
        streak_count = 0

    last_reflection_date = today

    click.echo(f"\nReflection saved. You’re doing beautifully, {name}.")


# -----------------------------
# View Streaks / Consistency
# -----------------------------
def view_streaks(name):
    click.echo("\n📈 Consistency Overview")
    click.echo(f"Current streak: {streak_count} day(s)")

    if reflections:
        click.echo("\nRecent reflections:")
        for r in reflections[-3:]:
            click.echo(
                f"- {r['date']}: completed {len(r['completed'])} task(s), "
                f"felt '{r['feeling']}', tomorrow: {r['tomorrow']}"
            )
    else:
        click.echo("No reflections yet — your journey starts here.")


# -----------------------------
# Main CLI Entry Point
# -----------------------------
@click.command()
@click.option('--name', prompt='Enter your name', help='Your name')
def todo(name):
    click.echo(f"\nWelcome, {name}! 🌿")
    click.echo("Let’s shape a day that meets your energy and intentions.")

    while True:
        show_menu()
        choice = click.prompt("What would you like to do?", type=int)

        if choice == 1:
            add_task()
        elif choice == 2:
            view_tasks()
        elif choice == 3:
            delete_task()
        elif choice == 4:
            view_recommended_tasks(name)
        elif choice == 5:
            daily_reflection(name)
        elif choice == 6:
            view_streaks(name)
        elif choice == 7:
            click.echo(f"Goodbye, {name}. Wishing you steadiness and clarity.")
            break
        else:
            click.echo("That option isn’t available — try again.")


if __name__ == '__main__':
    todo()
