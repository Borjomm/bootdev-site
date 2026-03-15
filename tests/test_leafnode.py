import unittest

from src.nodes import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_tag(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "This is a raw text")
        self.assertEqual(node.to_html(), "This is a raw text")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "This is a link!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">This is a link!</a>')

    def test_leaf_to_html_no_value(self):
        node = LeafNode("b", None) # pyright: ignore[reportArgumentType]
        with self.assertRaises(ValueError):
            node.to_html()

    