# https://github.com/hyperhype/hyperscript
# https://www.w3.org/TR/html52/syntax.html#writing-html-documents-elements
from collections.abc import Generator, Iterable, Mapping
from html import escape
from functools import partial


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
        self.attrs = {
            attr_aliases.get(key, key): value for key, value in attrs.items()
        }
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
                    str_value = ' '.join(value)
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
        super().__init__('doctype')

    def __str__(self):
        html = "<!DOCTYPE html>"
        for child in self.children:
            html += str(child)
        return html


a = partial(tag, "a")
abbr = partial(tag, "abbr")
address = partial(tag, "address")
area = partial(tag, "area")
article = partial(tag, "article")
aside = partial(tag, "aside")
audio = partial(tag, "audio")
b = partial(tag, "b")
base = partial(tag, "base")
bdi = partial(tag, "bdi")
bdo = partial(tag, "bdo")
blockquote = partial(tag, "blockquote")
body = partial(tag, "body")
br = partial(tag, "br")
button = partial(tag, "button")
canvas = partial(tag, "canvas")
caption = partial(tag, "caption")
cite = partial(tag, "cite")
code = partial(tag, "code")
col = partial(tag, "col")
colgroup = partial(tag, "colgroup")
data = partial(tag, "data")
datalist = partial(tag, "datalist")
dd = partial(tag, "dd")
del_ = partial(tag, "del")  # Python keyword
details = partial(tag, "details")
dfn = partial(tag, "dfn")
dialog = partial(tag, "dialog")
div = partial(tag, "div")
dl = partial(tag, "dl")
dt = partial(tag, "dt")
em = partial(tag, "em")
embed = partial(tag, "embed")
fieldset = partial(tag, "fieldset")
figcaption = partial(tag, "figcaption")
figure = partial(tag, "figure")
footer = partial(tag, "footer")
form = partial(tag, "form")
h1 = partial(tag, "h1")
h2 = partial(tag, "h2")
h3 = partial(tag, "h3")
h4 = partial(tag, "h4")
h5 = partial(tag, "h5")
h6 = partial(tag, "h6")
head = partial(tag, "head")
header = partial(tag, "header")
hr = partial(tag, "hr")
html = partial(tag, "html")
i = partial(tag, "i")
iframe = partial(tag, "iframe")
img = partial(tag, "img")
input_ = partial(tag, "input")  # Python builtin
ins = partial(tag, "ins")
kbd = partial(tag, "kbd")
label = partial(tag, "label")
legend = partial(tag, "legend")
li = partial(tag, "li")
link = partial(tag, "link")
main = partial(tag, "main")
map_ = partial(tag, "map")  # Python builtin
mark = partial(tag, "mark")
meta = partial(tag, "meta")
meter = partial(tag, "meter")
nav = partial(tag, "nav")
noscript = partial(tag, "noscript")
object_ = partial(tag, "object")  # Python builtin
ol = partial(tag, "ol")
optgroup = partial(tag, "optgroup")
option = partial(tag, "option")
output = partial(tag, "output")
p = partial(tag, "p")
param = partial(tag, "param")
picture = partial(tag, "picture")
pre = partial(tag, "pre")
progress = partial(tag, "progress")
q = partial(tag, "q")
rb = partial(tag, "rb")
rp = partial(tag, "rp")
rt = partial(tag, "rt")
rtc = partial(tag, "rtc")
ruby = partial(tag, "ruby")
s = partial(tag, "s")
samp = partial(tag, "samp")
script = partial(tag, "script")
section = partial(tag, "section")
select = partial(tag, "select")
small = partial(tag, "small")
source = partial(tag, "source")
span = partial(tag, "span")
strong = partial(tag, "strong")
style = partial(tag, "style")
sub = partial(tag, "sub")
summary = partial(tag, "summary")
sup = partial(tag, "sup")
table = partial(tag, "table")
tbody = partial(tag, "tbody")
td = partial(tag, "td")
template = partial(tag, "template")
textarea = partial(tag, "textarea")
tfoot = partial(tag, "tfoot")
th = partial(tag, "th")
thead = partial(tag, "thead")
time = partial(tag, "time")
title = partial(tag, "title")
tr = partial(tag, "tr")
track = partial(tag, "track")
u = partial(tag, "u")
ul = partial(tag, "ul")
var = partial(tag, "var")
video = partial(tag, "video")
wbr = partial(tag, "wbr")
