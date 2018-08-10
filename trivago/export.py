"""Classes related to data export format."""
import json

from lxml import etree


def factory(export_format):
    """Get the Export class definition based on format."""
    return {
        'json': JsonExport,
        'xml': XmlExport
    }.get(export_format)


class Export(object):

    def __init__(self, rows):
        self.rows = rows

    def write(self):
        """Abstract method write."""
        raise NotImplementedError

    def get_document(self):
        """Abstract method get_document."""
        raise NotImplementedError


class JsonExport(Export):

    def __init__(self, rows):
        super(JsonExport, self).__init__(rows)
        self.rows = rows

    def write(self, path, mode='w', ensure_ascii=False):
        """Write json data to file."""
        with open(path, mode=mode) as outfile:
            json.dump(
                list(self.rows),
                outfile,
                ensure_ascii=ensure_ascii,
                sort_keys=True,
                indent=4
            )

    def get_document(self, ensure_ascii=False):
        """Make a json string from the valid row data."""
        return json.dumps(
            list(self.rows),
            ensure_ascii=ensure_ascii,
            sort_keys=True,
            indent=4
        )


class XmlExport(Export):

    def __init__(self, rows):
        super(XmlExport, self).__init__(rows)
        self.rows = rows

    def write(self, path, collection='hotels', declaration=True):
        """Write a valid XML document."""
        root = self.get_document(collection=collection)
        tree = etree.ElementTree(root)
        tree.write(
            path,
            xml_declaration=declaration,
            encoding='UTF-8',
            pretty_print=True
        )

    def get_document(self, collection='hotels'):
        """Make an xml document from rows.

        <hotel>
            <address>63847 Lowe Knoll, East Maxine, WA 97030-4876</address>
            <contact>Dr. Sinda Wyman</contact>
            ...
        </hotel>
        """
        root = etree.Element(collection)
        for row in self.rows:
            hotel = etree.SubElement(root, "hotel")
            self.make_nodes(hotel, **row)
        return root

    @staticmethod
    def make_nodes(hotel, **row):
        """Make a sequence of nodes in a hotel element.

        <address>63847 Lowe Knoll, East Maxine, WA 97030-4876</address>
        <contact>Dr. Sinda Wyman</contact>
        ...
        """
        for name, value in row.items():
            node = etree.SubElement(hotel, name)
            setattr(node, 'text', value)
