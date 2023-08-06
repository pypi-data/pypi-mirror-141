# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dorfperfekt']

package_data = \
{'': ['*']}

install_requires = \
['PySide6>=6.2.3,<7.0.0', 'matplotlib>=3.5.1,<4.0.0', 'numpy>=1.22.2,<2.0.0']

entry_points = \
{'console_scripts': ['dorfperfekt = dorfperfekt.__main__:main']}

setup_kwargs = {
    'name': 'dorfperfekt',
    'version': '0.1.0',
    'description': 'Tile placement suggestions for the game Dorfromantik.',
    'long_description': None,
    'author': 'amosborne',
    'author_email': 'amosborne@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
