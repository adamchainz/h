from collections import OrderedDict

import pytest

import h


def test_empty_tag():
    assert str(h.tag("b")) == "<b></b>"


def test_void_tag():
    assert str(h.tag("hr")) == "<hr>"


def test_tag_with_children_cant_have_reassigned():
    with pytest.raises(ValueError) as excinfo:
        h.tag("b")["Hi"]["Hi again"]
    assert "Cannot reassign children" in str(excinfo.value)


def test_void_tag_cant_have_children():
    with pytest.raises(ValueError) as excinfo:
        h.tag("hr")["Hi"]
    assert "Void tag <hr> cannot have children" in str(excinfo.value)


def test_shortcut_tag():
    assert str(h.b()) == "<b></b>"


def test_shortcut_void_tag():
    assert str(h.hr()) == "<hr>"


def test_shortcut_tag_del():
    assert str(h.del_()) == "<del></del>"


def test_shortcut_tag_input():
    assert str(h.input_()) == "<input>"


def test_shortcut_tag_map():
    assert str(h.map_()) == "<map></map>"


def test_shortcut_tag_object():
    assert str(h.object_()) == "<object></object>"


def test_tag_with_text_child():
    assert str(h.tag("b")["Hi"]) == "<b>Hi</b>"


def test_tag_with_integer_child():
    assert str(h.tag("b")[1]) == "<b>1</b>"


def test_multiple_children():
    assert (
        str(h.ul()[h.li()["Item 1"], h.li()["Item 2"]])
        == "<ul><li>Item 1</li><li>Item 2</li></ul>"
    )


def test_tag_child_None_ignored():
    assert str(h.b()[None]) == "<b></b>"


def test_tag_class_child_direct():
    assert str(h.b["Hi"]) == "<b>Hi</b>"


def test_attribute():
    assert str(h.a(href="https://example.com")) == '<a href="https://example.com"></a>'


def test_attribute_id():
    assert str(h.h1(id="myheading")) == '<h1 id="myheading"></h1>'


def test_attribute_class():
    assert str(h.b(class_="mybold")) == '<b class="mybold"></b>'


def test_attribute_list():
    assert str(h.b(class_=["foo", "bar"])) == '<b class="foo bar"></b>'


def test_attribute_empty_string():
    assert str(h.a(href="")) == '<a href=""></a>'


def test_attribute_bool_true():
    assert (
        str(h.input_(type="checkbox", checked=True))
        == '<input type="checkbox" checked>'
    )


def test_attribute_bool_false():
    assert str(h.input_(type="checkbox", checked=False)) == '<input type="checkbox">'


def test_attribute_bool_false_solo():
    assert str(h.input_(disabled=False)) == "<input>"


def test_attribute_style_dict():
    assert str(h.b(style={"color": "red"})) == '<b style="color: red"></b>'


def test_attribute_style_ordered_dict():
    assert (
        str(h.b(style=OrderedDict([("color", "red"), ("font-weight", "bold")])))
        == '<b style="color: red; font-weight: bold"></b>'
    )


def test_attribute_and_child():
    assert str(h.b(id="foo")["Hi"]) == '<b id="foo">Hi</b>'


def test_void_tag_attribute():
    assert str(h.hr(id="foo")) == '<hr id="foo">'


def test_nested():
    assert str(h.b()[h.i()["Hi"]]) == "<b><i>Hi</i></b>"


def test_doctype():
    assert str(h.doctype()) == "<!DOCTYPE html>"


def test_doctype_child():
    assert str(h.doctype()[h.html()]) == "<!DOCTYPE html><html></html>"


def test_text():
    assert (
        str(h.text("<script>alert(1)</script>"))
        == "&lt;script&gt;alert(1)&lt;/script&gt;"
    )


def test_unsafe_raw_text():
    assert (
        str(h.unsafe_raw_text("<script>alert(1)</script>"))
        == "<script>alert(1)</script>"
    )


def test_comment():
    assert (
        str(h.comment("<script>alert(1)</script>"))
        == "<!--&lt;script&gt;alert(1)&lt;/script&gt;-->"
    )
