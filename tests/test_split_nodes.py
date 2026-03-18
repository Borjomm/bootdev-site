import unittest

from src.systems.markdown_parser import split_nodes_image, split_nodes_link
from src.nodes import TextNode, TextType

class TestSplitNodesImageOrLink(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_mixed_with_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
            ],
            new_nodes
        )

    def test_malformed_image(self):
        node = TextNode("This is text with an ![image](https://i.i(mgur.co(m))/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.i(mgur.co(m))/zjjcJKZ.png)", TextType.TEXT)
            ],
            new_nodes
        )