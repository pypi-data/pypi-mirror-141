# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tritium_pipeline',
 'tritium_pipeline.algebra',
 'tritium_pipeline.algebra.types',
 'tritium_pipeline.distribution',
 'tritium_pipeline.log']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0', 'toolz>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'tritium-pipeline',
    'version': '0.3.0',
    'description': 'Log based job pipeline tool',
    'long_description': None,
    'author': 'voidpointercast',
    'author_email': 'patrick.daniel.gress@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
