"""Unit tests related to transform.py"""
import os
from collections import OrderedDict

import pytest
from lxml import etree

from trivago.transform import (has_valid_rating, is_valid_row, load,
                               make_hotel_nodes, make_xml_document,
                               normalise_stars)


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


@pytest.mark.parametrize('rating, expected', [
    ('-1', False),
    ('0', True),
    ('1', True),
    ('5', True),
    ('6', False),
])
def test_has_valid_rating(rating, expected):
    """It returns the expected bool, given a rating."""
    assert has_valid_rating(rating) == expected


@pytest.mark.parametrize('row, expected', [
    (OrderedDict([('stars', '0')]), '0'),
    (OrderedDict([('stars', '-1')]), '0'),
    (OrderedDict([('stars', '6')]), '0'),
    (OrderedDict([('stars', '-0')]), '0'),
])
def test_normalise_stars(row, expected):
    """It returns a normalised star rating given a row."""
    assert normalise_stars(row) == expected


@pytest.mark.parametrize('row, expected', [
    (
        OrderedDict([
            ('name', 'somehotel'),
            ('uri', 'https://in.hotel.com/')
        ]),
        True
    ),
    (
        OrderedDict([
            ('name', 'somehotel'),
            ('uri', 'ftp://in.hotel.com/')
        ]),
        False
    )
])
def test_is_valid_row(row, expected):
    """It returns the expected bool given a row."""
    assert is_valid_row(row) == expected


def test_make_hotel_nodes(mock_hotel_root, mock_hotel_row):
    """It returns the expected xml given the parent element."""
    hotel = etree.SubElement(mock_hotel_root, "hotel")
    expected = b"<hotels>\n  <hotel>\n    <address>Stretto Bernardi 004, Quarto Mietta nell'emilia, 07958 Torino (OG)</address>\n    <contact>Rosalino Marchetti</contact>\n    <name>Martini Cattaneo</name>\n    <phone>+39 627 68225719</phone>\n    <stars>5</stars>\n    <uri>http://www.farina.org/blog/categories/tags/about.html</uri>\n  </hotel>\n</hotels>\n"  # pylint: disable=line-too-long
    make_hotel_nodes(hotel, **mock_hotel_row)
    # print(etree.tostring(mock_hotel_root, pretty_print=True))
    assert etree.tostring(mock_hotel_root, pretty_print=True) == expected


def test_make_xml_document(mock_hotel_rows):
    """It returns the expected xml given a list of OrderedDicts"""
    expected = b"<hotels>\n  <hotel>\n    <address>Stretto Bernardi 004, Quarto Mietta nell'emilia, 07958 Torino (OG)</address>\n    <contact>Rosalino Marchetti</contact>\n    <name>Martini Cattaneo</name>\n    <phone>+39 627 68225719</phone>\n    <stars>5</stars>\n    <uri>http://www.farina.org/blog/categories/tags/about.html</uri>\n  </hotel>\n  <hotel>\n    <address>Bolzmannweg 451, 05116 Hannover</address>\n    <contact>Scarlet Kusch-Linke</contact>\n    <name>Apartment D&#246;rr</name>\n    <phone>08177354570</phone>\n    <stars>1</stars>\n    <uri>http://www.garden.com/list/home.html</uri>\n  </hotel>\n</hotels>\n"  # pylint: disable=line-too-long
    root = make_xml_document(mock_hotel_rows, collection='hotels')
    # root.write('tests.xml', encoding='utf-8')
    assert etree.tostring(root, pretty_print=True) == expected
