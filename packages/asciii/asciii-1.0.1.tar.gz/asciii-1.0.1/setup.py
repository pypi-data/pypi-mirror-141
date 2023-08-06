# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['asciii']
install_requires = \
['Pillow>=9.0.1,<10.0.0']

setup_kwargs = {
    'name': 'asciii',
    'version': '1.0.1',
    'description': 'A library that converts images to ascii',
    'long_description': None,
    'author': 'acup1',
    'author_email': 'georgiyegoriy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
