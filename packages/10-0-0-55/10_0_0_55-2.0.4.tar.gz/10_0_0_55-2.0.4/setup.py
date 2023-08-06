# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['10_0_0_55']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': '10-0-0-55',
    'version': '2.0.4',
    'description': 'A headless login / logout script for 10.0.0.55',
    'long_description': None,
    'author': 'spencerwooo',
    'author_email': 'spencer.woo@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
