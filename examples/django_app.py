"""
pip install -e ..
pip install django
DEBUG=1 python django_app.py runserver
"""
import os
import sys

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path
from django.utils.crypto import get_random_string

import h

# h helpers


def bootstrap_jumbotron(*, class_=None, **kwargs):
    if class_ is None:
        class_ = []
    class_.append("jumbotron")
    return h.div(class_=class_, **kwargs)


def bootstrap_table(hover=True, striped=True, bordered=True):
    class_ = ["table"]
    if hover:
        class_.append("table-hover")
    if striped:
        class_.append("table-striped")
    if bordered:
        class_.append("table-bordered")
    return h.table(class_=class_)


def template_base(*, name, main_contents):
    return h.doctype()[
        h.html(lang="en")[
            h.head()[
                h.comment("Required meta tags"),
                h.meta(charset="utf-8"),
                h.meta(
                    name="viewport",
                    content="width=device-width, initial-scale=1, shrink-to-fit=no",
                ),
                h.comment("Bootstrap CSS"),
                h.link(
                    rel="stylesheet",
                    href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
                    integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh",
                    crossorigin="anonymous",
                ),
                h.title()[name],
            ],
            h.body()[
                bootstrap_jumbotron()[h.header()[h.h1()[name], h.main()[main_contents]]]
            ],
        ]
    ]


def template_table_page(*, title: str, table: dict):
    return template_base(
        name=title,
        main_contents=[
            bootstrap_table()[
                h.thead()[h.tr()[h.th()["Key"], h.th()["Value"]]],
                h.tbody()[
                    (
                        h.tr()[h.td()[key], h.td()[h.pre()[value]]]
                        for key, value in table.items()
                    )
                ],
            ],
        ],
    )


settings.configure(
    DEBUG=(os.environ.get("DEBUG", "") == "1"),
    ALLOWED_HOSTS=["*"],  # Disable host header validation
    ROOT_URLCONF=__name__,  # Make this module the urlconf
    SECRET_KEY=get_random_string(
        50
    ),  # We aren't using any security features but Django requires this setting
)


def index(request):
    def link_with_url(urlname):
        return h.a(href=urlname)[urlname]

    links = {
        "Python Information": link_with_url("/pyinfo/"),
    }
    return HttpResponse(template_table_page(title="🏡 Home", table=links))


def pyinfo(request):
    system_data = {
        "Byte Order": sys.byteorder,
        "C API Version": sys.api_version,
        "Copyright": sys.copyright,
        "Executable": sys.executable,
        "Implementation Name": sys.implementation.name,
        "Platform": sys.platform,
        "Prefix": sys.prefix,
        "Recursion Limit": f"{sys.getrecursionlimit()} frames",
        "Thread Switch Interval": f"{sys.getswitchinterval()} seconds",
        "Version": sys.version,
    }
    return HttpResponse(
        template_table_page(title="🔍 Python Information", table=system_data)
    )


urlpatterns = [
    path("", index),
    path("pyinfo/", pyinfo),
]

app = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
