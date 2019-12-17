# https://github.com/hyperhype/hyperscript
# https://www.w3.org/TR/html52/syntax.html#writing-html-documents-elements
from html import escape
from functools import partial


class doctype:
    def __init__(self, *children):
        self.children = children

    def to_html(self):
        return "<!DOCTYPE html>" + "".join(child.to_html() for child in self.children)


class text:
    __slots__ = ("_item",)

    def __init__(self, item):
        self._item = item

    def to_html(self):
        return escape(str(self._item))


void_tags = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


class tag:
    __slots__ = ("name", "is_void", "children", "attrs")

    def __init__(self, name, *children, **attrs):
        self.name = name
        self.is_void = name in void_tags

        if self.is_void and children:
            raise ValueError(f"Tag {self.name} may not have children")

        self.children = []
        children += tuple(attrs.pop("children", ()))
        for child in children:
            if hasattr(child, "to_html"):
                self.children.append(child)
            elif child is None:
                # Allow None to make inline ifs easy
                pass
            else:
                # Anything else we'll try to render as text
                self.children.append(text(child))

        key_replacements = {"class_": "class", "id_": "id"}
        self.attrs = {
            key_replacements.get(key, key): value for key, value in attrs.items()
        }

    def to_html(self):
        html = f"<{self.name}"
        if self.attrs:
            for key, value in self.attrs.items():
                if not value:
                    continue
                html += " "
                html += key
                if value is not True:
                    html += '="' + escape(value, quote=True) + '"'
        html += ">"
        if not self.is_void:
            html += "".join(child.to_html() for child in self.children)
            html += f"</{self.name}>"
        return html

    # Jinja2 compatibility
    __html__ = to_html


b = partial(tag, "b")
body = partial(tag, "body")
h1 = partial(tag, "h1")
h2 = partial(tag, "h2")
head = partial(tag, "body")
header = partial(tag, "header")
html = partial(tag, "html")
i = partial(tag, "i")
main = partial(tag, "main")
p = partial(tag, "p")
title = partial(tag, "title")
