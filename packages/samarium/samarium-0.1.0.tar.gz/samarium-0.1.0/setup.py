# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['samarium']

package_data = \
{'': ['*'], 'samarium': ['modules/*']}

entry_points = \
{'console_scripts': ['samarium = samarium.__main__:main',
                     'samarium-debug = samarium.__main__:main_debug']}

setup_kwargs = {
    'name': 'samarium',
    'version': '0.1.0',
    'description': '',
    'long_description': 'Docs can temporarily be found [here].\n\n[here]: http://github.com/tetraxile/Samarium/blob/docs/README.md',
    'author': 'trag1c',
    'author_email': 'trag1cdev@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
