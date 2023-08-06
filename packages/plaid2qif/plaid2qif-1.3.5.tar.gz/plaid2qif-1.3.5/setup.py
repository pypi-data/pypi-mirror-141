# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plaid2qif']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'plaid-python>=7.2.0,<8.0.0',
 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'plaid2qif',
    'version': '1.3.5',
    'description': 'Download financial transactions from Plaid as QIF files.',
    'long_description': None,
    'author': 'Edward Q. Bridges',
    'author_email': 'github@eqbridges.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
