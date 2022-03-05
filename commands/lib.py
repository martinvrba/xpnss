from operator import itemgetter
from tabulate import tabulate
from toml import dumps, loads


def create_expense_table(data, columns=None, sort_by="cost"):
    table = list()
    for expense in sorted(data["expenses"], key=itemgetter(sort_by)):
        table.append(
            [
                f"{expense[column]}{data['currency']}" \
                if column == "cost" else f"{expense[column]}" \
                for column in columns.values()
            ]
        )
    return tabulate(table, headers=list(columns))


def load_data(file):
    with open(file, "r") as f:
        data = loads(f.read())
    return data


def save_data(data, file):
    with open(file, "w") as f:
        f.write(dumps(data))
