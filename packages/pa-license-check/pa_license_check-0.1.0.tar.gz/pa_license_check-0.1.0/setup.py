# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pa_license_check']

package_data = \
{'': ['*']}

install_requires = \
['DateTime>=4.4,<5.0',
 'click>=8.0.4,<9.0.0',
 'configparser>=5.2.0,<6.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'urllib3>=1.26.8,<2.0.0']

entry_points = \
{'console_scripts': ['palicensecheck = pa_license_check.cli:cli']}

setup_kwargs = {
    'name': 'pa-license-check',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Angelo Poggi',
    'author_email': 'angelo.poggi@opti9tech.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
