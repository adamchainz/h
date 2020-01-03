# https://github.com/hyperhype/hyperscript
# https://www.w3.org/TR/html52/syntax.html#writing-html-documents-elements
from collections.abc import Generator, Iterable, Mapping
from html import escape


class html_item:
    pass


class text(html_item):
    __slots__ = ("_item",)

    def __init__(self, item):
        self._item = item

    def __str__(self):
        return escape(str(self._item))


class unsafe_raw_text(html_item):
    __slots__ = ("_item",)

    def __init__(self, item):
        self._item = item

    def __str__(self):
        return str(self._item)


class comment(html_item):
    __slots__ = ("_contents",)

    def __init__(self, contents):
        self._contents = contents

    def __str__(self):
        return f"<!--{escape(str(self._contents))}-->"


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


class tag(html_item):
    __slots__ = ("_tag", "is_void", "children", "attrs")

    def __init__(self, _tag, **attrs):
        self._tag = _tag
        self.is_void = _tag in void_tags
        attr_aliases = {"class_": "class", "id_": "id"}
        self.attrs = {attr_aliases.get(key, key): value for key, value in attrs.items()}
        self.children = ()

    def __getitem__(self, key):
        if self.children:
            raise ValueError("Cannot reassign children")
        elif self.is_void:
            raise ValueError(f"Void tag <{self._tag}> cannot have children")

        if isinstance(key, (Generator, Iterable)) and not isinstance(key, str):
            children = key
        else:
            children = [key]

        self.children = []
        for child in children:
            if isinstance(child, html_item):
                self.children.append(child)
            elif child is None:
                # Allow None to make inline ifs easy
                pass
            else:
                # Anything else we'll try to render as text
                self.children.append(text(child))

        return self

    @classmethod
    def __class_getitem__(cls, key):
        return cls()[key]

    def __str__(self):
        html = f"<{self._tag}"
        if self.attrs:
            for key, value in self.attrs.items():
                if value is False:
                    continue
                html += " "
                norm_key = {"class_": "class"}.get(key, key)
                html += norm_key

                if key == "style" and isinstance(value, Mapping):
                    str_value = "; ".join(
                        f"{css_key}: {css_value}"
                        for css_key, css_value in value.items()
                    )
                elif isinstance(value, (tuple, list)):
                    str_value = " ".join(value)
                else:
                    str_value = str(value)

                if value is not True:
                    html += '="' + escape(str_value, quote=True) + '"'
        html += ">"
        if not self.is_void:
            for child in self.children:
                html += str(child)
            html += f"</{self._tag}>"
        return html


class doctype(tag):
    def __init__(self):
        super().__init__("doctype")

    def __str__(self):
        html = "<!DOCTYPE html>"
        for child in self.children:
            html += str(child)
        return html


def tag_class(_tag):
    def __init__(self, **attrs):
        tag.__init__(self, _tag, **attrs)

    return type(_tag, (tag,), {"__init__": __init__})


a = tag_class("a")
abbr = tag_class("abbr")
address = tag_class("address")
area = tag_class("area")
article = tag_class("article")
aside = tag_class("aside")
audio = tag_class("audio")
b = tag_class("b")
base = tag_class("base")
bdi = tag_class("bdi")
bdo = tag_class("bdo")
blockquote = tag_class("blockquote")
body = tag_class("body")
br = tag_class("br")
button = tag_class("button")
canvas = tag_class("canvas")
caption = tag_class("caption")
cite = tag_class("cite")
code = tag_class("code")
col = tag_class("col")
colgroup = tag_class("colgroup")
data = tag_class("data")
datalist = tag_class("datalist")
dd = tag_class("dd")
del_ = tag_class("del")  # Python keyword
details = tag_class("details")
dfn = tag_class("dfn")
dialog = tag_class("dialog")
div = tag_class("div")
dl = tag_class("dl")
dt = tag_class("dt")
em = tag_class("em")
embed = tag_class("embed")
fieldset = tag_class("fieldset")
figcaption = tag_class("figcaption")
figure = tag_class("figure")
footer = tag_class("footer")
form = tag_class("form")
h1 = tag_class("h1")
h2 = tag_class("h2")
h3 = tag_class("h3")
h4 = tag_class("h4")
h5 = tag_class("h5")
h6 = tag_class("h6")
head = tag_class("head")
header = tag_class("header")
hr = tag_class("hr")
html = tag_class("html")
i = tag_class("i")
iframe = tag_class("iframe")
img = tag_class("img")
input_ = tag_class("input")  # Python builtin
ins = tag_class("ins")
kbd = tag_class("kbd")
label = tag_class("label")
legend = tag_class("legend")
li = tag_class("li")
link = tag_class("link")
main = tag_class("main")
map_ = tag_class("map")  # Python builtin
mark = tag_class("mark")
meta = tag_class("meta")
meter = tag_class("meter")
nav = tag_class("nav")
noscript = tag_class("noscript")
object_ = tag_class("object")  # Python builtin
ol = tag_class("ol")
optgroup = tag_class("optgroup")
option = tag_class("option")
output = tag_class("output")
p = tag_class("p")
param = tag_class("param")
picture = tag_class("picture")
pre = tag_class("pre")
progress = tag_class("progress")
q = tag_class("q")
rb = tag_class("rb")
rp = tag_class("rp")
rt = tag_class("rt")
rtc = tag_class("rtc")
ruby = tag_class("ruby")
s = tag_class("s")
samp = tag_class("samp")
script = tag_class("script")
section = tag_class("section")
select = tag_class("select")
small = tag_class("small")
source = tag_class("source")
span = tag_class("span")
strong = tag_class("strong")
style = tag_class("style")
sub = tag_class("sub")
summary = tag_class("summary")
sup = tag_class("sup")
table = tag_class("table")
tbody = tag_class("tbody")
td = tag_class("td")
template = tag_class("template")
textarea = tag_class("textarea")
tfoot = tag_class("tfoot")
th = tag_class("th")
thead = tag_class("thead")
time = tag_class("time")
title = tag_class("title")
tr = tag_class("tr")
track = tag_class("track")
u = tag_class("u")
ul = tag_class("ul")
var = tag_class("var")
video = tag_class("video")
wbr = tag_class("wbr")
