from .builder import build_public, generate_pages_recursive
import os

MD_PATH = "content"
HTML_TEMPLATE_PATH = "template.html"
BUILD_PATH = "public"


def main():
    build_public()
    generate_pages_recursive(MD_PATH, HTML_TEMPLATE_PATH, BUILD_PATH)


if __name__ == "__main__":
    main()