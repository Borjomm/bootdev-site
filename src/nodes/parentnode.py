from .htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str | None] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError(f"{self} didn't receive a tag")
        if self.children is None:
            raise ValueError(f"{self} is missing a list of children!")
        return f"<{self.tag}{self.props_to_html()}>{''.join(item.to_html() for item in self.children)}</{self.tag}>"
        
    def __repr__(self):
        return f"ParentNode(tag={self.tag!r}, children={self.children!r}, props={self.props!r})"