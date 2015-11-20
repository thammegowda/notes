#!/usr/bin/env python
# encoding: utf-8
# $Id$

import os.path

try:
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    pass

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

version = '0.1'

_descr = u'''**********
CS programming notes and scripts
***************
.. contents::
CS programming Notes and Scripts
'''
_keywords = 'Notes Algorithms Scripts ComputerScience Programming'
_classifiers = [
    'Development Status :: 1 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Students',
    'Intended Audience :: Computer Science',
    'Intended Audience :: Science/Research',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Database :: Notes',
    'Topic :: Database :: Reference',
    'Topic :: Database :: Education',
]

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = _descr

setup(
    name='notes',
    version=version,
    description='CS programming Notes and Scripts',
    long_description=long_description,
    classifiers=_classifiers,
    keywords=_keywords,
    author='Thamme Gowda N.',
    author_email='tgowdan@gmail.com',
    url='https://github.com/thammegowda/notes/tree/master/python',
    download_url='https://github.com/thammegowda/notes/tree/master/python',
    license=read('../LICENSE'),
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=True,
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'notes = notes:main'
        ],
    },
    package_data = {
        # And include any *.conf files found in the 'conf' subdirectory
        # for the package
    },
    install_requires=[
        'setuptools',
        'requests'
    ]
)