"""Console script for trivago."""
import asyncio
import os
import sys
from functools import update_wrapper

import aiohttp
import click

from trivago.export import factory
from trivago.transform import load, Row
from trivago.validate import HttpUriValidator


# pylint: disable=unused-argument
def output_directory(ctx, param, value):
    """Make path to data directory."""
    return os.path.join(os.getcwd(), 'data')


def make_file_name(outfile, output_format):
    """Join the name with the format as suffix."""
    return '.'.join([outfile, output_format])


def write(rows, outpath, outfile, output_format):
    """Handle writing rows to file."""
    if outfile:
        export_handler = factory(output_format)
        export = export_handler(rows)
        return export.write(outpath)


def coro(func):
    """Update the wrapper with the incoming function."""
    fn_coro = asyncio.coroutine(func)

    def wrapper(*args, **kwargs):
        """Inner wrapper"""
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(fn_coro(*args, **kwargs))
    return update_wrapper(wrapper, fn_coro)


@click.group()
@click.pass_context
def entrypoint(ctx):
    """Entrypoint to CLI."""
    ctx.obj = asyncio.get_event_loop()

# pylint: disable=too-many-arguments
@entrypoint.command()
@click.option(
    '-s',
    '--http-status',
    default=200,
    help='Only return uris with this http status.'
)
@click.option(
    '-p',
    '--ping',
    is_flag=True,
    default=False,
    help='Make async http requests for uri validation.'
)
@click.option(
    '-f',
    '--output-format',
    type=click.Choice(['json', 'xml']),
    default='json',
    help='The desired output format.'
)
@click.option(
    '-o',
    '--outfile',
    default='hotels',
    help='Output file name (without extension).'
)
@click.option(
    '-i',
    '--infile',
    type=click.Path(exists=True),
    default='./data/hotels.csv',
    help='The input file.'
)
@coro
@click.pass_obj
async def parse(loop, infile, outfile, output_format, ping, http_status):
    """Parse the csv"""
    hotels = load(infile)

    if ping:
        confirmation = click.confirm(
            f'You are about to make multiple async http requests. '
            'Are you sure you want to continue?',
            default='Yes'
        )

    if not confirmation:
        sys.exit(0)

    connector = aiohttp.TCPConnector(verify_ssl=False)
    validator = HttpUriValidator(hotels, loop, connector)
    hotels = await validator.fetch_all()
    click.echo('All Uri\'s returned...')

    filename = make_file_name(outfile, output_format)
    outpath = os.path.join(os.path.dirname(infile), filename)

    hotels = (Row(hotel) for hotel in hotels)
    valid = (hotel for hotel in hotels if all([
        hotel.has_valid_name(),
        hotel.uri_status == http_status
    ]))
    write(valid, outpath, outfile, output_format)
    click.echo(f'Your data is available at: {outpath}')


if __name__ == "__main__":
    sys.exit(entrypoint({}))  # pragma: no cover
