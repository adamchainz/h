import pytest

import h


def test_empty_tag():
    assert h.tag("b").to_html() == "<b></b>"


def test_void_tag():
    assert h.tag("hr").to_html() == "<hr>"


def test_void_tag_cant_have_children():
    with pytest.raises(ValueError):
        h.tag("hr", "Hi")


def test_tag_with_text_child():
    assert h.tag("b", "Hi").to_html() == "<b>Hi</b>"


def test_tag_with_integer_child():
    assert h.tag("b", 1).to_html() == "<b>1</b>"


def test_multiple_children():
    assert (
        h.tag("ul", h.tag("li", "Item 1"), h.tag("li", "Item 2")).to_html()
        == "<ul><li>Item 1</li><li>Item 2</li></ul>"
    )


def test_tag_child_None_ignored():
    assert h.tag("b", None).to_html() == "<b></b>"


def test_attribute():
    assert h.tag("b", id="foo").to_html() == '<b id="foo"></b>'


def test_attribute_empty_string():
    assert h.tag("a", href="").to_html() == '<a href=""></a>'


def test_attribute_true():
    assert h.tag("input", type="checkbox", checked=True).to_html() == '<input type="checkbox" checked>'


def test_attribute_false():
    assert h.tag("input", type="checkbox", checked=False).to_html() == '<input type="checkbox">'


def test_attribute_false_only():
    assert h.tag("input", disabled=False).to_html() == '<input>'


def test_class_attribute():
    assert h.tag("b", class_="foo").to_html() == '<b class="foo"></b>'


def test_id_attribute():
    assert h.tag("b", id_="foo").to_html() == '<b id="foo"></b>'


def test_attribute_and_child():
    assert h.tag("b", "Hi", id="foo").to_html() == '<b id="foo">Hi</b>'


def test_void_tag_attribute():
    assert h.tag("hr", id="foo").to_html() == '<hr id="foo">'


def test_children_tuple():
    assert h.tag("b", id="foo", children=("Hi",)).to_html() == '<b id="foo">Hi</b>'


def test_children_list():
    assert h.tag("b", id="foo", children=["Hi"]).to_html() == '<b id="foo">Hi</b>'


def test_nested():
    assert h.tag("b", h.i("Hi")).to_html() == "<b><i>Hi</i></b>"


def test_doctype():
    assert h.doctype().to_html() == "<!DOCTYPE html>"


def test_doctype_child():
    assert h.doctype(h.html()).to_html() == "<!DOCTYPE html><html></html>"
