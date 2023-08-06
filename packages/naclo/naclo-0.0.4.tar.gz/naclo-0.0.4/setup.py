import pathlib
from setuptools import find_packages, setup


HERE = pathlib.Path(__file__).parent

setup(
    name='naclo',
    version='0.0.4',
    description='Cleaning toolset for small molecule drug discovery datasets.',
    author='Jacob Gerlach',
    author_email='wgerlach00@gmail.com',
    packages=find_packages(exclude=('__unit_tests',)),
)