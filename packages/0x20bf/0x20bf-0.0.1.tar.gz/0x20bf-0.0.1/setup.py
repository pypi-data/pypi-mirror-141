# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['0x20bf']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==5.4.1',
 'aiohttp==3.7.4.post0',
 'gnupg>=2.3.1,<3.0.0',
 'pre_commit>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': '0x20bf',
    'version': '0.0.1',
    'description': '0x20bf: This document proposes an Internet standards track protocol for transporting, broadcasting and syndication of messages over common internet communications channels. The distribution of all documents related to this proposal are unlimited and unencumbered by any LICENSE, but some are included anyway.',
    'long_description': None,
    'author': 'randymcmillan',
    'author_email': 'randy.lee.mcmillan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
