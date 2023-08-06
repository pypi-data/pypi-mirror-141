# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xxp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xxp',
    'version': '22.3a0',
    'description': 'xxd ripoff',
    'long_description': None,
    'author': 'Nick Timkovich',
    'author_email': 'prometheus235@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
