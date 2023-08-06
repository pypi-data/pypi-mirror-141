# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genpipe']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'genpipe',
    'version': '0.1.0',
    'description': 'Pipe operator for iterables and generators.',
    'long_description': None,
    'author': 'Noah Pederson',
    'author_email': 'noah@packetlost.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
