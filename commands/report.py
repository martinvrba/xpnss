import click

from operator import itemgetter
from tabulate import tabulate
from termcolor import colored, cprint
from toml import loads


@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "-a",
    "--all",
    is_flag=True,
    help="Print all expenses."
)
@click.option(
    "-b",
    "--breakdown",
    is_flag=True,
    help="Print expense breakdown by category."
)
@click.option(
    "-e",
    "--exclude",
    help="Category to exclude."
)
def report(file, all, breakdown, exclude):
    """Print expense report."""
    with open(file, "r") as r:
        parsed_input = loads(r.read())

    expenses = parsed_input["expenses"]
    if exclude:
        excludes = list()
        for expense in expenses:
            if expense["category"] == exclude:
                excludes.append(expense)
        for expense in excludes:
            expenses.remove(expense)
    budget = parsed_input["budget"]
    if "currency" in parsed_input.keys():
        currency = parsed_input["currency"]
    else:
        currency = "€"

    cprint(
        f"Expense Report for [{parsed_input['title']}]",
        "grey",
        "on_white"
    )
    print("")

    if all:
        table = list()
        for expense in sorted(expenses, key=itemgetter("cost")):
            table.append(
                [
                    expense["item"],
                    expense["category"],
                    f"{expense['cost']}{currency}"
                ]
            )

        print(tabulate(table, headers=["Item", "Category", "Cost"]))
        print("")

    total_expense = sum([_["cost"] for _ in expenses])
    budget_left = budget - total_expense
    budget_color = "green" if budget_left > 0 else "red"
    print(
        "Total expense: {} ({} left)".format(
            colored(f"{total_expense}{currency}", "yellow"),
            colored(f"{budget_left}{currency}", budget_color)
        )
    )

    if breakdown:
        print("")
        for category in sorted(set([_["category"] for _ in expenses])):
            total_expense_for_category = sum(
                [_["cost"] for _ in expenses if _["category"] == category]
            )
            print(
                f"Total expense for [{category}]: " + colored(
                    f"{total_expense_for_category}{currency}", "yellow"
                )
            )
