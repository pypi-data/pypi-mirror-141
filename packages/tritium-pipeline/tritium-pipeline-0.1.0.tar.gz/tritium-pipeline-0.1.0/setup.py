# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tritium_pipeline']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tritium-pipeline',
    'version': '0.1.0',
    'description': 'Log based job pipeline tool',
    'long_description': None,
    'author': 'voidpointercast',
    'author_email': 'patrick.daniel.gress@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
