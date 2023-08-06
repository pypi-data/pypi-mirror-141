# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ander']

package_data = \
{'': ['*']}

install_requires = \
['fire']

entry_points = \
{'console_scripts': ['ander = ander.cli:main']}

setup_kwargs = {
    'name': 'ander',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Josuke Yamane',
    'author_email': 's1r0mqme@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joe-yama/ander',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
