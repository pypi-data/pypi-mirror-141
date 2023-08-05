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
    'version': '0.3.0',
    'description': 'HeliumHelper is a Python library to aid in creating Helium apps.',
    'long_description': '# HeliumHelper\n\nHeliumHelper is a Python library to aid in creating Helium apps.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install HeliumHelper.\n\n```bash\npip install HeliumHelper\n```\n\n## Usage\n\n```python\nfrom heliumhelper import helpers\n\n# returns current oracle price\nhelpers.get_current_price()\n```\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'Nathan Pirhalla',
    'author_email': 'steelersfan5052@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nathan7432/HeliumHelper.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
