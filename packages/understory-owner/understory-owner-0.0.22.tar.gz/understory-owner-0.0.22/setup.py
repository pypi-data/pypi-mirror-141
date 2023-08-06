# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory', 'understory.owner', 'understory.owner.templates']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodome>=3.14.1,<4.0.0', 'understory>=0.0.207,<0.0.208']

setup_kwargs = {
    'name': 'understory-owner',
    'version': '0.0.22',
    'description': '',
    'long_description': None,
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
