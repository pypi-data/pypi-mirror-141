# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csv_json_converter_bruno_areis']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'csv-json-converter-bruno-areis',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
