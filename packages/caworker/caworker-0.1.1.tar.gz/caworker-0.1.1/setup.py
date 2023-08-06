# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['caworker']

package_data = \
{'': ['*']}

install_requires = \
['pycamunda>=0.6.0,<0.7.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'caworker',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Gustavo Côrtes',
    'author_email': 'gpcortes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
