# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coro_context_manager']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'coro-context-manager',
    'version': '0.1.0',
    'description': 'A simple object to wrap couroutines to make them awaitable or used via an asyn context manager',
    'long_description': None,
    'author': 'Zach Schumacher',
    'author_email': 'zachary@simplebet.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<=3.10',
}


setup(**setup_kwargs)
