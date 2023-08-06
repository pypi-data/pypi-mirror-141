import setuptools, os, sys

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# SEARCH/REPLACE package_name WITH THE ACTUAL PACKAGE NAME BELOW:

setuptools.setup(
    name='popgen_dashboards',
    version="1.0.1",
    author="Kasper Munch",
    author_email="kaspermunch@birc.au.dk",
    description="Short description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/kaspermunch/popgen_dashboards',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
            'numpy>=1.1',
            'dash',
            'dash_core_components',
            'dash_html_components',
            'dash_bootstrap_components',
            'matplotlib>=3.0'
    ])