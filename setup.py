"""
Amatino API Python Bindings
PyPI Setup Module
Author: hugh@amatino.io
"""
from setuptools import setup, find_packages
from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name='amatino',
    version='0.0.1',
    description='Bindings for the Amatino API, a double-entry accounting system',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/amatino-code/amatino-python',
    author='Amatino',
    author_email='hello@amatino.io',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Office/Business :: Financial :: Accounting',
        'Topic :: Software Development :: Libraries'
    ],
    keywords='amatino api bindings accounting double-entry',
    packages=find_packages(),
    python_requires='>=3',
    project_urls={
        'Subscribe': 'https://amatino.io/subscribe',
        'Discuss': 'https://amatino.io/discussion',
        'Development Newsletter': 'https://amatino.io/newsletter'
    }
)