
from setuptools import setup, find_packages

setup(name='data-integrations',
      version='0.0.1',
      description='Python libraries/scripts for various integrations',
      python_requires='>=3.4',
      author='Chris Valaas',
      author_email='cvalaas@mozilla.com',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    )
