# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moosetash']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'moosetash',
    'version': '0.1.0',
    'description': 'Mustache template renderer',
    'long_description': None,
    'author': 'Michael Curtis',
    'author_email': 'michaelrccurtis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
