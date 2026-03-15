from .htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str | None] | None = None, void: bool = False):
        super().__init__(tag, value, None, props)
        self.void = void

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError(f"{self} didn't receive any value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}{f'</{self.tag}>' if not self.void else ''}"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"