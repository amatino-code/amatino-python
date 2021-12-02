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
with open(path.join(here, 'README.md'), encoding='utf-8') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

with open(path.join(here, 'VERSION'), encoding='utf-8') as version_file:
    VERSION = version_file.read()

setup(
    name='amatino',
    version=VERSION,
    description='Bindings for the Amatino API, an accounting & financial data e\
ngine',
    long_description=LONG_DESCRIPTION,
    url='https://amatino.io',
    author='Amatino',
    author_email='hugh@amatino.io',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Topic :: Office/Business :: Financial :: Accounting',
        'Topic :: Software Development :: Libraries'
    ],
    keywords='amatino api bindings accounting double-entry accounts library',
    packages=find_packages(exclude=('tests', 'tests.*')),
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    install_requires=['typing'],
    project_urls={
        'Twitter': 'https://twitter.com/amatinoapi',
        'Github Repository': 'https://github.com/amatino-code/amatino-python',
        'Subscribe': 'https://amatino.io/subscribe',
        'Getting Started Guide': 'https://amatino.io/articles/getting-started',
        'Discuss': 'https://amatino.io/discussion',
        'Development Newsletter': 'https://amatino.io/newsletter'
    }
)
