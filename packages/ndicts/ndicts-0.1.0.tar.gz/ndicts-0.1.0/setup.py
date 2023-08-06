# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ndicts']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ndicts',
    'version': '0.1.0',
    'description': 'Class to handle nested dictionaries',
    'long_description': None,
    'author': 'Edoardo Cicirello',
    'author_email': 'e.cicirello@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
