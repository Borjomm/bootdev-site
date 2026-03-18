import unittest

from src.systems.markdown_parser import _extract_markdown_links, _extract_markdown_images

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_links_single(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = _extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev")])

    def test_extract_markdown_links_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = _extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_links_mixed_with_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)"
        matches = _extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev")])

    def test_extract_markdown_links_malformed_text(self):
        text = "This is text with a link [to [boot] dev](https://www.boot.dev)"
        matches = _extract_markdown_links(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_links_malformed_url(self):
        text = "This is text with a link [to boot dev](https://ww(w.boo)t.dev)"
        matches = _extract_markdown_links(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_images_single(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = _extract_markdown_images(text)
        self.assertEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_images_multiple(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another image](https://i.imgur.com/zasdaf123.jpg)"
        matches = _extract_markdown_images(text)
        self.assertEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png"), ("another image", "https://i.imgur.com/zasdaf123.jpg")])

    def test_extract_markdown_images_mixed_with_links(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)"
        matches = _extract_markdown_images(text)
        self.assertEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_images_malformed_text(self):
        text = "This is text with an ![i[ma]ge](https://i.imgur.com/zjjcJKZ.png)"
        matches = _extract_markdown_images(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_images_malformed_url(self):
        text = "This is text with an ![image](https://i.i(mgur.co(m))/zjjcJKZ.png)"
        matches = _extract_markdown_images(text)
        self.assertEqual(matches, [])

    
