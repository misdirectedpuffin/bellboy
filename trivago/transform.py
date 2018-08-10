"""Functions and classes related to the parsing of hotel.csv"""
import csv
import os


class Row(object):

    def __init__(self, row):
        self.row = row
        self._stars = None
        self._uri = None
        self._name = None

    def __str__(self):
        return self.row.__str__()

    @property
    def stars(self):
        """Property method stars."""
        if self._stars is None:
            self._stars = self.row.get('stars', str(0))
        return self._stars

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

    def has_valid_uri(self):
        """Ensure the url is valid."""
        return self.uri.startswith('http')

    def has_valid_rating(self):
        """Ensure the row has a valid star rating."""
        return all([
            int(self.stars) >= 0,
            int(self.stars) <= 5,
        ])

    def normalise_stars(self):
        """Get the existing rating or normalise it."""
        if self.has_valid_rating():
            return str(abs(int(self.stars)))
        return str(0)

    def has_valid_name(self):
        """Ensure the hotel name is a valid utf-8 string."""
        try:
            bytes(self.name, 'utf-8').decode('utf-8', 'strict')
        except:
            # logger.warning('Invalid utf-8 hotel name found for {hotel}')
            print('cannot decode from bytes')
            return False
        else:
            return True

    def is_valid(self):
        """Sanitize and validate the row."""
        return all([
            self.has_valid_name(),
            self.has_valid_uri()
        ])


def load(path, delimiter=','):
    """Return csv rows as dicts."""
    with open(path, 'r') as data:
        reader = csv.DictReader(
            data,
            delimiter=delimiter
        )
        for row in reader:
            yield row
