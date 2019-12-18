"""
pip install -e ..
pip install django
DEBUG=1 python django_app.py runserver
"""
import os
import random
import sys

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path
from django.utils.crypto import get_random_string

import h

# h helpers


def bootstrap_jumbotron(*args, class_=None, **kwargs):
    if class_ is None:
        class_ = []
    class_.append("jumbotron")
    return h.div(*args, class_=class_, **kwargs)


def my_template(name, main_contents):
    return h.html_page(
        head_contents=[
            h.title(name),
            h.meta(charset="utf-8"),
            h.meta(
                name="viewport",
                content="width=device-width, initial-scale=1, shrink-to-fit=no",
            ),
            h.link(
                rel="stylesheet",
                href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
                integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh",
                crossorigin="anonymous",
            ),
        ],
        body_contents=[
            bootstrap_jumbotron(h.header(h.h1(name)), h.main(*main_contents),),
        ],
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
        my_template(
            name=f"Hello {name}!",
            main_contents=[
                h.p(style="color: red", children=["Hello ", name, "!"]),
                h.img(
                    src=f"https://placekitten.com/{random.randint(200, 500)}/400",
                    class_=["img-thumbnail", "rounded", "mx-auto", "d-block"],
                ),
            ],
        )
    )


urlpatterns = [
    path("", index),
]

app = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
