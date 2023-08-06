# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cbpro']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'coinbasepro-revived',
    'version': '1.1.12',
    'description': 'Revived https://github.com/danpaquin/coinbasepro-python. Python package to interact with the coinbase pro api https://docs.pro.coinbase.com/.',
    'long_description': None,
    'author': 'me',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
