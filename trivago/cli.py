"""Console script for trivago."""
import asyncio
import os
import sys
from functools import update_wrapper

import aiohttp
import click

from trivago.export import JsonExport, XmlExport, factory
from trivago.transform import Row, load
from trivago.validate import HttpUriValidator


def output_directory(ctx, param, value):
    """Make path to data directory."""
    return os.path.join(os.getcwd(), 'data')


def make_file_name(outfile, output_format):
    """Join the name with the format as suffix."""
    return '.'.join([outfile, output_format])


def write(rows, should_write, outfile, data_dir, output_format):
    if all([should_write, outfile]):
        filename = make_file_name(outfile, output_format)
        outpath = os.path.join(data_dir, filename)
        ExportHandler = factory(output_format)
        export = ExportHandler(rows)
        export.write(outpath)


def coro(f):
    f = asyncio.coroutine(f)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))
    return update_wrapper(wrapper, f)


@click.group()
@click.pass_context
def entrypoint(ctx):
    """Entrypoint to CLI."""
    ctx.obj = asyncio.get_event_loop()


@entrypoint.command()
@click.option('--ping', is_flag=True, default=False)
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
@coro
@click.pass_obj
async def parse(loop, output_format, data_dir, infile, outfile, write, ping):
    """Parse the csv"""
    data = load(os.path.join(data_dir, infile))
    rows = (row for row in data if row.is_valid())

    if ping:
        confirmation = click.confirm(
            'You are about to make a large number of http requests. '
            'Are you sure you want to continue?',
            default='Yes'
        )

        if confirmation:
            connector = aiohttp.TCPConnector(verify_ssl=False)
            validator = HttpUriValidator(rows, loop, connector)
            return await validator.fetch_all()

if __name__ == "__main__":
    sys.exit(entrypoint({}))  # pragma: no cover
