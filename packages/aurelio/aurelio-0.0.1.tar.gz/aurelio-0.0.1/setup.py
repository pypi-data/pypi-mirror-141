# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aurelio', 'aurelio.clients', 'aurelio.settings']

package_data = \
{'': ['*']}

extras_require = \
{'redis': ['redis>=4.1.4,<5.0.0']}

setup_kwargs = {
    'name': 'aurelio',
    'version': '0.0.1',
    'description': 'Python dictionary interface for key-value databases',
    'long_description': None,
    'author': 'KelvinS',
    'author_email': 'kelvinpfw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
