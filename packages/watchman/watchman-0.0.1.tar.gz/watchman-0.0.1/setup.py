# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['watchman']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'watchman',
    'version': '0.0.1',
    'description': '',
    'long_description': '# watchman \n\nPlaceholder until I rename [watchgod](https://pypi.org/project/watchgod/) to use this name.\n',
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
