#!/usr/bin/env python3
# encode: utf-8
from setuptools import setup, find_packages, Extension
from distutils.core import setup, Extension

# read the contents of the README
with open('README.md') as README_md:
    README = README_md.read()


def get_info():
    print('test')


get_info()

setup(
    name='testcasescrate',
    version='0.1.2',
    description='help people find spider',
    keywords=' '.join([
        'Pypi',
    ]),
    classifiers=[
        'License :: Free For Educational Use',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    url='https://lossyou.com',
    author='OuYanghaoyue',
    author_email='111@qq.com',
    long_description=README,
    long_description_content_type="text/markdown",
    license='Proprietary',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    install_requires=[''],
    entry_points={
        'console_scripts': [
            'say_hello=say_hello:say',
        ]
    }
)