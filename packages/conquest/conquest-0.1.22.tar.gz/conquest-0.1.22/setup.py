# coding: utf-8

"""
    Conquest Public API

    This package is the official Python SDK to build projects using the Conquest Public API.

    Generated with: https://github.com/swagger-api/swagger-codegen.git
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "conquest"
VERSION = "0.1.22"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "certifi>=2017.4.17",
    "python-dateutil>=2.1",
    "six>=1.10",
    "urllib3>=1.23"
]
    

setup(
    name=NAME,
    version=VERSION,
    description="Conquest Public API",
    author="Gil Bassi",
    author_email="gbassi@conquestsoftware.com.au",
    url="https://github.com/gbassicq/python-conquest/",
    keywords=["Conquest", "Conquest Public API", "Conquest 4"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=("test",)),
    include_package_data=True,
    long_description="""\
    This is the official Conquest API SDK, still undergoing tests
    """
)
