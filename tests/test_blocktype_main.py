import unittest

from src.nodes import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_dispatch_heading(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_dispatch_code(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_dispatch_quote(self):
        block = "> quoted text"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_dispatch_unordered_list(self):
        block = "- item one\n- item two"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_dispatch_ordered_list(self):
        block = "1. item one\n2. item two"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_dispatch_paragraph(self):
        block = "Just a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_dispatch_empty_string_is_paragraph(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_dispatch_invalid_heading_is_paragraph(self):
        block = "####### too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_dispatch_invalid_ordered_list_is_paragraph(self):
        block = "1. first\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_dispatch_invalid_quote_is_paragraph(self):
        block = "> valid\nnot quoted"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestBlockToBlockTypePrecedence(unittest.TestCase):
    def test_code_fence_beats_other_inner_syntax(self):
        block = "```\n# not a heading\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_beats_list_inside_quote(self):
        block = "> - not an unordered list at top level"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_beats_ordered_list_inside_quote(self):
        block = "> 1. not an ordered list at top level"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)