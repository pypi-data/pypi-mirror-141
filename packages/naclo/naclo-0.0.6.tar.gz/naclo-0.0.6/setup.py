from setuptools import setup, find_packages


setup(
    name='naclo',
    version='0.0.6',
    description='Cleaning toolset for small molecule drug discovery datasets',
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
