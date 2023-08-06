# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chocs_middleware', 'chocs_middleware.trace']

package_data = \
{'': ['*']}

install_requires = \
['chocs>=1.5.3,<2.0.0', 'gid>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'chocs-middleware.trace',
    'version': '0.2.0',
    'description': 'Http tracing middleware for chocs library.',
    'long_description': '# Chocs-Trace <br> [![PyPI version](https://badge.fury.io/py/chocs-middleware.trace.svg)](https://pypi.org/project/chocs-middleware.trace/) [![CI](https://github.com/kodemore/chocs-trace/actions/workflows/main.yaml/badge.svg)](https://github.com/kodemore/chocs-trace/actions/workflows/main.yaml) [![Release](https://github.com/kodemore/chocs-trace/actions/workflows/release.yml/badge.svg)](https://github.com/kodemore/chocs-trace/actions/workflows/release.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\nHttp tracing middleware for chocs library. \n\n\n# Installation\n\n### Poetry:\n```bash\npoetry add chocs-middleware.trace\n```\n\n### Pip:\n```bash\npip install chocs-middleware.trace\n```\n\n# Usage\n\n## Support tracing in your responses\n\n```python\nfrom chocs_middleware.trace import TraceMiddleware\nfrom chocs import Application, HttpRequest, HttpResponse\n\n# id_prefix will ensure generated tracing headers to contain your prefix\napp = Application(TraceMiddleware(id_prefix="service-name-"))\n\n\n@app.get("/hello")\ndef say_hello(req: HttpRequest) -> HttpResponse:\n    return HttpResponse("Hello!")  # tracing middleware will automatically attach x-request-id, x-correlation-id, x-causation-id headers to your response\n\n```\n\n## Tracing requests\n\n```python\nfrom chocs_middleware.trace import TraceMiddleware, HttpStrategy\nfrom chocs import Application, HttpRequest, HttpResponse\nimport requests\n\n# http_strategy will try to detect requests library and use it to add tracing headers in all your requests\n# if it fails to detect requests library it will fallback to urllib3\napp = Application(TraceMiddleware(http_strategy=HttpStrategy.AUTO))\n\n\n@app.get("/hello")\ndef say_hello(req: HttpRequest) -> HttpResponse:\n    \n    requests.get("http://example.com/test")  # middleware will automatically attach x-correlation-id, x-causation-id and x-request-id headers to your request\n    \n    return HttpResponse("Hello!")\n```\n\n## Using logger\n\n### Formatting message\n\n#### Available properties\n',
    'author': 'Dawid Kraczkowski',
    'author_email': 'dawid.kraczkowski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kodemore/chocs-trace',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
