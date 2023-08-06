# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nordend', 'nordend.commands', 'nordend.spotipy', 'nordend.spotipy.spotipy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['nordend_cli = nordend.__main__:main',
                     'score = nordend.commands.score:main']}

setup_kwargs = {
    'name': 'nordend',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Leo Burgy',
    'author_email': 'leo.burgy@epfl.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
