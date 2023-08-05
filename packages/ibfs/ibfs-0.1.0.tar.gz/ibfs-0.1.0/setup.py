# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ibfs']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0.3,<9.0.0',
 'fusepy>=3.0.1,<4.0.0',
 'requests>=2.27.1,<3.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'trieregex>=1.0.0,<2.0.0',
 'ujson>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'ibfs',
    'version': '0.1.0',
    'description': 'Mount instabase filesystem API locally',
    'long_description': None,
    'author': 'Arjoonn Sharma',
    'author_email': 'arjoonn.sharma@instabase.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
