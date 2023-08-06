# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluigent_sdk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fluigent-sdk',
    'version': '0.0.1',
    'description': 'Placeholder for fluigent_sdk by Fluigent',
    'long_description': None,
    'author': 'Paul Müller',
    'author_email': 'dev@craban.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
