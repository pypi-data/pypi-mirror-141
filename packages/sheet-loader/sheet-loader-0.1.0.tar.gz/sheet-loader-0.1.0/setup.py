# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sheet_loader']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=4.0.0,<5.0.0', 'pandas>=1.4.1,<2.0.0']

extras_require = \
{'fastapi': ['fastapi>=0.74.1,<0.75.0'], 's3path': ['s3path>=0.3.3,<0.4.0']}

setup_kwargs = {
    'name': 'sheet-loader',
    'version': '0.1.0',
    'description': 'Description',
    'long_description': '# Python Template Repo',
    'author': 'Daniel Sullivan',
    'author_email': 'mumblepins@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mumblepins/sheet-loader/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
