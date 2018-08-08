"""Functions and classes related to the parsing of hotel.csv"""
import csv
import os

FIELDS = [
    'name',
    'address',
    'stars',
    'contact',
    'phone',
    'uri'
]


def load(path, fieldnames=FIELDS, delimiter=','):
    """Return csv rows as dicts."""
    with open(path, 'r') as data:
        reader = csv.DictReader(
            data,
            fieldnames=fieldnames,
            delimiter=delimiter
        )
        for row in reader:
            yield row
