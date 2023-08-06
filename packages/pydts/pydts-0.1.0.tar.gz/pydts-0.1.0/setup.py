# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydts']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'pydts',
    'version': '0.1.0',
    'description': 'Discrete timeline survival analysis',
    'long_description': '# pydts',
    'author': 'Tomer Meir',
    'author_email': 'tomer1812@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tomer1812/pydts',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
