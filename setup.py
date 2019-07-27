import os
import setuptools
from setuptools import setup, find_packages

setup(name='data-integrations',
      version='0.0.1',
      description='Python libraries/scripts for various integrations',
      python_requires='>=3.4',
      author='Chris Valaas',
      author_email='cvalaas@mozilla.com',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      scripts=[s for s in setuptools.findall('bin/') if os.path.splitext(s)[1] != '.pyc'],
      install_requires=[
        'requests',
        'geopy',
        'pytz',
      ]
    )
