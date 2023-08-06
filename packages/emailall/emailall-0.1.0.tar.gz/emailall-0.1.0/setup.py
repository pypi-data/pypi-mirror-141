# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['emailall',
 'emailall.common',
 'emailall.config',
 'emailall.modules',
 'emailall.modules.datasets',
 'emailall.modules.search']

package_data = \
{'': ['*']}

install_requires = \
['fake-useragent>=0.1.11,<0.2.0',
 'fire>=0.4.0,<0.5.0',
 'loguru>=0.6.0,<0.7.0',
 'lxml>=4.8.0,<5.0.0',
 'prettytable>=3.1.1,<4.0.0',
 'requests>=2.27.1,<3.0.0',
 'urllib3>=1.26.8,<2.0.0']

setup_kwargs = {
    'name': 'emailall',
    'version': '0.1.0',
    'description': 'EmailAll is a powerful Email Collect tool —— 一款强大的邮箱收集工具',
    'long_description': None,
    'author': 'zmf963',
    'author_email': 'zmf96@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
