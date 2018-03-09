from setuptools import setup, find_packages
import sys

version = '0.0.1'

setup(
    name='homepage',
    author='Joe Viveiros',
    author_email='joe.viveiros@verygood.systems',
    version=version,
    description='VGS Demo',
    license='Other/Proprietary License',
    include_package_data=True,
    packages=['.'],
    install_requires=[
        "gunicorn",
        "requests",
        "flask_sqlalchemy",
        "flask-admin",
   ],
)
