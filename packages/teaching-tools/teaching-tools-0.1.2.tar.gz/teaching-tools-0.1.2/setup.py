# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teaching_tools']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=8.1.1,<9.0.0',
 'ipywidgets>=7.6.5,<8.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'teaching-tools',
    'version': '0.1.2',
    'description': 'Teaching tools for the WQU Data Science Lab',
    'long_description': None,
    'author': 'Nicholas Cifuentes-Goodbody',
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
