# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apple_data']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'apple-data',
    'version': '1.0.0',
    'description': 'Static data from https://docs.hackdiffe.rent',
    'long_description': '',
    'author': 'Rick Mark',
    'author_email': 'rickmark@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
