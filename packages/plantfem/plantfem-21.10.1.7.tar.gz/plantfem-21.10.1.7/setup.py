"""Minimal setup file for tasks project."""
import os
from setuptools import setup, find_packages

print("Prior to install this,")
print("please run")
print("git clone https://github.com/kazulagi/plantFEM && cd plantFEM && python3 install.py")

setup(
    name='plantfem',
    version='21.10.1.7',
    license='MIT',
    description='Module Experiment',
    author='kazulagi',
    author_email='hogehoge@gmail.com',
    url='https://plantfem.org',
    packages=find_packages("src"),
    package_dir={'src': ''},
    install_requires=[
        'numpy>=1.14.5',
        'matplotlib>=2.2.0',
    ],
    entry_points={
        'console_scripts':[
            'plantfem = src.plantfem:plantfem',
        ],
    },
)

os.system("export PYTHONPATH=$PYTHONPATH:/opt/plantfem")