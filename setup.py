# -*- coding: utf-8 -*-

import sys
import mse

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PACKAGE = "mse"
NAME = "mysql-size-estimator"
DESCRIPTION = "Mysql Table Size Estimator"
AUTHOR = u'Özgür Orhan'
AUTHOR_EMAIL = "ozgur.orhan@gmail.com"
URL = "http://github.com/frail/mysql-size-estimator"
VERSION = __import__(PACKAGE).__version__


def readme():
    with open('README.md') as f:
        return f.read()


def requirements():
    install_requires = []
    with open('requirements.txt') as f:
        for line in f:
            install_requires.append(line.strip())

    # Terminal colors for Windows
    if 'win32' in str(sys.platform).lower():
        install_requires.append('colorama>=0.2.4')

    return install_requires

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme(),
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=mse.__license__,
    packages=['mse'],
    entry_points={'console_scripts': ['mysql-size-estimator = mse.__main__:main']},
    install_requires=requirements(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7"
        ],
    keywords=['mysql', 'size', 'estimate', 'size-estimator', 'innodb'],
    include_package_data=True,
    zip_safe=False,
    )