from setuptools import setup

VERSION = '0.0.21'
DESCRIPTION = 'get data for your soccer team from fupa.net'
LONG_DESCRIPTION = 'A package that uses fupa.net to get data for your soccer team'

# Setting up
setup(
    name="fupa_client",
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=['fupa_client', 'fupa_client.models', 'fupa_client.repositories'],
    install_requires=['requests', 'beautifulsoup4', 'lxml', 'python-dateutil'],
)
