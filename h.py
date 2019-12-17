# https://github.com/hyperhype/hyperscript
# https://www.w3.org/TR/html52/syntax.html#writing-html-documents-elements
from html import escape
from functools import partial

import pytest


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


class h:
    __slots__ = ("tag", "is_void", "children", "attrs")

    def __init__(self, tag, *children, **attrs):
        self.tag = tag
        self.is_void = tag in void_tags

        if self.is_void and children:
            raise ValueError(f"Tag {tag} may not have children")

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
        html = f"<{self.tag}"
        if self.attrs:
            html += " "
            html += " ".join(
                f'{k}="{escape(v, quote=True)}"' for k, v in self.attrs.items()
            )
        html += ">"
        if not self.is_void:
            html += "".join(child.to_html() for child in self.children)
            html += f"</{self.tag}>"
        return html

    # Jinja2 compatibility
    __html__ = to_html


html = partial(h, 'html')
head = partial(h, 'body')
h1 = partial(h, 'h1')
h2 = partial(h, 'h2')
p = partial(h, 'p')
b = partial(h, 'b')
i = partial(h, 'i')


def test_empty_tag():
    assert h("b").to_html() == "<b></b>"


def test_void_tag():
    assert h("hr").to_html() == "<hr>"


def test_void_tag_cant_have_children():
    with pytest.raises(ValueError):
        h("hr", "Hi")


def test_tag_with_text_child():
    assert h("b", "Hi").to_html() == "<b>Hi</b>"


def test_tag_with_integer_child():
    assert h("b", 1).to_html() == "<b>1</b>"


def test_multiple_children():
    assert h("ul",)


def test_tag_child_None_ignored():
    assert h("b", None).to_html() == "<b></b>"


def test_attribute():
    assert h("b", id="foo").to_html() == '<b id="foo"></b>'


def test_class_attribute():
    assert h("b", class_="foo").to_html() == '<b class="foo"></b>'


def test_id_attribute():
    assert h("b", id_="foo").to_html() == '<b id="foo"></b>'


def test_attribute_and_child():
    assert h("b", "Hi", id="foo").to_html() == '<b id="foo">Hi</b>'


def test_void_tag_attribute():
    assert h("hr", id="foo").to_html() == '<hr id="foo">'


def test_children_tuple():
    assert h("b", id="foo", children=("Hi",)).to_html() == '<b id="foo">Hi</b>'


def test_children_list():
    assert h("b", id="foo", children=["Hi"]).to_html() == '<b id="foo">Hi</b>'


def test_nested():
    assert h("b", h("i", "Hi")).to_html() == "<b><i>Hi</i></b>"


def test_doctype():
    assert doctype().to_html() == '<!DOCTYPE html>'


def test_doctype_child():
    assert doctype(h('html')).to_html() == '<!DOCTYPE html><html></html>'
