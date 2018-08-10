"""Console script for trivago."""
import os
import sys
import click

from trivago.transform import load, is_valid_row, file_output_factory


def get_current_directory():
    return os.path.dirname(os.path.realpath(__file__))


def output_directory(ctx, param, value):
    return os.path.join(get_current_directory(), '..', 'data')


@click.group()
def entrypoint():
    """Entrypoint to CLI."""


@entrypoint.command()
@click.option('--outfile', default='hotel')
@click.option('--infile', default='hotel.csv')
@click.option('--data-dir', type=click.Path(exists=True), default=output_directory)
@click.option('--output-format', type=click.Choice(['json', 'yaml']), default='json')
def parse(output_format, data_dir, infile, outfile):
    """Parse the csv"""
    data = load(os.path.join(data_dir, infile))
    rows = list(filter(is_valid_row, data))
    output_func = file_output_factory(output_format)
    filename = '.'.join([outfile, output_format])
    output_func(os.path.join(data_dir, filename), rows)



if __name__ == "__main__":
    sys.exit(entrypoint())  # pragma: no cover
