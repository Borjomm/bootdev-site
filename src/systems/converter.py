from ..nodes import TextNode, TextType, LeafNode, HTMLNode
from .markdown_parser import split_nodes_image, split_nodes_link, split_nodes_code, split_nodes_bold, split_nodes_italic


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    text = text_node.text
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError(f"Error converting {text_node}: link TextNode must have a url")
            return LeafNode(tag="a", value=text, props={"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError(f"Error converting {text_node}: img TextNode must have a url")
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text}, void=True)
        case _:
            raise ValueError(f"Unsupported text type: {text_node.text_type}")
        
def text_to_textnodes(text: str) -> list[TextNode]:
    temp1 = split_nodes_link([TextNode(text, TextType.TEXT)])
    temp2 = split_nodes_image(temp1)
    temp3 = split_nodes_code(temp2)
    temp4 = split_nodes_bold(temp3)
    temp5 = split_nodes_italic(temp4)
    final = temp5
    return final
        
def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]
