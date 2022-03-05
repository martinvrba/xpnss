import click

from random import choice
from string import ascii_letters, digits
from sys import exit

from .lib import create_expense_table, load_data, save_data


def check_options(disallowed_options):
    for option in disallowed_options:
        if option:
            click.echo("Only one option can be used at a time!")
            exit(1)


def generate_id():
    return "".join([choice(ascii_letters + digits) for _ in range(8)])


@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "-a",
    "--add-items",
    is_flag=True,
    help="Add items."
)
@click.option(
    "-l",
    "--list-items",
    is_flag=True,
    help="List items."
)
@click.option(
    "-r",
    "--remove-items",
    is_flag=True,
    help="Remove items."
)
def item(file, add_items, list_items, remove_items):
    """Manage items."""
    data = load_data(file)

    if add_items:
        check_options([list_items, remove_items])

        continue_adding = "y"
        while continue_adding == "y":
            expense = input("Enter expense [item,category,cost]: ").split(",")
            data["expenses"].append(
                {
                    "id": generate_id(),
                    "item": expense[0],
                    "category": expense[1],
                    "cost": int(expense[2])
                }
            )
            continue_adding = ""
            while continue_adding not in ["y", "n"]:
                continue_adding = input("Add another item [Y/N]? ").lower()

        save_data(data, file)
    elif list_items:
        check_options([add_items, remove_items])

        print(
            create_expense_table(
                data,
                columns={
                    "ID": "id",
                    "Item": "item",
                    "Category": "category",
                    "Cost": "cost"
                }
            )
        )
    elif remove_items:
        check_options([add_items, list_items])

        id = input("Enter ID of item to remove: ")
        for expense in data["expenses"]:
            if expense["id"] == id:
                expense_to_remove = expense
                break
        data["expenses"].remove(expense_to_remove)

        save_data(data, file)
