import setuptools
from io import BytesIO
# coding=utf-8

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name="yhproject_pkg",
        version="0.0.3",
        author="HUXIAOFENG",
        author_email="474025548@qq.com",
        description="A small example package",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/pypa/sampleproject",
        packages=setuptools.find_packages(),
        classifiers=[
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
        ],
    )
