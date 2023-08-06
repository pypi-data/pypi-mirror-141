from setuptools import setup

setup(name='dataflux',
      version='0.1.2',
      description='DataScience Package',
      packages = ['dataflux'],
      install_requires = ["utilum","numpy","pandas","matplotlib"],
      zip_safe = False,
      )