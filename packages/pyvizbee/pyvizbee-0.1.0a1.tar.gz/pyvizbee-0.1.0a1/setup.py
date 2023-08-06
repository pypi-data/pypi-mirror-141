# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyvizbee']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.4.2,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'logzero>=1.7.0,<2.0.0',
 'panel>=0.12.6,<0.13.0',
 'param>=1.12.0,<2.0.0']

setup_kwargs = {
    'name': 'pyvizbee',
    'version': '0.1.0a1',
    'description': 'a dualtext alingner based on holoviz panel',
    'long_description': None,
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
