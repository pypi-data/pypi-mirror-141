# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csv_json_converter_bruno_areis']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['csv_json_converter = '
                     'csv_json_converter_bruno_areis.converter:converter']}

setup_kwargs = {
    'name': 'csv-json-converter-bruno-areis',
    'version': '0.1.8',
    'description': 'Convert csv to json or json to csv',
    'long_description': '',
    'author': 'Bruno Reis',
    'author_email': 'brunoalvesbhx@gmail.com',
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
