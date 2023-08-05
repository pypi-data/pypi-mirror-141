# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['floip', 'floip.models']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'flow-interop-tools',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Weni',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
