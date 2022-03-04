import click

from random import choice
from string import ascii_letters, digits
from sys import exit
from toml import dumps, loads


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
    with open(file, "r") as r:
        data = loads(r.read())

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
                continue_adding = input("Add next expense [Y/N]? ").lower()

        with open(file, "w") as w:
            w.write(dumps(data))
    elif list_items:
        check_options([add_items, remove_items])
        pass
    elif remove_items:
        check_options([add_items, list_items])
        pass
