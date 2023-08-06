#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='ctm-py',
    version='0.0.1',
    description='Cloud Task Manager',
    url='',
    author='',
    author_email='',
    license='',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    keywords='Cloud Task Manager',
    packages=find_packages(),
    install_requires=[
          'fire', 'pyyaml', 'redis', 'tabulate'
    ],
    entry_points={
          'console_scripts': [
              'ctm = ctm.ctm:main'
          ]
    },
)