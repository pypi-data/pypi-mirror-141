# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leoribas_csv_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pathlib>=1.0.1,<2.0.0']

entry_points = \
{'console_scripts': ['converter = '
                     'leoribas_csv_converter.converter:json_converter']}

setup_kwargs = {
    'name': 'leoribas-csv-converter',
    'version': '0.2.0',
    'description': '',
    'long_description': '',
    'author': 'Leonardo Ribas',
    'author_email': 'leo_rnm@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
