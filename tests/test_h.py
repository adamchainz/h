import pytest

from h import doctype, h


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
    assert doctype().to_html() == "<!DOCTYPE html>"


def test_doctype_child():
    assert doctype(h("html")).to_html() == "<!DOCTYPE html><html></html>"
