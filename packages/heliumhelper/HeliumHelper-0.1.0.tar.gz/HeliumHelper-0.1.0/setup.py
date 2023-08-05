# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['heliumhelper']

package_data = \
{'': ['*']}

install_requires = \
['flatdict>=4.0.1,<5.0.0', 'pandas>=1.4.1,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'heliumhelper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Nathan Pirhalla',
    'author_email': 'steelersfan5052@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
