# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zdppy_log',
 'zdppy_log.libs',
 'zdppy_log.libs.colorama',
 'zdppy_log.libs.loguru']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zdppy-log',
    'version': '0.1.5',
    'description': 'python日志工具',
    'long_description': None,
    'author': 'zhangdapeng',
    'author_email': 'pygosuperman@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
