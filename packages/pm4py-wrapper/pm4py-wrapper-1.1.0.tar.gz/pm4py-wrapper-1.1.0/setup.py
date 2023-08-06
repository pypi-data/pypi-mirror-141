# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pm4py_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pm4py>=2.2.19,<3.0.0',
 'pytest>=7.0.1,<8.0.0']

entry_points = \
{'console_scripts': ['pm4py_wrapper = pm4py_wrapper.cli:main']}

setup_kwargs = {
    'name': 'pm4py-wrapper',
    'version': '1.1.0',
    'description': 'pm4py wrapper to call the original package from CLI',
    'long_description': None,
    'author': 'Ihar Suvorau',
    'author_email': 'ihar.suvorau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
