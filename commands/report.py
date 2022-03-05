import click

from termcolor import colored, cprint

from .lib import create_expense_table, load_data


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
    data = load_data(file)

    budget = data["budget"] if "budget" in data.keys() else None
    currency = data["currency"]
    expenses = data["expenses"]
    if exclude:
        excludes = list()
        for expense in expenses:
            if expense["category"] == exclude:
                excludes.append(expense)
        for expense in excludes:
            expenses.remove(expense)

    cprint(
        f"Expense Report for [{data['title']}]",
        "grey",
        "on_white"
    )
    print("")

    if all:
        print(
            create_expense_table(
                data,
                columns={
                    "Item": "item",
                    "Category": "category",
                    "Cost": "cost"
                }
            )
        )
        print("")

    total_expense = sum([_["cost"] for _ in expenses])
    if budget:
        budget_left = budget - total_expense
        budget_color = "green" if budget_left > 0 else "red"
        budget_text = " ({} left)".format(
            colored(f'{budget_left}{currency}', budget_color)
        )
    else:
        budget_text = ""
    print(
        "Total expense: {}{}".format(
            colored(f"{total_expense}{currency}", "yellow"),
            budget_text
        )
    )

    if breakdown:
        print("")
        for category in sorted(
            set([expense["category"] for expense in expenses])
        ):
            total_expense_for_category = sum(
                [
                    expense["cost"] \
                    for expense in expenses \
                    if expense["category"] == category
                ]
            )
            print(
                f"Total expense for [{category}]: " + \
                colored(f"{total_expense_for_category}{currency}", "yellow")
            )
