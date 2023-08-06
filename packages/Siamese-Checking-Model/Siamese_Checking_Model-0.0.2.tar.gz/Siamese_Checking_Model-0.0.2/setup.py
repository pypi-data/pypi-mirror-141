#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
	]

setup(
    name='Siamese_Checking_Model',
    version='0.0.2',
    description="Models used for face_recognition by siamese neural network.",
    long_description=readme,
	long_description_content_type="text/markdown",
    author="AlphonseInbarajXavier",
    author_email='xalphonse@gmail.com',
    url='https://github.com/xalphonseinbaraj/Siamese_Checking_Model',
    packages=[
        'Siamese_Checking_Model',
    ],
    package_dir={'Siamese_Checking_Model': 'Siamese_Checking_Model'},
    package_data={
        'Siamese_Checking_Model': ['models/*.dat'],
				
    },
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='Siamese_Checking_Model',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],

)
