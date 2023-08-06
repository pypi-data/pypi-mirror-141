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
    'version': '0.1.0b2',
    'description': 'A lightning fast cooldown/ratelimit implementation.',
    'long_description': "# pycooldown\n[![pypi](https://github.com/TrigonDev/apgorm/actions/workflows/pypi.yml/badge.svg)](https://pypi.org/project/apgorm)\n\n[Documentation](https://github.com/trigondev/pycooldown/wiki) | [CONTRIBUTING.md](https://github.com/trigondev/.github/tree/main/CONTRIBUTING.md)\n\nA lightning-fast cooldown/ratelimit implementation using cython.\n\nIf you need support, you can contact me `CircuitSacul#3397` after joining [this server](https://discord.gg/dGAzZDaTS9). I don't accept friend requests.\n",
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
