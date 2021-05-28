from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'get data for your soccer team from fupa.net'
LONG_DESCRIPTION = 'A package that uses fupa.net to get data for your soccer team'

# Setting up
setup(
    name="fupa_client",
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=['fupa_client'],
    install_requires=['requests'],
)
