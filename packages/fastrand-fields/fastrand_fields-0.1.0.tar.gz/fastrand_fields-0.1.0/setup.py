# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastrand_fields']

package_data = \
{'': ['*']}

install_requires = \
['pytest-flake8>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'fastrand-fields',
    'version': '0.1.0',
    'description': 'Package to randomly generate fields such as funny usernames. Suitable for fast microservices.',
    'long_description': None,
    'author': 'sam',
    'author_email': 'contact@justsam.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jsam/fastrand_fields',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
