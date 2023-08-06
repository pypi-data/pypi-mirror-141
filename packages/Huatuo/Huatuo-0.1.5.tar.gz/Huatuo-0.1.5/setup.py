#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Huatuo",
    version="0.1.5",
    author="Eason Hua",
    author_email="",
    description="Provide medical NER service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/easonforai/Huatuo",
    data_files=[],
    packages=find_packages(),
    install_requires=['tqdm==4.62.3', 'numpy==1.21.5', 'keras==2.3.1', 'tensorflow==2.1.0',
                      'bert4keras==0.10.9', 'pyahocorasick==1.4.4'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    zip_sage=False,
    include_package_data=True,
)