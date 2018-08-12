"""Functions and classes related to Uri validation."""
import asyncio

import aiohttp
import click


class HttpUriValidator(object):

    def __init__(self, hotels, loop, connector, **options):
        self.hotels = hotels
        self.loop = loop
        self.connector = connector
        self.options = options

    async def ping(self, hotel, session):
        try:
            async with session.get(hotel.uri) as response:
                jsn = await response.json()
                hotel.valid = None
        except asyncio.TimeoutError:
            hotel.valid = False
        finally:
            print(f'Ping: {response.status} {hotel.name} {hotel.uri}')
            hotel.valid = True if response.status == 200 else False
            return hotel

    async def fetch_all(self):
        """Await all uri responses."""
        async with aiohttp.ClientSession(
            loop=self.loop,
            connector=self.connector
        ) as session:
            rows = [self.ping(hotel, session) for hotel in self.hotels]
            results = await asyncio.gather(*rows, return_exceptions=True)
            click.echo('\nAll results collected...')
        return results

    async def hotel_data(self):
        """Ping all uri's within a non-blocking event loop."""
        return self.loop.run_until_complete(self.fetch_all())
