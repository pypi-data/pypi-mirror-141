# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['echo1_geopix']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'echo1-geopix',
    'version': '0.1.0',
    'description': '',
    'long_description': '# echo1-geopix',
    'author': 'Michael Mohamed',
    'author_email': 'michael.mohamed@echo1.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/e1-io/echo1-geopix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.6.2',
}


setup(**setup_kwargs)
