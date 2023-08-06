# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sbmodder']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0', 'fire>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['sbmodder = sbmodder.client:main']}

setup_kwargs = {
    'name': 'sbmodder',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'takumi2786',
    'author_email': 'takumi_1884@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
