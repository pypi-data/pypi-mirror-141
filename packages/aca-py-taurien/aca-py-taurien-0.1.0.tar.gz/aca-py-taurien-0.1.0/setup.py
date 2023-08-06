# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aca_py_taurien']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aca-py-taurien',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Taurien',
    'author_email': 'michel.a.c474@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
