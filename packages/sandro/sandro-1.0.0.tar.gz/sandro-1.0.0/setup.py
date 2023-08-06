# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sandro']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sandro',
    'version': '1.0.0',
    'description': "Hi, I'm Sandro",
    'long_description': None,
    'author': 'Sandro Meireles',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
