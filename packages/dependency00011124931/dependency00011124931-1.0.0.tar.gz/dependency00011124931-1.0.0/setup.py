from setuptools import setup
from setuptools.command.install import install
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        os.system("mousepad")


setup(name='dependency00011124931', #package name
      version='1.0.0',
      description='test',
      author='test',
      license='MIT',
      zip_safe=False,
      cmdclass={'install': CustomInstall})