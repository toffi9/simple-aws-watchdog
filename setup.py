#!/usr/bin/env python3from codecs import open
from setuptools import find_packages, setup


setup(
    name='aws_watchdog',
    version='0.0.1',
    description='',
    url='https://bitbucket.org/toffi9/aws-watchdog',
    author='Mateusz Kamycki',
    author_email='mateusz.kamycki@gmail.com',
    license='MIT',
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'boto3==1.4.6',
        'click==6.7',
        'python-daemon==2.1.2',
    ],
    scripts=[
        'aws_watchdogd',
    ],
)
