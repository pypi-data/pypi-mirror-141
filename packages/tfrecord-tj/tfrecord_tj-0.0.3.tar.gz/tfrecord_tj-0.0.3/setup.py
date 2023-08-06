import os
import sys

from distutils.core import setup
from setuptools import find_packages


# List of runtime dependencies required by this built package
install_requires = []
if sys.version_info <= (2, 7):
    install_requires += ['future', 'typing']
install_requires += ['numpy', 'protobuf', 'crc32c']

# read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='tfrecord_tj',
    version='0.0.3',
    description='TFRecord reader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Tao Jiang',
    author_email='tjiang.work@gmail.com',
    url='https://github.com/seamanj/tfrecord_tj.git',
    packages=find_packages(),
    license='MIT',
    install_requires=install_requires
)
