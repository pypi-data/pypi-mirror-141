# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libnova', 'libnova.log', 'libnova.pwn', 'libnova.struct', 'libnova.typ']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs>=15.0.1,<16.0.0', 'pwntools>=4.7.0,<5.0.0']

setup_kwargs = {
    'name': 'libnova',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'novafacing',
    'author_email': 'rowanbhart@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.10',
}


setup(**setup_kwargs)
