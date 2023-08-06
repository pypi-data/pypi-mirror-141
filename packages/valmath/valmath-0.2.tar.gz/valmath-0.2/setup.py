#!/usr/bin/env python

from setuptools import setup
# from distutils.core import setup    # also can but cannot create wheel


# This setup is suitable for "python setup.py develop".

setup(name='valmath',
      version='0.2',
      description='A silly math package',
      author='Mike Driscoll',
      author_email='mike@mymath.org',
      url='http://www.mymath.org/',
      packages=['valmath', 'valmath.adv'],
      setup_requires=['wheel'],

      keywords=['python', 'first package'],
      classifiers= [
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Education",
      "Programming Language :: Python :: 2",
      "Programming Language :: Python :: 3",
      "Operating System :: MacOS :: MacOS X",
      "Operating System :: Microsoft :: Windows",
      ]      
)
