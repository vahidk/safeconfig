import os
import sys

from distutils.core import setup
from setuptools import find_packages


# List of runtime dependencies required by this built package
install_requires = ['pyyaml']
if sys.version_info <= (2, 7):
    install_requires += ['future', 'typing']

# read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='safeconfig',
    version='1.0.6',
    description='Structured, flexible, and secure configuration management for Python with CLI support.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vahid Kazemi',
    author_email='vkazemi@gmail.com',
    url='https://github.com/vahidk/safeconfig',
    packages=find_packages(),
    license='MIT',
    install_requires=install_requires,
    test_suite='tests',
)
