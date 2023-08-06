# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane']

package_data = \
{'': ['*']}

install_requires = \
['firebase-admin==5.2.0']

setup_kwargs = {
    'name': 'arcane-firebase',
    'version': '0.2.0',
    'description': 'Utility functions for firebase',
    'long_description': '# Arcane firebase\n',
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
