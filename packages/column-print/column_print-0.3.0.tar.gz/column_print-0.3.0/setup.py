# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['column_print']
setup_kwargs = {
    'name': 'column-print',
    'version': '0.3.0',
    'description': 'A simple way to print short strings to a terminal in columns.',
    'long_description': None,
    'author': 'SteveDaulton',
    'author_email': 'stevedaulton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
