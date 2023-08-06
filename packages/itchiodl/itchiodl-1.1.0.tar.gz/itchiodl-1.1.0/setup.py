# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itchiodl', 'itchiodl.bundle_tool', 'itchiodl.downloader']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0', 'clint>=0.5.1,<0.6.0', 'requests']

setup_kwargs = {
    'name': 'itchiodl',
    'version': '1.1.0',
    'description': 'Python Scripts for downloading / archiving your itchio library',
    'long_description': None,
    'author': 'Peter Taylor',
    'author_email': 'me@et1.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
