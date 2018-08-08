"""Console script for trivago."""
import sys
import click

from trivago.transform import load

@click.group()
def entrypoint():
    """Entrypoint to CLI."""


@entrypoint.command()
@click.option('--output', type=click.Choice(['json', 'yaml']), default='json')
def parse(output):
    """Parse the csv"""
    pass


if __name__ == "__main__":
    sys.exit(entrypoint())  # pragma: no cover
