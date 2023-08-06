# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['etchrepl']
install_requires = \
['etchlang', 'requests>=2.27.1,<3.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['etch = etchrepl:main']}

setup_kwargs = {
    'name': 'etchrepl',
    'version': '0.1.5',
    'description': 'A repl for Etch. Nothing much to see here.',
    'long_description': None,
    'author': 'GingerIndustries',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
