from setuptools import setup, find_packages
import re

VERSIONFILE = 'maeapi/_version.py'

version_line = open(VERSIONFILE).read()
version_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
match = re.search(version_re, version_line, re.M)
if match:
    version = match.group(1)
else:
    raise RuntimeError("Could not find version in '%s'" % VERSIONFILE)

setup(name='maeapi',
      version=version,
      description='Unofficial API for MAE',
      url='https://github.com/liej6799/maeapi',
      author='liej6799',
      author_email='',
      license='MIT',
      packages=find_packages(),
      install_requires=['requests >= 2.22'],
      python_requires=">=3.6",
      include_package_data=True,
      zip_safe=False)
