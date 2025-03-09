from setuptools import setup, find_packages

setup(
    name="Fraud_Agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pydantic",
        "python-dotenv"
    ],
) import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "PokerGame",
    version = "0.0.4",
    author = "Dave",
    author_email = "l33tsux42@gmail.com",
    description = ("Small summer project to escape from the boredom"
                                   "just about it"),
    license = "GNU",
    keywords = "example documentation tutorial",
    url = "http:/github.com/davidus27/pokerGame",
    packages=['an_example_pypi_project', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU License",
    ],
)
