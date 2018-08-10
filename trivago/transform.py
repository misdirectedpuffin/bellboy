"""Functions and classes related to the parsing of hotel.csv"""
import csv
import os
import json
import yaml

from lxml import etree

FIELDS = [
    'name',
    'address',
    'stars',
    'contact',
    'phone',
    'uri'
]


def load(path, delimiter=','):
    """Return csv rows as dicts."""
    with open(path, 'r') as data:
        reader = csv.DictReader(
            data,
            delimiter=delimiter
        )
        for row in reader:
            yield row


def is_valid_uri(uri):
    """Ensure the url is valid."""
    valid = uri.startswith('http')
    return valid


def has_valid_rating(rating):
    return all([
        int(rating) >= 0,
        int(rating) <= 5,
    ])


def normalise_stars(row):
    """Get the existing rating or normalise it."""
    return str(abs(int(row.get('stars', 0)))) if has_valid_rating(row.get('stars', str(0))) else str(0)


def is_valid_hotel_name(hotel_name):
    """Ensure the hotel name is a valid utf-8 string."""
    try:
        bytes(hotel_name, 'utf-8').decode('utf-8', 'strict')
    except:
        # logger.warning('Invalid utf-8 hotel name found for {hotel}')
        print('cannot decode from bytes')
        return False
    else:
        return True


def is_valid_row(row):
    """Sanitize and validate the row."""
    return all([
        is_valid_hotel_name(row['name']),
        is_valid_uri(row['uri'])
    ])


def make_json(valid_rows, ensure_ascii=False):
    """Output a json string from the valid row data."""
    return json.dumps(
        list(valid_rows),
        ensure_ascii=ensure_ascii,
        sort_keys=True,
        indent=4
    )


def make_json_file(path, data, mode='w', ensure_ascii=False):
    with open(path, mode=mode) as out:
        json.dump(
            list(data),
            out,
            ensure_ascii=ensure_ascii,
            sort_keys=True,
            indent=4
        )


def make_hotel_nodes(hotel, **row):
    """Make a sequence of nodes in a hotel element.

    <address>63847 Lowe Knoll, East Maxine, WA 97030-4876</address>
    <contact>Dr. Sinda Wyman</contact>
    ...
    """
    for name, value in row.items():
        node = etree.SubElement(hotel, name)
        setattr(node, 'text', value)


def make_xml_document(rows, collection='hotels'):
    """Make an xml document from rows.

    <hotel>
        <address>63847 Lowe Knoll, East Maxine, WA 97030-4876</address>
        <contact>Dr. Sinda Wyman</contact>
        ...
    </hotel>
    """
    root = etree.Element(collection)
    for row in rows:
        hotel = etree.SubElement(root, "hotel")
        make_hotel_nodes(hotel, **row)
    return root


def make_xml_file(path, rows, collection='hotels'):
    """Write a valid XML document."""
    root = make_xml_document(rows, collection=collection)
    tree = etree.ElementTree(root)
    tree.write(path, xml_declaration=True, encoding='UTF-8', pretty_print=True)


def file_output_factory(output):
    """Provide the correct output format function."""
    return {
        'json': make_json_file,
        'xml': make_xml_file,
    }.get(output)


if __name__ == '__main__':
    directory = os.path.dirname(os.path.realpath(__file__))
    data = load(os.path.join(directory, '../data/hotels.csv'))
    rows = list(filter(is_valid_row, data))
    output_format = 'xml'
    outfile = 'hotel'
    output_func = file_output_factory(output_format)
    filename = '.'.join([outfile, output_format])
    output_func(os.path.join(directory, filename), rows)
