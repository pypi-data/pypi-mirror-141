"""
Allows installation via pip, e.g. by navigating to this directory with the command prompt, and using 'pip install .'
"""

import sys
from setuptools import setup, find_packages

setup(
    name='cusfbamboo',
    author = 'Daniel Gibbons',                 
    author_email = 'daniel.u.gibbons@gmail.com',        
    version='0.2.1',
    license = '	gpl-3.0',
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib', 'scipy'],
    description='Cooling system modelling for liquid rocket engines',
    keywords = ['rocket', 'engine', 'liquid', 'cooling', 'spaceflight', 'thermal'],
    download_url = 'https://github.com/cuspaceflight/bamboo/archive/refs/tags/0.2.1.tar.gz',
    url = 'https://github.com/cuspaceflight/bamboo',
    classifiers=[
        'Development Status :: 4 - Beta',     
        'Intended Audience :: Science/Research',    
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   
        'Programming Language :: Python :: 3'],
)
