from pathlib import Path
from typing import Optional, Union

from tini_test.coverage.consts import STYLE_FILE
from tini_test.coverage.enums import HTMLNodeType
from tini_test.misc.annotations import HTML, HTMLContent


class HTMLClass: # XXX FIX

    def __init__(self, _class: dict[str, str] | None) -> None:
        self._class = _class

    def to_html(self) -> HTMLContent:
        match self._class:

            case None:
                return ''
            
            case _:
                return ' '.join(
                    '%s="%s"' % (key, value)
                    for key, value in self._class.items()
                )


class HTMLNode:

    def __init__(self, 
                 _type: HTMLNodeType,
                 classes: Optional[dict[str, str] | list[dict[str, str]]] = None,
                 content: Optional[HTMLContent] = None,
                 children: Optional[Union['HTMLNode', list['HTMLNode']]] = None) -> None:
        
        self._type = _type

        if classes is None:
            self.classes = []
        elif isinstance(classes, dict):
            self.classes = [classes]
        else:
            self.classes = classes

        self.content = content or ''

        if children is None:
            self.children = []
        elif isinstance(children, HTMLNode):
            self.children = [children]
        else:
            self.children = children

    def add_class(self, classes: dict[str, str] | list[dict[str, str]]) -> None:
        if isinstance(classes, list):
            self.classes.extend(classes)
        else:
            self.classes.append(classes)

    def set_content(self, content: HTMLContent) -> None:
        self.content = content

    def add_children(self, children: Union['HTMLNode', list['HTMLNode']]) -> None:
        if isinstance(children, list):
            self.children.extend(children)
        else:
            self.children.append(children)

    def to_html(self) -> HTMLContent:
        class_content = ' '.join(map(lambda x: x.to_html(), map(HTMLClass, self.classes))) # XXX FIX
        children_html = '\n'.join(child.to_html() for child in self.children)
        content = '%s%s' % (self.content, children_html)
        return self._type.value % (class_content, content)

    
class HTMLHyperLink:

    def __init__(self, href: str, text: str) -> None:
        self.href = href
        self.text = text

    def to_html(self) -> HTMLContent:
        node = HTMLNode(HTMLNodeType.HREF)
        node.add_class({'href': self.href})
        node.set_content(self.text)
        return node.to_html()


class HTMLTemplate:

    def __init__(self, 
                 file_path: Path, 
                 content: HTMLContent, 
                 style_link: Optional[str] = None) -> None:
        
        self.file_path = file_path
        self.content = content
        self.style_link = style_link or STYLE_FILE

    def get_head(self) -> HTMLContent:
        node = HTMLNode(HTMLNodeType.LINK)
        node.add_class({'rel': 'stylesheet', 'href': self.style_link })
        return node.to_html()

    def get_body(self) -> HTMLContent:
        return self.content

    def to_html(self) -> HTML:
        return (HTMLNodeType.ROOT.value
                    %
                    (
                        '\n'.join([
                            HTMLNodeType.HEAD.value % (self.get_head(), ),
                            HTMLNodeType.BODY.value % (self.get_body(), ),
                        ])
                    )
               )

    def write_to_file(self) -> None:
        with open(self.file_path, 'w') as f:
            f.write(self.to_html())
