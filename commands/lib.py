from operator import itemgetter
from tabulate import tabulate
from toml import dumps, loads


class ItemCost():
    def __init__(self, cost, currency):
        try:
            self.cost = int(str(cost))
        except ValueError:
            self.cost = float(str(cost))
        self.currency = currency

    def __repr__(self):
        if isinstance(self.cost, int):
            return str(self.cost) + self.currency
        else:
            return "{:.2f}{}".format(
                self.cost,
                self.currency
            ).replace(".", ",")


def create_expense_table(
        data,
        columns=None,
        sort_by="cost",
        reverse_sort=True
):
    """Creates an expense table that can be printed in a terminal."""
    table = list()
    for expense in sorted(
        data["expenses"],
        key=itemgetter(sort_by),
        reverse=reverse_sort
    ):
        table.append(
            [
                f"{ItemCost(expense[column], data['currency'])}"
                if column == "cost" else f"{expense[column]}"
                for column in columns.values()
            ]
        )
    return tabulate(table, headers=columns.keys())


def load_data(file):
    """Loads data from a TOML."""
    with open(file, "r") as f:
        data = loads(f.read())
    return data


def save_data(data, file):
    """Saves data to a TOML."""
    with open(file, "w") as f:
        f.write(dumps(data))
