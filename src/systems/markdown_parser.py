import re

from ..nodes import TextNode, TextType

def _extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def _extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def _split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        split_sections = node.text.split(delimiter)
        if len(split_sections) % 2 == 0:
            raise ValueError(f"Received node {node} with an invalid syntax for '{delimiter}' delimiter")
        result.extend(TextNode(text=part, text_type=TextType.TEXT if i % 2 == 0 else text_type) for i, part in enumerate(split_sections) if part)
    return result

def _split_nodes_inner(old_nodes: list[TextNode], split_type: TextType) -> list[TextNode]:
    if split_type not in [TextType.LINK, TextType.IMAGE]:
        raise ValueError(f"Inner split_nodes function got invalid split type: {split_type}")
    result = []
    prefix = "!" if split_type == TextType.IMAGE else "" 
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        if split_type == TextType.IMAGE:
            objects = _extract_markdown_images(node.text)
        else:
            objects = _extract_markdown_links(node.text)
        if not objects:
            result.append(node)
            continue
        temp_str = node.text
        for alt_text, link in objects:
            temp_list = temp_str.split(f"{prefix}[{alt_text}]({link})", maxsplit=1)
            if temp_list[0]:
                result.append(TextNode(text=temp_list[0], text_type=TextType.TEXT))
            result.append(TextNode(text=alt_text, text_type=split_type, url=link))
            temp_str = temp_list[1]
        if temp_str:
            result.append(TextNode(text=temp_str, text_type=TextType.TEXT))
    return result

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_inner(old_nodes, TextType.LINK)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_inner(old_nodes, TextType.IMAGE)

def split_nodes_bold(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

def split_nodes_italic(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

def split_nodes_code(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_delimiter(old_nodes, "`", TextType.CODE)




        