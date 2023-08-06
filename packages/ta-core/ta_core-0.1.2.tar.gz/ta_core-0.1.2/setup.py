#!/usr/bin/env python
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup_args = dict(
    name="ta_core",
    version="0.1.2",
    packages=["ta_core"],
    author="Serhii Romanets",
    author_email="serhii.romanets@thoughtfulautomation.com",
    description="Thoughtful Automation Core",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.thoughtfulautomation.com/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="ta_core, ta-core",
    include_package_data=True,
    zip_safe=False,
)

install_requires = ["requests"]

if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires)
