#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
setup.py - Installs this repository as a package

Steps:
    For development (In the repo directory):
    >>> pip install -e . 

    For installation (In the repo directory):
    >>> pip install .
"""

__author__ = "Grapphy"

# Python standard libraries
from setuptools import setup


setup(
    name="pyosu",
    version="1.0",
    description="API Wrapper for osu!api v2",
    author="Grapphy",
    packages=["pyosu"],
)
