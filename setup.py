#!/usr/bin/python
from distutils.core import setup

setup(name='Teaching Utilities',
      version='1.0',
      description='some tools to assist various tasks faced by teachers',
      author='Scott Gustafson',
      author_email='s1gustaf@gmail.com',
      packages=['TeachingUtils','Tests'],
      package_dir={'TeachingUtils':'./','Tests':'./Tests'},
      package_data={'TeachingUtils':'./Data/data.cfg'},
      license='MIT License',
      long_description=open('README.md').read(),
     )
