

class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str | None] | None = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self):
        return " " + ' '.join(f'{key}="{value}"' for key, value in self.props.items()) if self.props else ""
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"
    

if __name__ == "__main__":
    node = HTMLNode("p", "text", None, {"href": "https://www.google.com", "target": "_blank"})
    print(node)
    print(node.props_to_html())