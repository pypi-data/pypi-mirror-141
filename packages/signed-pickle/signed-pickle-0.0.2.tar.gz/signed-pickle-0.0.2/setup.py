# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['signed_pickle']

package_data = \
{'': ['*']}

install_requires = \
['lz4>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'signed-pickle',
    'version': '0.0.2',
    'description': 'Description',
    'long_description': '# Signed Pickle',
    'author': 'Daniel Sullivan',
    'author_email': 'mumblepins@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mumblepins/signed-pickle/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
