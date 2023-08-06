# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moosetash']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'moosetash',
    'version': '0.2.0',
    'description': 'Mustache template renderer',
    'long_description': '# Moosetash\n\n## A Mustache template renderer for Python\n\nMoosetash is a python implementation of the [Mustache](https://mustache.github.io/) templating specification.\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.\n',
    'author': 'Michael Curtis',
    'author_email': 'michaelrccurtis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/michaelrccurtis/moosetash',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
