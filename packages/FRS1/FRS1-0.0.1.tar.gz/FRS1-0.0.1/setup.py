#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import codecs
import os
import setuptools

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
	'absl-py==0.10.0',
	'astor==0.8.1',
	'certifi==2020.6.20',
	'click>=8.0.3',
	'colorama==0.4.4',
	'cycler==0.10.0',
	'dlib>=19.16.0',
	'h5py==2.8.0',
	'imutils==0.5.1',
	'itsdangerous==2.0.1',
	'Keras>=2.2.4',
	'Keras-Applications==1.0.8',
	'Keras-Preprocessing==1.1.2',
	'matplotlib==3.0.0',
	'numpy>=1.16.0',
	'opencv-python==3.4.3.18',
	'python-dateutil==2.8.1',
	'PyYAML==5.3.1',
	'scipy==1.1.0',
	'six==1.15.0',
	'tensorboard==1.15.0',
	'tensorflow==1.15.2',
	'tensorflow-estimator==1.15.1',
	'termcolor==1.1.0',
	'Werkzeug==2.0.2',
	'wincertstore==0.2',
	'wrapt==1.12.1',
	'zipp==3.3.0'
    ]

# Setting up
setup(
    name="FRS1",
    version='0.0.1',
	description='Face Recogition for Siamese(FRS)',
	long_description=readme,
	long_description_content_type="text/markdown",
    author="AlphonseInbarajXavier",
    author_email="xalphonse@gmail.com",
    url='https://github.com/xalphonseinbaraj/FRS1',
	packages=[
        'FRS1',
    ],
    package_dir={'FRS1': 'FRS1'},
	package_data={
        'FRS1': ['*.dat','*.xml','*.h5']
		    },
    license="MIT license",
    zip_safe=False,
    keywords='Siamese_Checking_Model',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.6",
        "Natural Language :: English",
    ]
)
