from setuptools import setup, find_packages

def readme():
    with open('README.md') as f: 
        return f.read()

setup(name='Teaching Utilites',
      version='1.0',
      description='some tools to assist various tasks faced by teachers',
      long_description=readme(),
      keywords='education',
      url='http://github.com/astroScott/TeachingUtilities',
      author='Scott Gustafson',
      author_email='s1gustaf@gmail.com',
      license='GNU GPL, version 2',
      packages=find_packages('teachingutils','Tests'),
      package_dir = {'':'teachingutils',
                     'teachingutils/Tests':'teachingutils.Tests'},   # tell distutils packages are under src
      install_requires=['numpy'],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': [],  #TODO later
      },
      include_package_data=True,
      zip_safe=False)
