from fileinput import filename
import click

from toml import dumps


@click.command()
@click.argument("title")
@click.option(
    "-b",
    "--budget",
    type=int,
    help="Set budget."
)
@click.option(
    "-c",
    "--currency",
    default="€",
    help="Set currency."
)
def toml(title, budget, currency):
    """Create TOML."""
    data = dict()
    data["title"] = title
    if budget:
        data["budget"] = budget
    data["currency"] = currency
    data["expenses"] = list()

    toml_file = f"{title.replace(' ', '_').lower()}.toml"
    with open(toml_file, "w") as w:
        w.write(dumps(data))
    click.echo(f"{toml_file} successfully created.")
