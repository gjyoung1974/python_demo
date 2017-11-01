from setuptools import setup, find_packages
import sys

version = '0.0.1'

setup(
    name='homepage',
    author='Joe Viveiros',
    author_email='joe.viveiros@verygood.systems',
    version=version,
    description='VGS Demo',
    scripts=['bin/run.py'],
    license='Other/Proprietary License',
    include_package_data=True,
    packages=['website_forms'],
    install_requires=[
        'flask',
        'requests',
   ],
)
