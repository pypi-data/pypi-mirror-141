# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['primapy_pizzapy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'primapy-pizzapy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'gianpy15',
    'author_email': 'gianpaolo.dipietro@prima.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
