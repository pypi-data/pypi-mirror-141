# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sholl']

package_data = \
{'': ['*']}

install_requires = \
['jinja2==3.0.3']

entry_points = \
{'console_scripts': ['sholl = sholl.sholl:main']}

setup_kwargs = {
    'name': 'sholl',
    'version': '0.0.6',
    'description': 'Generate or Updates Hombrew formulas for your python projects',
    'long_description': None,
    'author': 'jeremynac',
    'author_email': 'jeremynac@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.1,<4.0',
}


setup(**setup_kwargs)
