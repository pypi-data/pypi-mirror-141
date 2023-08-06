# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['asciii']
setup_kwargs = {
    'name': 'asciii',
    'version': '1.0',
    'description': 'A library that converts images to ascii',
    'long_description': None,
    'author': 'acup1',
    'author_email': 'georgiyegoriy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
