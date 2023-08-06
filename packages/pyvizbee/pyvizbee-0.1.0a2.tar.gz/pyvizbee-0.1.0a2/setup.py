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
    'version': '0.1.0a2',
    'description': 'a dualtext alingner based on holoviz panel',
    'long_description': '# pyvizbee\n[![pytest](https://github.com/ffreemt/vizbee/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/vizbee/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/pyvizbee.svg)](https://badge.fury.io/py/pyvizbee)\n\na dualtext aligner based on holoviz panel\n\n## Use it\n### `git clone`\n```bash\ngit clone https://github.com/ffreemt/vizbee\ncd vizbee\npoetry install  # or pip install requirements.txt\npoetry shell\npanel serve vizbee/vizbee.py\n```\n\n### `pypi`\n```shell\n**NOTREADY** pip install pyvizbee\npython -m pyvizbee\n\n```\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/vizbee',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
