# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resist']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0', 'tornado>=6.1,<7.0']

setup_kwargs = {
    'name': 'resist',
    'version': '0.1.0',
    'description': 'Strongly typed revolt API wrapper.',
    'long_description': 'RESIST\n======\nAn API wrapper for `revolt`\n\n\nGoals\n=====\n- Strongly typed `revolt` API wrapper.\n- Good semantics & conventions.\n- Explicit.\n\n\nNotable contributors\n====================\n- `Andy <https://github.com/an-dyy>`_ Creater & Maintainer.\n',
    'author': 'andy',
    'author_email': 'andy.development@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/an-dyy/Resist',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
