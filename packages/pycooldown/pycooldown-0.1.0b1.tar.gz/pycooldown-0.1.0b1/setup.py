# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycooldown']

package_data = \
{'': ['*']}

install_requires = \
['mypy-extensions>=0.4.3,<0.5.0']

setup_kwargs = {
    'name': 'pycooldown',
    'version': '0.1.0b1',
    'description': 'A lightning fast cooldown/ratelimit implementation.',
    'long_description': '# pycooldown\n A lightning-fast cooldown/ratelimit implementation using cython.\n',
    'author': 'Circuit',
    'author_email': 'circuitsacul@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TrigonDev/pycooldown',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
