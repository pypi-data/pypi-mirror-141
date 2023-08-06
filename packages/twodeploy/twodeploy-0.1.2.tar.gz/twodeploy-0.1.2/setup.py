from setuptools import setup

setup(name='twodeploy',
      version='0.1.2',
      description='Deploying Package',
      packages = ['package'],
      install_requires = ["utilum","numpy","pandas","matplotlib"],
      zip_safe = False,
      )