import xml.etree.ElementTree as XmlTree
from typing import List, Optional

NAMESPACES = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "xy": "http://www.x-and-y.ai/schema/bpmn/xy",
    "dmn": "https://www.omg.org/spec/DMN/20191111/MODEL/"
}


class XMLElement:

    def __init__(self, element: XmlTree.Element):
        self.element = element

    def get_tags(self, tag: str) -> List['XMLElement']:
        elements = self.element.findall(tag, NAMESPACES)
        return list(map(lambda x: XMLElement(x), elements))

    def has_tag(self, tag: str) -> bool:
        return self.get_tag(tag) is not None

    def get_tag(self, tag: str) -> Optional['XMLElement']:
        elements = self.element.findall(tag, NAMESPACES)
        if len(elements) == 0:
            return None
        return next(map(lambda x: XMLElement(x), elements))

    def get_attributes(self):
        return {x[0]: x[1] for x in self.element.items()}

    def get_attribute(self, name: str) -> Optional[str]:
        attributes = self.get_attributes()

        if ":" in name:
            array = name.split(":")
            namespace = NAMESPACES[array[0]]
            key = "{" + namespace + "}" + array[1]
            return attributes[key] if key in attributes else None

        return attributes[name] if name in attributes else None

    def get_text(self, unescape: bool = False):
        if unescape:
            import xml.sax.saxutils as sax
            return sax.unescape(self.element.text.strip())
        return self.element.text.strip()

    def __getitem__(self, item):
        return self.get_attribute(item)