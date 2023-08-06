# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['semgrep_agent']

package_data = \
{'': ['*'], 'semgrep_agent': ['templates/*']}

install_requires = \
['GitPython>=3.1.11,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'attrs>=20.3,<22.0',
 'boltons>=20.2.1,<22.0.0',
 'click>=7.1.2,<9.0.0',
 'glom>=20.8.0,<21.0.0',
 'pymmh3>=0.0.5,<0.0.6',
 'requests>=2.24.0,<3.0.0',
 'sh>=1.13.1,<2.0.0']

entry_points = \
{'console_scripts': ['semgrep-agent = semgrep_agent.__main__:error_guard']}

setup_kwargs = {
    'name': 'semgrep-agent',
    'version': '0.1.0b2',
    'description': '',
    'long_description': None,
    'author': 'Return To Corporation',
    'author_email': 'support@r2c.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
