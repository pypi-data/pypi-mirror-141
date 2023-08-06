import setuptools
from setuptools import setup

if __name__ == "__main__":
    setup()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "bp_dependency", # Replace with your own username
    version = "0.0.0",
    author = "Joris Pries",
    author_email = "joris.pries@cwi.nl",
    description = "Package to measure the Berkelmans-Pries dependency",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/joris-pries/Official_Dependency_Function",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)