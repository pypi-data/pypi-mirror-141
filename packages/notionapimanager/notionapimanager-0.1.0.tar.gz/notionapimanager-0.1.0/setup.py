# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notionapimanager']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.0,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'notionapimanager',
    'version': '0.1.0',
    'description': 'Python package for consulting, creating and editing Notion databases',
    'long_description': None,
    'author': 'Ruben Chulia Mena',
    'author_email': 'rubchume@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
