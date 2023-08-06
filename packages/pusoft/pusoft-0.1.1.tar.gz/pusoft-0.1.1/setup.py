#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='pusoft',
    version='0.1.1',
    author='Pumpkin_1001',
    author_email='2752349525@qq.com',
    url='https://github.com/pumkin1001/pusoft',
    description=u'PUSoft Tools',
    packages=['pusoft'],
    install_requires=['colorama'],
    entry_points={
        'console_scripts': [
            'pusoft=pusoft.home_page:cmd',
            'pupm=pusoft.pusoft_package_manager:cmd'
        ]
    }
)