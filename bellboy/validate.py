"""Functions and classes related to Uri validation."""
import asyncio

import aiohttp


class HttpUriValidator:
    """Custom Uri validator."""

    def __init__(self, hotels, loop, connector, **options):
        self.hotels = hotels
        self.loop = loop
        self.connector = connector
        self.options = options

    async def ping(self, hotel, session):
        """Make a get reques to a given hotel uri."""
        try:
            async with session.get(hotel['uri'], allow_redirects=False) as response:
                _ = await response.text()
                hotel['uri_status'] = response.status
                name = hotel['name']
                uri = hotel['uri']
                print(f'Ping: {response.status} {name} {uri}')
        except:  # pylint: disable=bare-except
            # Just swallow all exceptions as 500 and move on.
            name = hotel['name']
            hotel['uri_status'] = 500
            print(f'Ping: Hotel website exception handled for {name}')
        return hotel

    async def fetch_all(self):
        """Await all uri responses."""
        async with aiohttp.ClientSession(
                loop=self.loop,
                connector=self.connector
        ) as session:
            rows = [self.ping(hotel, session) for hotel in self.hotels]
            results = await asyncio.gather(*rows, return_exceptions=True)
        return results
