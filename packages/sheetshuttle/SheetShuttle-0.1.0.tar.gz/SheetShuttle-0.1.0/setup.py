# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sheetshuttle']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.55,<2.0',
 'PyYAML>=5.4.1,<6.0.0',
 'google-api-python-client>=2.21.0,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth-oauthlib>=0.4.6,<0.5.0',
 'jsonschema>=4.1.2,<5.0.0',
 'openpyxl-stubs>=0.1.21,<0.2.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.3.3,<2.0.0',
 'pluginbase>=1.0.1,<2.0.0',
 'python-dotenv>=0.19.1,<0.20.0',
 'rich>=10.9.0,<11.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer[all]>=0.3.2,<0.4.0',
 'types-PyYAML>=6.0.0,<7.0.0',
 'types-jsonschema>=4.4.1,<5.0.0']

entry_points = \
{'console_scripts': ['sheetshuttle = sheetshuttle.main:app']}

setup_kwargs = {
    'name': 'sheetshuttle',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Noor Buchi',
    'author_email': 'buchin@allegheny.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.6,<4.0.0',
}


setup(**setup_kwargs)
