#!/usr/bin/env python3

import os
import setuptools

import pathhistogram

_APP_PATH = os.path.dirname(pathhistogram.__file__)

with open(os.path.join(_APP_PATH, 'resources', 'README.md')) as f:
      long_description = f.read()

with open(os.path.join(_APP_PATH, 'resources', 'requirements.txt')) as f:
      install_requires = [s.strip() for s in f.readlines()]

setuptools.setup(
    name='pathhistogram',
    version=pathhistogram.__version__,
    description="A tool to generate histograms of file-sizes",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Dustin Oprea',
    author_email='myselfasunder@gmail.com',
    url='https://github.com/dsoprea/pathhistogram',
    license='GPL 2',
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    package_data={
        'pathhistogram': [
            'resources/README.md',
            'resources/requirements.txt',
        ],
    },
    zip_safe=False,
    install_requires=install_requires,
    scripts=[
        'pathhistogram/resources/scripts/ph_files',
    ],
)
