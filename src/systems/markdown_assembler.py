from ..nodes import HTMLNode, ParentNode, LeafNode, block_to_block_type, BlockType, TextNode, TextType
from .converter import markdown_to_blocks, text_node_to_html_node, text_to_textnodes

def _text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]



def _make_heading_node(block: str) -> HTMLNode:
    i = 0
    while i < len(block) and block[i] == "#":
        i += 1
    text = block[i+1:]
    return ParentNode(tag=f"h{i}", children=_text_to_children(text))

def _make_code_node(block: str) -> HTMLNode:
    text = block[4:-3]
    node = TextNode(text, TextType.CODE)
    return ParentNode(tag="pre", children=[text_node_to_html_node(node)])

def _make_quote_node(block: str) -> HTMLNode:
    html_nodes = []
    lines = block.split('\n')
    for i, line in enumerate(lines):
        start = 2 if line[1] == " " else 1
        html_nodes.extend(_text_to_children(line[start:]))
        if i != len(lines) - 1:
            html_nodes.append(LeafNode(tag=None, value='\n'))
    return ParentNode(tag="blockquote", children=[ParentNode(tag='p', children=html_nodes)])

def _make_unordered_list(block: str) -> HTMLNode:
    entries = []
    lines = block.split('\n')
    for line in lines:
        nodes = _text_to_children(line[2:])
        entries.append(ParentNode(tag="li", children=nodes))
    return ParentNode(tag="ul", children=entries)

def _make_ordered_list(block: str) -> HTMLNode:
    entries = []
    lines = block.split('\n')
    for line in lines:
        start = line.index(" ")
        nodes = _text_to_children(line[start + 1:])
        entries.append(ParentNode(tag="li", children=nodes))
    return ParentNode(tag="ol", children=entries)

def _make_paragraph(block: str) -> HTMLNode:
    text = " ".join(line.strip() for line in block.split("\n"))
    return ParentNode(tag="p", children=_text_to_children(text))
    


def markdown_to_html_node(markdown: str) -> HTMLNode:
    children: list[HTMLNode] = []

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                node = _make_heading_node(block)
            case BlockType.CODE:
                node = _make_code_node(block)
            case BlockType.QUOTE:
                node = _make_quote_node(block)
            case BlockType.UNORDERED_LIST:
                node = _make_unordered_list(block)
            case BlockType.ORDERED_LIST:
                node = _make_ordered_list(block)
            case BlockType.PARAGRAPH:
                node = _make_paragraph(block)
            case _:
                raise ValueError(f"Unsupported block type: {block_type}")
        children.append(node)
    return ParentNode(tag="div", children=children)
