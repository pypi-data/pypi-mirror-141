# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['igrf_model', 'igrf_model.data']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'igrf-model',
    'version': '1.1.3',
    'description': 'Pure Python implementation of the IGRF13 magnetic model',
    'long_description': None,
    'author': 'Tamas Nepusz',
    'author_email': 'ntamas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
