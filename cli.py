#!python3

import click

from commands.item import item
from commands.report import report
from commands.toml import toml


@click.group()
def cli():
    pass


if __name__ == "__main__":
    cli.add_command(item)
    cli.add_command(report)
    cli.add_command(toml)
    cli(prog_name="xpnss")
