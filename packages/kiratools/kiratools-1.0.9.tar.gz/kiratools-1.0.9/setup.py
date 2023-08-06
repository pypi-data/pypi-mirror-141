from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.9'
DESCRIPTION = 'nothing'
LONG_DESCRIPTION = 'nothing'

# Setting up
setup(
    name="kiratools",
    version=VERSION,
    author="Abdulaziz Alshaye",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=['requests','paramiko','bs4'],
    keywords=['python']
    )