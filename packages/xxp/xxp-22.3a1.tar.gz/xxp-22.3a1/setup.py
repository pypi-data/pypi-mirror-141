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
    'version': '22.3a1',
    'description': 'xxd ripoff',
    'long_description': "# xxp\n\n## What\n\nIt's [`xxd`][xxddoc] ([C source][xxdsrc]), but in Python, so it can also provide an API. Helpful when trying to reverse engineer binary things.\n\n## Why\n\nPart created for a want of a Python binary-dumper to decode my LoRa messages, part to learn GitHub Actions.\n\n\n[xxddoc]: https://linux.die.net/man/1/xxd\n[xxdsrc]: https://github.com/vim/vim/blob/master/src/xxd/xxd.c\n",
    'author': 'Nick Timkovich',
    'author_email': 'prometheus235@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nicktimko/xxd',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
