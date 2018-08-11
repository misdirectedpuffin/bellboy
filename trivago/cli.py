"""Console script for trivago."""
import os
import sys

import click

from trivago.export import JsonExport, XmlExport, factory
from trivago.transform import Row, load


def get_current_directory():
    """Make path to directory containing current file."""
    return os.path.dirname(os.path.realpath(__file__))


def output_directory(ctx, param, value):
    """Make path to data directory."""
    return os.path.join(get_current_directory(), '..', 'data')


def make_file_name(outfile, output_format):
    """Join the name with the format as suffix."""
    return '.'.join([outfile, output_format])


@click.group()
def entrypoint():
    """Entrypoint to CLI."""


@entrypoint.command()
@click.option('--write', is_flag=True, default=False)
@click.option('--outfile', default='hotels')
@click.option('--infile', default='hotels.csv')
@click.option(
    '--data-dir',
    type=click.Path(exists=True),
    callback=output_directory
)
@click.option(
    '--output-format',
    type=click.Choice(['json', 'xml']),
    default='json'
)
def parse(output_format, data_dir, infile, outfile, write):
    """Parse the csv"""
    data = load(os.path.join(data_dir, infile))
    rows = (row for row in data if row.is_valid())

    if all([write, outfile]):
        filename = make_file_name(outfile, output_format)
        outpath = os.path.join(data_dir, filename)
        click.echo(outpath)
        click.echo(filename)
        ExportHandler = factory(output_format)
        export = ExportHandler(rows)
        return export.write(outpath)
    click.echo('You didn\'t specify whether or where to write to a file....')


if __name__ == "__main__":
    sys.exit(entrypoint())  # pragma: no cover
