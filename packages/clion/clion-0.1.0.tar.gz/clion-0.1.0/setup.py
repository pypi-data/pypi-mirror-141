# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['clion']
setup_kwargs = {
    'name': 'clion',
    'version': '0.1.0',
    'description': 'Minimalistic CLI library',
    'long_description': None,
    'author': 'Yevhen Shymotiuk',
    'author_email': 'yshym@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
