# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['masureel', 'masureel.max']

package_data = \
{'': ['*'], 'masureel': ['data/*']}

install_requires = \
['airtable-python-wrapper>=0.15.3,<0.16.0',
 'click>=8.0.3,<9.0.0',
 'pick>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['masureel = masureel.console:main']}

setup_kwargs = {
    'name': 'masureel',
    'version': '0.1.9.4',
    'description': '',
    'long_description': None,
    'author': 'Lucas Selfslagh',
    'author_email': 'lucas.selfslagh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.10',
}


setup(**setup_kwargs)
