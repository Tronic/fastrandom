"""fastrandom"""
import codecs
import os
import re
import sys

from setuptools import find_packages, setup

def open_local(paths):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), *paths)
    return codecs.open(path, "r", "UTF-8")

with open_local(["fastrandom", "__version__.py"]) as fp:
    try:
        version = re.findall(
            r"^__version__ = \"([^']+)\"\r?$", fp.read(), re.M
        )[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")

with open_local(["README.md"]) as rm:
    long_description = rm.read()

setup_kwargs = {
    "name": "fastrandom",
    "version": version,
    "url": "http://github.com/Tronic/fastrandom",
    "license": "MIT",
    "author": "L. Karkkainen",
    "description": (
        "A shell tool to generate random bytes extremely fast e.g. for SSD scrubbing."
    ),
    "long_description": long_description,
    "long_description_content_type": 'text/markdown',
    "packages": find_packages(),
    "platforms": "any",
    "python_requires": ">=3.8",
    "classifiers": [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    "entry_points": {"console_scripts": ["fastrandom = fastrandom.__main__:main"]},
    "install_requires": [
        "cryptography",
    ],
}

setup(**setup_kwargs)
