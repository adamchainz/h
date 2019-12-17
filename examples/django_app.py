import os
import sys

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path
from django.utils.crypto import get_random_string

import h


def page(head_contents, body_contents):
    return h.doctype(h.html(h.head(*head_contents), h.body(*body_contents)))


def my_template(name, main_contents):
    return page(
        head_contents=[h.title(name)],
        body_contents=[h.header(h.h1(name)), h.main(*main_contents)],
    )


class HResponse(HttpResponse):
    def __init__(self, content, *args, **kwargs):
        super().__init__(content.to_html(), *args, **kwargs)


settings.configure(
    DEBUG=(os.environ.get("DEBUG", "") == "1"),
    ALLOWED_HOSTS=["*"],  # Disable host header validation
    ROOT_URLCONF=__name__,  # Make this module the urlconf
    SECRET_KEY=get_random_string(
        50
    ),  # We aren't using any security features but Django requires this setting
)


def index(request):
    name = request.GET.get("name", "World")
    return HResponse(
        my_template("Hello!", [h.p(style="color: red", children=["Hello ", name, "!"])])
    )


urlpatterns = [
    path("", index),
]

app = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
