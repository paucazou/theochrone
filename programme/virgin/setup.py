#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("slaves.py")
    )
