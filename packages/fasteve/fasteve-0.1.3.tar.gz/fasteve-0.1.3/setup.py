# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fasteve',
 'fasteve.core',
 'fasteve.endpoints',
 'fasteve.io',
 'fasteve.io.mongo',
 'fasteve.methods',
 'fasteve.middleware']

package_data = \
{'': ['*']}

install_requires = \
['email-validator==1.1.1',
 'fastapi>=0.70.1,<0.71.0',
 'motor>=2.5.1,<3.0.0',
 'uvicorn>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'fasteve',
    'version': '0.1.3',
    'description': 'A simple and feature complete REST API framework designed for speed',
    'long_description': None,
    'author': 'Wytamma Wirth',
    'author_email': 'wytamma.wirth@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
