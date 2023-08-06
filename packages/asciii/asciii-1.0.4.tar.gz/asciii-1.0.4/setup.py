# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['asciii']
install_requires = \
['Pillow>=9.0.1,<10.0.0']

setup_kwargs = {
    'name': 'asciii',
    'version': '1.0.4',
    'description': 'A library that converts images to ascii',
    'long_description': '# asciii\ncheck the description on my [github](https://github.com/acup1/asciii)\n\noriginal\n![original](https://myoctocat.com/assets/images/base-octocat.svg)\n\nin ascii\n![ascii](https://raw.githubusercontent.com/acup1/asciii/main/examples/asciii_example1.png)',
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
