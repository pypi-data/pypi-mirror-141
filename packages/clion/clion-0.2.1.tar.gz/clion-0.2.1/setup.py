# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['clion']
setup_kwargs = {
    'name': 'clion',
    'version': '0.2.1',
    'description': 'Minimalistic library for building CLI applications',
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
