"""Unit tests related to transform.py"""
import os
from collections import OrderedDict

import pytest

from trivago.transform import Row, load


def test_load(tmpdir):
    """It returns the expected loaded data."""
    os.chdir(tmpdir)
    with open('test.csv', 'w') as test_file:
        test_file.write(
            'name,'
            'address,'
            'stars,'
            'contact,'
            'phone,'
            'uri,'
            '\n'
            'The Gibson,'
            '"63847 Lowe Knoll, East Maxine, WA 97030-4876",'
            '5,'
            'Dr. Sinda Wyman,'
            '1-270-665-9933x1626,'
            'http://www.paucek.com/search.htm'
        )
    assert list(load('test.csv')) == [
        OrderedDict([
            ('name', 'The Gibson'),
            ('address', '63847 Lowe Knoll, East Maxine, WA 97030-4876'),
            ('stars', '5'),
            ('contact', 'Dr. Sinda Wyman'),
            ('phone', '1-270-665-9933x1626'),
            ('uri', 'http://www.paucek.com/search.htm'),
            ('', None)
        ])
    ]


@pytest.mark.parametrize('mock_row, expected', [
    (Row(OrderedDict([('stars', '-1')])), False),
    (Row(OrderedDict([('stars', '0')])), True),
    (Row(OrderedDict([('stars', '1')])), True),
    (Row(OrderedDict([('stars', '5')])), True),
    (Row(OrderedDict([('stars', '6')])), False)
])
def test_has_valid_rating(mock_row, expected):
    """It returns the expected bool, given a rating."""
    assert mock_row.has_valid_rating() == expected


@pytest.mark.parametrize('mock_row, expected', [
    (Row(OrderedDict([('stars', '0')])), '0'),
    (Row(OrderedDict([('stars', '-1')])), '0'),
    (Row(OrderedDict([('stars', '6')])), '0'),
    (Row(OrderedDict([('stars', '-0')])), '0'),
])
def test_normalise_stars(mock_row, expected):
    """It returns a normalised star rating given a row."""
    assert mock_row.normalise_stars() == expected


@pytest.mark.parametrize('mock_row, expected', [
    (
        Row(OrderedDict([
            ('name', 'somehotel'),
            ('uri', 'https://in.hotel.com/')
        ])),
        True
    ),
    (
        Row(OrderedDict([
            ('name', 'somehotel'),
            ('uri', 'ftpp://in.hotel/')
        ])),
        False
    )
])
def test_is_valid_row(mock_row, expected):
    """It returns the expected bool given a row."""
    assert mock_row.is_valid() == expected


# pylint: disable=protected-access
def test_make_code_points():
    """It returns the expected ord value of a character."""
    row = Row(OrderedDict([('name', 'test-name')]))
    assert list(row._make_code_points()) == [
        116, 101, 115, 116, 45, 110, 97, 109, 101
    ]


def test_has_valid_name_false():
    """It returns False given an invalid string."""
    row = Row(OrderedDict([('name', 'Apartment Dörr')]))
    assert not row.has_valid_name()


def test_has_valid_name_true():
    """It returns True given a valid string."""
    row = Row(OrderedDict([('name', 'Apartment Dorr')]))
    assert row.has_valid_name()


def test_has_valid_uri_format_true():
    """It returns the expected bool given an uri."""
    row = Row(OrderedDict([('uri', 'https://news.ycombinator.com/')]))
    assert row.has_valid_uri_format()


def test_has_valid_uri_format_false():
    """It returns the expected bool given an uri."""
    row = Row(OrderedDict([('uri', 'news.ycombinator.com/')]))
    assert not row.has_valid_uri_format()
