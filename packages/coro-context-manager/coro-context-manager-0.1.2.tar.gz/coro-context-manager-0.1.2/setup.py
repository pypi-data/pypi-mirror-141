# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coro_context_manager']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'coro-context-manager',
    'version': '0.1.2',
    'description': 'A simple object to wrap coroutines to make them awaitable or used via an asyn context manager',
    'long_description': '[![test](https://github.com/zschumacher/coro-context-manager/actions/workflows/test.yml/badge.svg)](https://github.com/zschumacher/coro-context-manager/actions/workflows/test.yml)\n[![PyPI version](https://badge.fury.io/py/coro-context-manager.svg)](https://badge.fury.io/py/coro-context-manager)\n[![codecov](https://codecov.io/gh/zschumacher/coro-context-manager/branch/main/graph/badge.svg?token=6610H3V6JE)](https://codecov.io/gh/zschumacher/coro-context-manager)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/coro-context-manager)\n\n# coro-context-manager\n*coro-context-manager* is a simple python package that includes an object that can wrap a coroutine to allow it to\nbehave as a context manager or a regular awaitable.\n\nThis class is super useful when you have a coroutine that returns an object that defines an async context manager using\n`__aenter__` and `__aexit__`\n\n## Installation\n\n### pip\n```console\npip install coro-context-manager\n```\n\n### poetry\n```console\npoetry add coro-context-manager\n```\n\n\n## Usage\n*CoroContextManager* can be used to wrap a coroutine so that it can be awaited or called via an async context manager\nin which case the library will try to use the underlying object\'s `__aenter__` and `__aexit__`, if they exist.\n```python\nimport asyncio\n\nfrom coro_context_manager import CoroContextManager\n\n\nclass MyObject:\n\n    def __init__(self, initial_value):\n        self.some_value = initial_value\n\n    async def __aenter__(self):\n        await asyncio.sleep(.1)\n        self.some_value += 1\n        return self\n\n    async def __aexit__(self, exc_type, exc_val, exc_tb):\n        await asyncio.sleep(.1)\n        self.some_value -= 1\n\n    @classmethod\n    async def an_io_intensive_constructor(cls, initial_value):\n        await asyncio.sleep(10)\n        return cls(initial_value)\n\n\nasync def main():\n    """\n    Using CoroContextManager, I get a coroutine I can await or use with an async context manager, which proxies to\n    the context manager defined on object returned by the coroutine, if it exists.\n    """\n\n    # i can await it directly\n    myobj = await CoroContextManager(MyObject.an_io_intensive_constructor(5))\n    print(type(myobj))\n    # <class \'__main__.MyObject\'>\n\n    # or use it as an async context manager, not having to await it, with the same api!\n    async with CoroContextManager(MyObject.an_io_intensive_constructor(5)) as myobj:\n        print(type(myobj))\n        # <class \'__main__.MyObject\'>\n        print(myobj.some_value)\n        # 6\n\n    print(myobj.some_value)\n    # 5\n\n\nasyncio.run(main())\n```\n\n## Rationale\nThis is a common enough pattern used in several async packages all with slightly different implementation.  It would be\nnice if there was a consistent pattern everyone was using; this package aims to provide that.\n\n* [aiopg](https://github.com/aio-libs/aiopg/blob/master/aiopg/utils.py#L44)\n* [aioodbc](https://github.com/aio-libs/aioodbc/blob/master/aioodbc/utils.py#L36)\n* [aiohttp](https://github.com/aio-libs/aiohttp/blob/7514f220947ce078d4dd039cd0be49929b9976cc/aiohttp/client.py#L1082)\n* [cx_Oracle_async](https://github.com/GoodManWEN/cx_Oracle_async/blob/main/cx_Oracle_async/context.py#L3)\n* [aiomysql](https://github.com/aio-libs/aiomysql/blob/master/aiomysql/utils.py#L30)\n\n## Latest Changes\n\n',
    'author': 'Zach Schumacher',
    'author_email': 'zschu15@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
