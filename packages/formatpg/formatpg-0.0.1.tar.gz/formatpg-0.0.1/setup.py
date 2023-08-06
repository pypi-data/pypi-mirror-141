# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formatpg']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'formatpg',
    'version': '0.0.1',
    'description': '',
    'long_description': '# formatpg\n\nPlaceholder until I rename [buildpg](https://pypi.org/project/buildpg/) to use this name.\n',
    'author': 'Samuel Colvin',
    'author_email': 's@muelcolvin.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
