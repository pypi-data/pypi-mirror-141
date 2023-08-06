# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guvicorn_logger']

package_data = \
{'': ['*']}

install_requires = \
['gunicorn>=20.1.0,<21.0.0', 'uvicorn>=0.17.5,<0.18.0']

setup_kwargs = {
    'name': 'guvicorn-logger',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'carlos.rian',
    'author_email': 'crian.rian@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
