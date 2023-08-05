from setuptools import setup, find_packages
from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="SimpleROT",
    version="0.1",
    description="A basic library made with Python, useful for encrypting strings or files with ROT cipher.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fix-22/SimpleROT",
    author="Fix-22",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["SimpleROT"],
    include_package_data=True,
)