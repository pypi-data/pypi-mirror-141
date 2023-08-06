# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetrypkgtemplatelucas']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poetrypkgtemplatelucas',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'edkrueger',
    'author_email': 'edkrueger@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
