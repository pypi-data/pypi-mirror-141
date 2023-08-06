# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['laboris', 'laboris.commands', 'laboris.reports']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'halo>=0.0.31,<0.0.32',
 'humanize>=4.0.0,<5.0.0',
 'isodate>=0.6.1,<0.7.0',
 'pony>=0.7.16,<0.8.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'rich>=11.2.0,<12.0.0']

entry_points = \
{'console_scripts': ['laboris = laboris.main:main']}

setup_kwargs = {
    'name': 'laboris',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Arden Rasmussen',
    'author_email': 'ardenisthebest@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
