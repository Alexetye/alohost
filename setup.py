#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: ALeDo
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2023 ALeDo
"""

version = '1.8.9'
'''
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
'''

long_description = '''Python module for Alo Host project
                    managenent platform (AloHost API wrapper)'''
                    
setup(    
    name='alohost',
    version=version,
    
    author='ALeDo',
    author_email='fedlexs20@gmail.ru',
    
    description=(
        u'Python module for writing scripts for project management platfrom '
        u'Alo Host (alohost.io API wrapper)'
    ),
    long_description=long_description,
    #long_description_content_type='text/markdown',
    
    url='https://github.com/Alexetye/alohost',
    download_url='https://github.com/Alexetye/alohost/archive/v{}.zip'.format(
        version
    ),
    
    license='Apache License, Version 2.0, see LICENSE file',
    
    packages=['alohost'],
    install_requires=['aiohttp', 'aiosignal'],
    
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',   
    ]
)
