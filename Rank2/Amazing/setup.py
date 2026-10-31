"""Setup script for the maze generator package.

This file allows the maze_generator module to be packaged and installed
via pip. It defines metadata and dependencies.
"""

from setuptools import setup, find_packages

setup(
    name='mazegen-huwang-yuhli',
    version='1.0.0',
    description='A maze generator module implementing recursive backtracking',
    author='huwang_yuhli',
    packages=find_packages(),
    py_modules=['maze_generator'],
    python_requires='>=3.10',
)
