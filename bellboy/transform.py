"""Functions and classes related to the parsing of hotel.csv"""
import csv

from collections import OrderedDict
from itertools import product
from operator import ne

INVALID_CODE_POINTS = (
    192,
    193,
    245,
    246,
    247,
    248,
    249,
    250,
    251,
    252,
    253,
    254,
    255,
)


class Row(OrderedDict):
    """Custom OrderedDict."""

    def __init__(self, *args, **kwargs):
        self.row = args[0]
        self._stars = None
        self._uri = None
        self._name = None
        self._valid_uri_format = None
        self._uri_status = None
        super(Row, self).__init__(*args, **kwargs)

    @property
    def stars(self):
        """Property method stars."""
        if self._stars is None:
            self._stars = self.row.get('stars', 0)
        return int(self._stars)

    @property
    def uri(self):
        """Property method uri."""
        if self._uri is None:
            self._uri = self.row.get('uri')
        return self._uri

    @property
    def name(self):
        """Property method name."""
        if self._name is None:
            self._name = self.row.get('name')
        return self._name

    @property
    def uri_status(self):
        """Property method valid."""
        if self._uri_status is None:
            self._uri_status = self.row.get('uri_status')
        return self._uri_status

    @uri_status.setter
    def uri_status(self, value):
        # self._uri_status = value
        self.row['uri_status'] = str(value)

    def has_valid_rating(self):
        """Ensure the row has a valid star rating."""
        return all([
            int(self.stars) >= 0,
            int(self.stars) <= 5,
        ])

    def normalise_stars(self):
        """Get the existing rating or normalise it."""
        if self.has_valid_rating():
            return abs(int(self.stars))
        return 0

    def has_valid_name(self):
        """Ensure the hotel name is a valid utf-8 string."""
        return all(ne(*pair) for pair in product(
            self._make_code_points(),
            INVALID_CODE_POINTS
        ))

    def _make_code_points(self):
        for char in self.name:
            yield ord(char)


def load(path, delimiter=','):
    """Return csv rows as OrderedDicts."""
    with open(path, 'r') as data:
        reader = csv.DictReader(
            data,
            delimiter=delimiter
        )
        for row in reader:
            yield row
