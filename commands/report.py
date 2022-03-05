import click

from operator import itemgetter
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
@click.option(
    "-o",
    "--output-format",
    default="terminal",
    help="Set output format."
)
def report(file, all, breakdown, exclude, output_format):
    """Output expense report."""
    data = load_data(file)

    currency = data["currency"]
    expenses = data["expenses"]

    if exclude:
        excludes = list()
        for expense in expenses:
            if expense["category"] == exclude:
                excludes.append(expense)
        for expense in excludes:
            expenses.remove(expense)

    total_expense = sum([expense["cost"] for expense in expenses])

    if "budget" in data.keys():
        budget = data["budget"]
        budget_left = budget - total_expense
    else:
        budget = None

    if breakdown:
        expenses_by_category = list()
        categories = set([expense["category"] for expense in expenses])
        for category in categories:
            expenses_by_category.append(
                {
                    "name": category,
                    "total_expense": sum(
                        [
                            expense["cost"] \
                            for expense in expenses \
                            if expense["category"] == category
                        ]
                    )
                }
            )

    if output_format == "terminal":
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

        if budget:
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
                expenses_by_category,
                key=itemgetter("total_expense")
            ):
                print(
                    f"Total expense for [{category['name']}]: " + \
                    colored(f"{category['total_expense']}{currency}", "yellow")
                )
