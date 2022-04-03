import click

from operator import itemgetter
from random import choice
from termcolor import colored, cprint

from .lib import create_expense_table, ItemCost, load_data
from module import Data, BarChart, Args, Colors


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

    total_expense = round(sum([expense["cost"] for expense in expenses]), 2)

    if "budget" in data.keys():
        budget = data["budget"]
        budget_left = round(budget - total_expense, 2)
    else:
        budget = None

    if breakdown:
        expenses_by_category = list()
        categories = set([expense["category"] for expense in expenses])
        for category in categories:
            expenses_by_category.append(
                {
                    "name": category,
                    "total_expense": round(sum(
                        [
                            expense["cost"]
                            for expense in expenses
                            if expense["category"] == category
                        ]
                    ), 2)
                }
            )

    if output_format == "terminal":
        cprint(
            f"Expense Report for [{data['title']}]",
            "grey",
            "on_white"
        )
        print("\n")

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
            print("\n")

        if budget:
            budget_color = "green" if budget_left > 0 else "red"
            budget_text = " ({}".format(
                colored(
                    f"{ItemCost(abs(budget_left), currency)}",
                    budget_color
                )
            )
            budget_text += " left)" if budget_left > 0 else " over)"
        else:
            budget_text = ""
        print(
            "Total expense: {}{}".format(
                colored(f"{ItemCost(total_expense, currency)}", "yellow"),
                budget_text
            )
        )

        if breakdown:
            chart_values = list()
            chart_legend = list()
            available_colors = [
                Colors.Blue, Colors.Cyan, Colors.Green,
                Colors.Magenta, Colors.Red, Colors.Yellow
            ]

            print("\n")
            for category in sorted(
                expenses_by_category,
                key=itemgetter("total_expense"),
                reverse=True
            ):
                print(
                    f"Total expense for [{category['name']}]: " +
                    colored(
                        f"{ItemCost(category['total_expense'], currency)}",
                        "yellow"
                    )
                )
                if len(chart_legend) < len(available_colors):
                    chart_values.append(category["total_expense"])
                    chart_legend.append(category["name"])

            chart_data = Data([chart_values], [""], chart_legend)
            picked_colors = list()
            for category in chart_legend:
                color = choice(available_colors)
                picked_colors.append(color)
                available_colors.remove(color)
            chart_legend_width = len("".join(chart_legend))
            if chart_legend_width > 50:
                chart_width = chart_legend_width
            else:
                chart_width = 50

            chart = BarChart(
                chart_data,
                Args(
                    colors=picked_colors,
                    no_labels=True,
                    width=chart_width
                )
            )
            print("\n")
            chart.draw()
