#!/usr/bin/env python

from os.path import isfile

from setuptools import setup


def _read_file(path):
    with open(path) as fp:
        return fp.read().strip()


PROJECT_VERSION = _read_file("VERSION.txt")

REQUIREMENTS = _read_file("requirements.txt").split("\n")
DEV_REQUIREMENTS = _read_file("requirements_dev.txt").split("\n")


if isfile("README.md"):
    long_description = _read_file("README.md")
else:
    long_description = ""

setup(
    name="csh-sanitizer",
    author="Sunil Kumar",
    url="https://github.com/sunil-reglobe/csh-sanitizer",
    description="Convert basic HTML into JSON format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=PROJECT_VERSION,
    packages=["csh_sanitizer"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=REQUIREMENTS,
    extras_require={"dev": DEV_REQUIREMENTS},
    zip_safe=False,
)
