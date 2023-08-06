#!/usr/bin/env python
# coding: utf-8
#
# Licensed under MIT
#
import setuptools

setuptools.setup(
    install_requires=['flask>=2.0.1','requests'],
    version='1.0.4',
    packages=setuptools.find_namespace_packages(include=["solox", "solox.*"], ),
    include_package_data=True
)