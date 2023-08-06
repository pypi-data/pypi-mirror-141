#!/usr/bin/env python
from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='cam-tool',
    version='0.0.7',
    description='Cloud Assignment Manager Tool',
    url='https://github.com/fuzihaofzh/cam-tool',
    author='',
    author_email='',
    license='',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    keywords='Cloud Assignment Manager',
    packages=find_packages(),
    install_requires=[
          'fire', 'pyyaml', 'redis', 'tabulate'
    ],
    entry_points={
          'console_scripts': [
              'cam = cam.cam:main'
          ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
)