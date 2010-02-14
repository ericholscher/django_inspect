from distutils.core import setup

setup(
    name = "django_inspect",
    version = "0.1",
    packages = [
        "django_inspect",
        "django_inspect.tests",
    ],
    author = "Eric Holscher",
    author_email = "eric@ericholscher.com",
    description = "A stupidly simple Django model introspection API.",
    url = "http://github.com/ericholscher/django_inspect/tree/master",
)
