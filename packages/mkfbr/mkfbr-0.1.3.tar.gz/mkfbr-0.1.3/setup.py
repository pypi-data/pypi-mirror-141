# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkfbr']

package_data = \
{'': ['*'], 'mkfbr': ['database/*', 'json/*']}

setup_kwargs = {
    'name': 'mkfbr',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Matheus Santos',
    'author_email': '78329418+darkmathew@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
