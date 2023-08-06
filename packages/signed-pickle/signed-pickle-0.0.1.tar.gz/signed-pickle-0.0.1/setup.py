# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['lz4>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'signed-pickle',
    'version': '0.0.1',
    'description': 'Description',
    'long_description': '# Signed Pickle',
    'author': 'Daniel Sullivan',
    'author_email': 'mumblepins@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mumblepins/signed-pickle/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
