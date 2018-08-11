"""Unit test fixtures"""
from collections import OrderedDict

import pytest
from lxml import etree

from trivago.transform import Row


@pytest.fixture(scope='module')
def mock_hotel_root():
    """Make a hotels element."""
    yield etree.Element("hotels")


@pytest.fixture
def mock_hotel_row():
    """Make a single row as returned by the csv parser."""
    return Row(OrderedDict(
        [
            ("address", (
                "Stretto Bernardi 004,"
                " Quarto Mietta nell'emilia,"
                " 07958 Torino (OG)"
            )),
            ("contact", "Rosalino Marchetti"),
            ("name", "Martini Cattaneo"),
            ("phone", "+39 627 68225719"),
            ("stars", "5"),
            ("uri", "http://www.farina.org/blog/categories/tags/about.html")
        ]
    ))

@pytest.fixture(scope='module')
def mock_hotel_rows():
    """Make two rows as returned by the csv parser."""
    return [
        Row(OrderedDict(
            [
                ("address", (
                    "Stretto Bernardi 004,"
                    " Quarto Mietta nell'emilia,"
                    " 07958 Torino (OG)"
                )),
                ("contact", "Rosalino Marchetti"),
                ("name", "Martini Cattaneo"),
                ("phone", "+39 627 68225719"),
                ("stars", "5"),
                ("uri", "http://www.farina.org/blog/categories/tags/about.html"),
            ]
        )),
        Row(OrderedDict(
            [
                ("address", "Bolzmannweg 451, 05116 Hannover"),
                ("contact", "Scarlet Kusch-Linke"),
                ("name", "Apartment Dörr"),
                ("phone", "08177354570"),
                ("stars", "1"),
                ("uri", "http://www.garden.com/list/home.html")
            ]
        ))]
