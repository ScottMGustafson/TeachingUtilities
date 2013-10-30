#!/usr/bin/python
from distutils.core import setup

setup(name='Teaching Utilities',
      version='1.0',
      description='some tools to assist various tasks faced by teachers',
      author='Scott Gustafson',
      author_email='s1gustaf@gmail.com',
      packages=['TeachingUtils','TeachingUtils.Tests','TeachingUtils.scripts'],
      package_dir={'TeachingUtils':'./src','TeachingUtils.Tests':'./Tests','TeachingUtils.scripts':'./scripts'},
      #package_data={'TeachingUtils':'./Data/data.cfg'},
      license='MIT License',
      long_description=open('README.md').read(),
     )
