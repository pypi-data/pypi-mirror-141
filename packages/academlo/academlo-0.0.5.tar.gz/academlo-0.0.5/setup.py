# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['academlo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'academlo',
    'version': '0.0.5',
    'description': '',
    'long_description': '# Academlo: Python Web Framework built for learning purposes\nAcademlo is a Python web framework built for learning purposes.\n\nIt\'s a WSGI framework and can be used with any WSGI application server such as Gunicorn.\n## Installation\n\n```shell\npip install academlo\n```\n\n\n## How to use it\n\n### Basic usage:\n\n```python\nfrom academlo.api import API\n\napp = API()\n\n\n@app.route("/home")\ndef home(request, response):\n    response.text = "Hello from the HOME page"\n\n\n@app.route("/hello/{name}")\ndef greeting(request, response, name):\n    response.text = f"Hello, {name}"\n\n\n@app.route("/book")\nclass BooksResource:\n    def get(self, req, resp):\n        resp.text = "Books Page"\n\n    def post(self, req, resp):\n        resp.text = "Endpoint to create a book"\n\n\n@app.route("/template")\ndef template_handler(req, resp):\n    resp.body = app.template(\n        "index.html", context={"name": "academlo", "title": "Best Framework"}).encode()\n```\n\n### Unit Tests\n\nThe recommended way of writing unit tests is with [pytest](https://docs.pytest.org/en/latest/). There are two built in fixtures\nthat you may want to use when writing unit tests with academlo. The first one is `app` which is an instance of the main `API` class:\n\n```python\ndef test_route_overlap_throws_exception(app):\n    @app.route("/")\n    def home(req, resp):\n        resp.text = "Welcome Home."\n\n    with pytest.raises(AssertionError):\n        @app.route("/")\n        def home2(req, resp):\n            resp.text = "Welcome Home2."\n```\n\nThe other one is `client` that you can use to send HTTP requests to your handlers. It is based on the famous [requests](http://docs.python-requests.org/en/master/) and it should feel very familiar:\n\n```python\ndef test_parameterized_route(app, client):\n    @app.route("/{name}")\n    def hello(req, resp, name):\n        resp.text = f"hey {name}"\n\n    assert client.get("http://testserver/matthew").text == "hey matthew"\n```\n\n## Templates\n\nThe default folder for templates is `templates`. You can change it when initializing the main `API()` class:\n\n```python\napp = API(templates_dir="templates_dir_name")\n```\n\nThen you can use HTML files in that folder like so in a handler:\n\n```python\n@app.route("/show/template")\ndef handler_with_template(req, resp):\n    resp.html = app.template(\n        "example.html", context={"title": "Awesome Framework", "body": "welcome to the future!"})\n```\n\n## Static Files\n\nJust like templates, the default folder for static files is `static` and you can override it:\n\n```python\napp = API(static_dir="static_dir_name")\n```\n\nThen you can use the files inside this folder in HTML files:\n\n```html\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n  <meta charset="UTF-8">\n  <title>{{title}}</title>\n\n  <link href="/static/main.css" rel="stylesheet" type="text/css">\n</head>\n\n<body>\n    <h1>{{body}}</h1>\n    <p>This is a paragraph</p>\n</body>\n</html>\n```\n\n### Middleware\n\nYou can create custom middleware classes by inheriting from the `academlo.middleware.Middleware` class and overriding its two methods\nthat are called before and after each request:\n\n```python\nfrom academlo.api import API\nfrom academlo.middleware import Middleware\n\n\napp = API()\n\n\nclass SimpleCustomMiddleware(Middleware):\n    def process_request(self, req):\n        print("Before dispatch", req.url)\n\n    def process_response(self, req, res):\n        print("After dispatch", req.url)\n\n\napp.add_middleware(SimpleCustomMiddleware)\n```',
    'author': 'Nicolas',
    'author_email': 'nicolas.rondon@academlo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
