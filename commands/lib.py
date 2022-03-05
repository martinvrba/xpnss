from operator import itemgetter
from tabulate import tabulate
from toml import dumps, loads


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
                f"{expense[column]}{data['currency']}" \
                if column == "cost" else f"{expense[column]}" \
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
