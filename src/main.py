from .builder import build_public, generate_pages_recursive, BUILD_PATH
import sys

MD_PATH = "content"
HTML_TEMPLATE_PATH = "template.html"


def main():
    build_public()
    basename = sys.argv[1] if len(sys.argv) > 1 else "/"
    generate_pages_recursive(MD_PATH, HTML_TEMPLATE_PATH, BUILD_PATH, basename)


if __name__ == "__main__":
    main()