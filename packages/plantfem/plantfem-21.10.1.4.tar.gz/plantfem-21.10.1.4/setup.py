"""Minimal setup file for tasks project."""
import os
from setuptools import setup, find_packages

print("Prior to install this,")
print("please run")
print("git clone https://github.com/kazulagi/plantFEM && cd plantFEM && python3 install.py")

setup(
    name='plantfem',
    version='21.10.1.4',
    license='MIT',
    description='Module Experiment',
    author='kazulagi',
    author_email='hogehoge@gmail.com',
    url='https://plantfem.org',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)

os.system("export PYTHONPATH=$PYTHONPATH:/opt/plantfem")