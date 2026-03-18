import unittest

from src.systems.markdown_parser import _split_nodes_delimiter
from src.nodes import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold_single(self):
        nodes = [
            TextNode("This is text with a **bold** word", TextType.TEXT)
        ]
        new_nodes = _split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT)
            ]
            )
        
    def test_bold_multiple(self):
        nodes = [
            TextNode("This is a **text **with **multiple** **bold** words", TextType.TEXT)
        ]
        new_nodes = _split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("text ", TextType.BOLD),
                TextNode("with ", TextType.TEXT),
                TextNode("multiple", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" words", TextType.TEXT)
            ]
        )

    def test_invalid_markdown(self):
        nodes = [
            TextNode("This is a _text_ with _invalid markdown", TextType.TEXT)
        ]
        with self.assertRaises(ValueError):
            _split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    def test_italic_and_empty_markdown(self):
        nodes = [
            TextNode("_This_ is an _italic text_ with __some empty markdown", TextType.TEXT)
        ]
        new_nodes = _split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This", TextType.ITALIC),
                TextNode(" is an ", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
                TextNode(" with ", TextType.TEXT),
                TextNode("some empty markdown", TextType.TEXT)
            ]
        )

    def test_code_and_multiple(self):
        nodes = [
            TextNode("This has a `code block`, ", TextType.TEXT),
            TextNode("this is already parsed", TextType.BOLD),
            TextNode(" and this is another `code block`", TextType.TEXT)
        ]
        new_nodes = _split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This has a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(", ", TextType.TEXT),
                TextNode("this is already parsed", TextType.BOLD),
                TextNode(" and this is another ", TextType.TEXT),
                TextNode("code block", TextType.CODE)
            ]
        )