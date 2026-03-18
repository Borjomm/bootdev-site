from .builder import build_public, generate_pages_recursive
import sys

MD_PATH = "content"
HTML_TEMPLATE_PATH = "template.html"
BUILD_PATH = "docs"


def main():
    build_public()
    basename = sys.argv[0] if sys.argv else "/"
    generate_pages_recursive(MD_PATH, HTML_TEMPLATE_PATH, BUILD_PATH, basename)


if __name__ == "__main__":
    main()