# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['napr',
 'napr.apps',
 'napr.apps.coconut',
 'napr.apps.coconut.terpene',
 'napr.data',
 'napr.plotting',
 'napr.utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'tqdm>=4.63.0,<5.0.0']

setup_kwargs = {
    'name': 'napr',
    'version': '0.1.3',
    'description': 'Machine learning meets natural products',
    'long_description': None,
    'author': 'Morteza Hosseini',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
