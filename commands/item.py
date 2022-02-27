import click


@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "-a",
    "--add",
    help="Add item."
)
@click.option(
    "-l",
    "--list",
    is_flag=True,
    help="List items."
)
@click.option(
    "-r",
    "--remove",
    help="Remove item."
)
def item(file, add, list, remove):
    """Manage items."""
    pass
