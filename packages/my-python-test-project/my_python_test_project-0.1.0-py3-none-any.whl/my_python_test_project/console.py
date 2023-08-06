"""Command-line interface."""
import textwrap

import click

from . import __version__, wikipedia


@click.command()
@click.option(
    "--language",
    "-l",
    default="en",
    help="Language edition of Wikipedia",
    metavar="LANG",
    show_default=True,
)
@click.version_option(version=__version__)
def main(language: str) -> None:
    """Start the my python test project."""
    page = wikipedia.random_page(language)

    click.secho(page.title, fg="green")
    click.echo(textwrap.fill(page.extract))
