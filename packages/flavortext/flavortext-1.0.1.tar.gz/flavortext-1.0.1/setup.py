import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="flavortext",
    version="1.0.1",
    description="Add a touch of pizzaz to your python projects.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/TheMingus/flavortext.py",
    author="Mingus",
    license="MIT",
    classifiers=["License :: OSI Approved :: MIT License"],
    packages=["flavortext"],
    include_package_data=True,
)