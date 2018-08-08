"""Unit tests related to transform.py"""
import os

import pytest
from collections import OrderedDict

from trivago.transform import load


def test_load(tmpdir):
    """It returns the expected loaded data."""
    os.chdir(tmpdir)
    with open('test.csv', 'w') as test_file:
        test_file.write(
            'The Gibson,'
            '"63847 Lowe Knoll, East Maxine, WA 97030-4876",'
            '5,'
            'Dr. Sinda Wyman,'
            '1-270-665-9933x1626,'
            'http://www.paucek.com/search.htm,'
        )
    assert list(load('test.csv')) == [
        OrderedDict([
            ('name', 'The Gibson'),
            ('address', '63847 Lowe Knoll, East Maxine, WA 97030-4876'),
            ('stars', '5'),
            ('contact', 'Dr. Sinda Wyman'),
            ('phone', '1-270-665-9933x1626'),
            ('uri', 'http://www.paucek.com/search.htm'),
            (None, [''])
        ])
    ]
