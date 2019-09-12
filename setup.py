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
        'importlib_resources',
        'geopy==1.20.0',
        'requests==2.22.0',
        'bonobo==0.6.4',
        'pandas',
        'geopy==1.20.0',
        'python-gnupg',
        'pysftp',
        'google-cloud-storage',
        'google-cloud-bigquery',
        'gcsfs',
        'mockito==1.1.1',
        'pytest==5.0.1',
        'pytest-cov==2.7.1',
        'pytest-mock==1.10.4',
        'mock==3.0.5',
        'patch==1.16',
        'pyopenssl',
        'behave',
        'purl',
        'jsoncompare',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib'
      ]
    )
