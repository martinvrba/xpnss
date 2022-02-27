import click


@click.command()
@click.argument("file")
@click.option(
    "-t",
    "--title",
    help="Set title."
)
@click.option(
    "-b",
    "--budget",
    help="Set budget."
)
@click.option(
    "-c",
    "--currency",
    help="Set currency."
)
def toml(file, title, budget, currency):
    """Create TOML."""
    pass
