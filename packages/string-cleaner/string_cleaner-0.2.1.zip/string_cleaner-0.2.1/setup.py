"""
:author: v.oficerov
:license: MIT
:copyright: (c) 2022 www.sqa.engineer
"""

from setuptools import setup
from os.path import dirname

version = '0.2.1'
short_description = """Module for clean string from special chars and replace it by html-entity."""

with open(f'{dirname(__file__)}\\README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='string_cleaner',
    version=version,
    author='v.oficerov',
    author_email='valeryoficerov@gmail.com',
    description=short_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Oficerov/string_cleaner',
    download_url='https://github.com/Oficerov/string_cleaner/archive/refs/heads/master.zip',
    license='MIT',
    packages=['string_cleaner'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]

)
