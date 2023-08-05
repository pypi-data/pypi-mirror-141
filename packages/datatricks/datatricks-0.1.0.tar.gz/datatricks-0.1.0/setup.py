# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datatricks']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0', 'pandas>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'datatricks',
    'version': '0.1.0',
    'description': 'Common Functions for Data Science/Analysis',
    'long_description': None,
    'author': 'Shivam Anand',
    'author_email': 'shivam01anand@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shivam01anand/datatricks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
