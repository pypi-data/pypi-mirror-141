# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hao']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML',
 'chardet',
 'decorator',
 'ldap3',
 'oss2',
 'passlib',
 'pydantic',
 'python-fity3',
 'pytz',
 'regex',
 'requests',
 'tqdm']

setup_kwargs = {
    'name': 'hao',
    'version': '3.6.0',
    'description': 'conf, logs, namespace, etc',
    'long_description': None,
    'author': 'orctom',
    'author_email': 'orctom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
