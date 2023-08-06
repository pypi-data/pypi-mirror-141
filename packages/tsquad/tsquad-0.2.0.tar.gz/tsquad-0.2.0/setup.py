# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tsquad']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'mpmath>=1.2.1,<2.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pytest>=7.0.0,<8.0.0']

setup_kwargs = {
    'name': 'tsquad',
    'version': '0.2.0',
    'description': 'numeric quadrature using the Tanh-Sinh variable transformation',
    'long_description': None,
    'author': 'Richard Hartmann',
    'author_email': 'richard.hartmann@tu-dresden.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
