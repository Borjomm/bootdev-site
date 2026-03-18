from enum import Enum, auto

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()

def _is_heading(block: str) -> BlockType | None:
    i = 0
    while i < len(block) and block[i] == "#":
        i += 1
    if not 1 <= i <= 6:
        return None
    if i >= len(block) or block[i] not in [" ", "\t"]:
        return None
    if block[i + 1:].strip() == "":
        return None
    return BlockType.HEADING

def _is_code(block: str) -> BlockType | None:
    return BlockType.CODE if block.startswith("```\n") and block.endswith("```") else None

def _is_quote(block: str) -> BlockType | None:
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            return None
        if not line[1:].strip():
            return None
    return BlockType.QUOTE

def _is_unordered_list(block: str) -> BlockType | None:
    lines = block.split("\n")
    for line in lines:
        if not line.startswith("- "):
            return None
    return BlockType.UNORDERED_LIST

def _is_ordered_list(block: str) -> BlockType | None:
    lines = block.split("\n")
    counter = 1
    for line in lines:
        if not line.startswith(f"{counter}. "):
            return None
        counter += 1
    return BlockType.ORDERED_LIST    

def block_to_block_type(block: str) -> BlockType:
    return (_is_heading(block) 
            or _is_code(block) 
            or _is_quote(block) 
            or _is_unordered_list(block) 
            or _is_ordered_list(block) 
            or BlockType.PARAGRAPH)