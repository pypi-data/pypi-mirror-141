# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zdppy_code']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zdppy-code',
    'version': '0.1.0',
    'description': '统一响应格式和响应状态码',
    'long_description': None,
    'author': 'zhangdapeng520',
    'author_email': 'pygosuperman@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
