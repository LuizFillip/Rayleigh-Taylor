#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2017, JK & AGB
# Full license can be found in License.md
#-----------------------------------------------------------------------------

from os import path
from setuptools import setup, find_packages

# Define a read function for using README for long_description

def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()


setup(name='Rayleigh-Taylor',
      version='0.1',
      url='github.com/LuizFillip/Rayleigh-Taylor',
      author='Luiz Fillip',
      author_email='luizfillip6@gmail.com',
      description='Prepares geophysical data for compute IRT growth rate',
      long_description=read('README.md'),
      packages=find_packages(),
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Topic :: Scientific/Engineering :: Physics",
          "Intended Audience :: Science/Research",
          "License :: BSD",
          "Natural Language :: English",
          "Programming Language :: Python :: 3.6",
      ],
      include_package_data=True,
      zip_safe=False,
)