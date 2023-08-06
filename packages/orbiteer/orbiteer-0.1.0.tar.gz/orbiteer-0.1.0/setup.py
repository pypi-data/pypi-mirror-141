# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orbiteer',
 'orbiteer.inputgenerators',
 'orbiteer.notifiers',
 'orbiteer.optimizers',
 'orbiteer.retries',
 'orbiteer.targets']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'orbiteer',
    'version': '0.1.0',
    'description': 'An optimizing chunking command runner',
    'long_description': None,
    'author': 'Avery Fischer',
    'author_email': 'avery@averyjfischer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
