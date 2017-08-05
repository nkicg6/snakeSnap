#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

setup(
    name='snakesnap',
    version='0.1.0',
    description="""snakesnap is a python project with a
    simple flask interface to take a picture with a thermal camera
    and email them to the user.""",
    author="Nicholas George",
    scripts=['src', 'app'],
    author_email='nicholas.m.george@ucdenver.edu',
    url='https://github.com/nkicg6/snakesnap',
    packages=find_packages(include=['snakesnap']),
    include_package_data=True,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='snakesnap',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
)
