import unittest

from src.nodes.blocks import BlockType, _is_heading, _is_quote, _is_code, _is_unordered_list, _is_ordered_list

class TestBlockTypeHeading(unittest.TestCase):
    def test_is_heading_h1(self):
        block = "# Text"
        block_type = _is_heading(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_is_heading_h6(self):
        block = "###### Text"
        block_type = _is_heading(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_is_heading_h7(self):
        block = "####### Text"
        block_type = _is_heading(block)
        self.assertEqual(block_type, None)

    def test_is_heading_plain_text(self):
        block = "Text"
        block_type = _is_heading(block)
        self.assertEqual(block_type, None)

    def test_is_heading_no_whitespace(self):
        block = "###Text"
        block_type = _is_heading(block)
        self.assertEqual(block_type, None)

    def test_is_heading_no_text(self):
        block = "### \t\t    "
        block_type = _is_heading(block)
        self.assertEqual(block_type, None)

    def test_is_heading_tab_after_hashes(self):
        block = "##\tText"
        block_type = _is_heading(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_is_heading_empty_string(self):
        block = ""
        block_type = _is_heading(block)
        self.assertEqual(block_type, None)

    def test_is_heading_only_hashes(self):
        block = "###"
        block_type = _is_heading(block)
        self.assertEqual(block_type, None)

    def test_is_heading_hash_space_hash(self):
        block = "# #"
        block_type = _is_heading(block)
        self.assertEqual(block_type, BlockType.HEADING)

class TestBlockTypeQuote(unittest.TestCase):
    def test_is_quote_single_line(self):
        self.assertEqual(_is_quote("> Text"), BlockType.QUOTE)

    def test_is_quote_multi_line(self):
        self.assertEqual(_is_quote("> Text\n> More"), BlockType.QUOTE)

    def test_is_quote_missing_marker(self):
        self.assertEqual(_is_quote("> Text\nMore"), None)

    def test_is_quote_empty_after_marker(self):
        self.assertEqual(_is_quote("> "), BlockType.QUOTE)

class TestBlockTypeCode(unittest.TestCase):
    def test_is_code_valid(self):
        self.assertEqual(_is_code("```\ncodecodecode```"), BlockType.CODE)

    def test_is_code_invalid_brackets_first(self):
        self.assertEqual(_is_code("``\ncodecodecode```"), None)

    def test_is_code_invalid_brackets_last(self):
        self.assertEqual(_is_code("```\ncodecodecode``"), None)

    def test_is_code_no_newline(self):
        self.assertEqual(_is_code("```codecodecode```"), None)

class TestBlockTypeUnorderedList(unittest.TestCase):
    def test_is_unordered_list_valid_single(self):
        self.assertEqual(_is_unordered_list("- something"), BlockType.UNORDERED_LIST)

    def test_is_unordered_list_valid_multiple(self):
        self.assertEqual(_is_unordered_list("- something\n- anything\n- nothing"), BlockType.UNORDERED_LIST)

    def test_is_unordered_list_single_whitespace_first(self):
        self.assertEqual(_is_unordered_list(" - something"), None)

    def test_is_unordered_list_multiple_no_whitespace(self):
        self.assertEqual(_is_unordered_list("- something\n- anything\n-nothing"), None)

    def test_is_unordered_list_multiple_no_dash(self):
        self.assertEqual(_is_unordered_list("- something\n anything"), None)

class TestBlockTypeOrderedList(unittest.TestCase):
    def test_is_ordered_list_valid_single(self):
        self.assertEqual(_is_ordered_list("1. first"), BlockType.ORDERED_LIST)

    def test_is_ordered_list_valid_multiple(self):
        self.assertEqual(_is_ordered_list("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)

    def test_is_ordered_list_repeating_number(self):
        self.assertEqual(_is_ordered_list("1. first\n2. second\n1. first"), None)

    def test_is_ordered_list_skipped_number(self):
        self.assertEqual(_is_ordered_list("1. first\n3. third\n4. forth"), None)

    def test_is_ordered_list_no_dot(self):
        self.assertEqual(_is_ordered_list("1 first\n2. second"), None)

    def test_is_ordered_list_no_space(self):
        self.assertEqual(_is_ordered_list("1. first\n2.second"), None)
    


    
