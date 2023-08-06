# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['goodboy_flask']

package_data = \
{'': ['*']}

install_requires = \
['goodboy>=0.2,<0.3']

extras_require = \
{':python_version >= "3.6" and python_version < "3.8"': ['typing-extensions>=4.0']}

setup_kwargs = {
    'name': 'goodboy-flask',
    'version': '0.1.0',
    'description': 'Request validation tool for Flask',
    'long_description': '# Goodboy-Flask: Request Validation for Flask\n\nThis project is currently in an early stage of development.',
    'author': 'Maxim Andryunin',
    'author_email': 'maxim.andryunin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
