from ..nodes import TextNode, TextType, LeafNode, HTMLNode


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
        
