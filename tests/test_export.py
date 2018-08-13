"""Unit tests related to export."""
from lxml import etree

from trivago.export import XmlExport, JsonExport


# pylint: disable=no-self-use
class TestXmlExport:
    """Group Xml tests."""

    def test_make_nodes(self, mock_hotel_root, mock_hotel_row):
        """It returns the expected xml given the parent element."""
        hotel = etree.SubElement(mock_hotel_root, "hotel")
        expected = b"<hotels>\n  <hotel>\n    <address>Stretto Bernardi 004, Quarto Mietta nell'emilia, 07958 Torino (OG)</address>\n    <contact>Rosalino Marchetti</contact>\n    <name>Martini Cattaneo</name>\n    <phone>+39 627 68225719</phone>\n    <stars>5</stars>\n    <uri>http://www.farina.org/blog/categories/tags/about.html</uri>\n  </hotel>\n</hotels>\n"  # pylint: disable=line-too-long
        XmlExport(None).make_nodes(hotel, **mock_hotel_row)
        assert etree.tostring(mock_hotel_root, pretty_print=True) == expected

    def test_get_document(self, mock_hotel_rows):
        """It returns the expected xml given a list of OrderedDicts"""
        expected = b"<hotels>\n  <hotel>\n    <address>Stretto Bernardi 004, Quarto Mietta nell'emilia, 07958 Torino (OG)</address>\n    <contact>Rosalino Marchetti</contact>\n    <name>Martini Cattaneo</name>\n    <phone>+39 627 68225719</phone>\n    <stars>5</stars>\n    <uri>http://www.farina.org/blog/categories/tags/about.html</uri>\n  </hotel>\n  <hotel>\n    <address>Bolzmannweg 451, 05116 Hannover</address>\n    <contact>Scarlet Kusch-Linke</contact>\n    <name>Apartment D&#246;rr</name>\n    <phone>08177354570</phone>\n    <stars>1</stars>\n    <uri>http://www.garden.com/list/home.html</uri>\n  </hotel>\n</hotels>\n"  # pylint: disable=line-too-long
        export = XmlExport(mock_hotel_rows)
        root = export.get_document()
        assert etree.tostring(root, pretty_print=True) == expected


    def test_get_document_json(self, mock_hotel_rows):
        """It returns the expected json given a list of OrderedDicts"""
        export = JsonExport(mock_hotel_rows)
        assert export.get_document() == '[\n    {\n        "address": "Stretto Bernardi 004, Quarto Mietta nell\'emilia, 07958 Torino (OG)",\n        "contact": "Rosalino Marchetti",\n        "name": "Martini Cattaneo",\n        "phone": "+39 627 68225719",\n        "stars": "5",\n        "uri": "http://www.farina.org/blog/categories/tags/about.html"\n    },\n    {\n        "address": "Bolzmannweg 451, 05116 Hannover",\n        "contact": "Scarlet Kusch-Linke",\n        "name": "Apartment Dörr",\n        "phone": "08177354570",\n        "stars": "1",\n        "uri": "http://www.garden.com/list/home.html"\n    }\n]'  # pylint: disable=line-too-long
