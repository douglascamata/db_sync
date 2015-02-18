from setuptools import setup, find_packages

setup(name='db_sync',
      version='0.1',
      description='A simple cassandra/elasticsearch sync package',
      url='http://github.com/douglascamata/db_sync',
      author='Douglas Camata',
      author_email='d.camata@gmail.com',
      license='MIT',
      packages=find_packages(),
      test_suite='nose2.collector.collector',
      install_requires=[
          'nose2',
          'cqlengine',
          'unittest2',
          'elasticsearch-dsl == 0.0.3'
      ],
      zip_safe=False)
