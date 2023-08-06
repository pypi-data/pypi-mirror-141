# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'main'}

packages = \
['aryan',
 'aryan.contact',
 'aryan.event',
 'aryan.event.events',
 'aryan.internal',
 'aryan.message',
 'aryan.message.code',
 'aryan.message.data']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'loguru>=0.5.3,<0.6.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'aryan',
    'version': '0.0.3.post1',
    'description': 'A small package',
    'long_description': '# Example Package\n\nThis is a simple example package. You can use\n[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)\nto write your content.',
    'author': 'qianmo527',
    'author_email': '2816661524@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
